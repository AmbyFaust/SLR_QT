import logging
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import List, Callable, Any, Union, Tuple, Dict
from threading import Lock
from abc import abstractmethod, ABC

Task = Union[Callable[..., Any],
             List[Callable[..., Any]],
             List[Tuple[Callable[..., Any], Tuple[Any]]],
             List[Tuple[Callable[..., Any], Tuple[Any], Dict[str, Any]]]]


class IFuture(ABC):
    def __init__(self, manager: 'ConcurrentManager'):
        self.maneger = manager
        self._canceled = False
        self.promises = []
        self._exception = None

    def _done(self):
        self.maneger.futures.discard(self)
        pass

    def cancel(self):
        self.maneger.futures.discard(self)
        self._canceled = True
        for promise in self.promises:
            promise.cancel()

    @property
    def canceled(self):
        return self._canceled

    def exception(self):
        return self._exception

    @abstractmethod
    def done(self):
        pass

    @abstractmethod
    def add_callback(self, callback: Callable[[Any], Any], notifier):
        pass

    def __promise_callback(self, args, *, promise: 'Promise', func: Callable[[List[Any]], Task]):
        if self._canceled:
            return
        rec = func(args)
        future = self.maneger.add_task(rec)
        promise._set_future(future)

    def chain(self, func: Callable[[List[Any]], Task]):
        promise = Promise(self.maneger)
        self.maneger.futures.add(promise)
        self.add_callback(partial(self.__promise_callback, promise=promise, func=func))
        self.promises.append(promise)
        return promise


class Promise(IFuture):
    def __init__(self, manager):
        super(Promise, self).__init__(manager)
        self.future = None
        self.callbacks = []

    def cancel(self):
        super(Promise, self).cancel()
        if self.future is not None:
            if self.future.done():
                return
            self.future.cancel()
        for _, notifier in self.callbacks:
            if notifier is not None:
                notifier(done=True)

    def done(self):
        if self.future is not None:
            return self.future.done()
        return False

    def exception(self):
        if self.future:
            return self.future.exception()
        return super(Promise, self).exception()

    def _set_future(self, future: IFuture):
        self.future = future
        if self._canceled:
            future.cancel()
            return
        for callback, notifier in self.callbacks:
            self.future.add_callback(callback, notifier)
        self._done()

    def add_callback(self, callback, notifier=None):
        if self._canceled:
            return
        if self.future is not None:
            self.future.add_callback(callback, notifier)
        else:
            self.callbacks.append((callback, notifier))
        return self


class Future(IFuture):
    def __init__(self, manager, future):
        super(Future, self).__init__(manager)
        self.future = future
        self.notifiers = []

    def cancel(self):
        super(Future, self).cancel()
        if self.future.done():
            return
        self.future.cancel()
        for notifier in self.notifiers:
            notifier(done=True)

    def done(self):
        return self.future.done()

    def exception(self):
        if self._exception:
            return self._exception
        return self.future.exception()

    def __result_callback(self, future, *, callback, notifier=None):
        if self._canceled:
            if notifier:
                notifier(done=True)
            return
        try:
            args = future.result()
        except Exception as e:
            logging.getLogger('debug').exception('ERR')
            self._exception = e
            self.cancel()
            if notifier:
                notifier(done=True)
            return
        callback(args)
        if notifier:
            notifier()
        self._done()

    def add_callback(self, callback, notifier=None):
        self.future.add_done_callback(partial(self.__result_callback, callback=callback, notifier=notifier))
        if notifier:
            self.notifiers.append(notifier)
        return self


class Futures(IFuture):
    def __init__(self, manager, futures):
        super(Futures, self).__init__(manager)
        self.futures = futures
        self.__add_lock = Lock()
        self.__callback_lock = Lock()
        self.callbacks_list = []
        self.done_list = []

    def cancel(self):
        super(Futures, self).cancel()
        all_done = True
        for f in self.futures:
            if not f.done():
                all_done = False
            else:
                f.cancel()
        if all_done:
            return
        for _, notifier in self.callbacks_list:
            if notifier:
                notifier(done=True)

    def done(self):
        for f in self.futures:
            if not f.done():
                return False
        return True

    def exception(self):
        if self._exception:
            return self._exception
        for f in self.futures:
            e = f.exception()
            if e is not None:
                return e

    def __results_callback(self, future, *, num, notifier=None):
        if self._canceled:
            if notifier:
                notifier(done=True)
            return
        try:
            args = future.result()
        except Exception as e:
            logging.getLogger('debug').exception('ERR')
            self._exception = e
            self.cancel()
            if notifier:
                notifier(done=True)
            return
        with self.__callback_lock:
            if notifier:
                notifier(len(self.done_list[num]), len(self.futures))
            self.done_list[num].append(args)
            if len(self.done_list[num]) == len(self.futures):
                callback, notifier = self.callbacks_list[num]
                callback(self.done_list[num])
                self._done()

    def add_callback(self, callback, notifier=None):
        with self.__add_lock:
            num = len(self.callbacks_list)
            self.callbacks_list.append((callback, notifier))
            self.done_list.append([])
        for f in self.futures:
            f.add_done_callback(partial(self.__results_callback, num=num, notifier=notifier))
        return self


class FakeFuture(IFuture):
    def __init__(self, manager):
        super(FakeFuture, self).__init__(manager)

    def done(self):
        return True

    def add_callback(self, callback, notifier=None):
        if not self.canceled:
            callback([])
            self._done()
        if notifier:
            notifier(done=True)
        return self


class ConcurrentManager:
    def __init__(self, max_threads=min(32, multiprocessing.cpu_count() + 4)):
        self.pool = ThreadPoolExecutor(max_threads)
        self.done = False
        self.futures = set()

    def __task(self, func, *args, **kwargs):
        future = self.pool.submit(func, *args, **kwargs)
        return Future(self, future)

    def __tasks(self, funcs):
        if len(funcs) == 0:
            return FakeFuture(self)
        futures = []
        for func in funcs:
            if self.done:
                return FakeFuture(self)
            if callable(func):
                futures.append(self.pool.submit(func))
            elif len(func) == 2:
                futures.append(self.pool.submit(func[0], *func[1]))
            else:
                futures.append(self.pool.submit(func[0], *func[1], **func[2]))
        return Futures(self, futures)

    def add_task(self, task, *args, **kwargs):
        if self.done:
            res = FakeFuture(self)
        elif isinstance(task, List):
            res = self.__tasks(task)
        else:
            res = self.__task(task, *args, **kwargs)
        self.futures.add(res)
        return res

    def cancel_all(self):
        while self.futures:
            try:
                f = self.futures.pop()
                f.cancel()
            except IndexError:
                continue

    def shutdown(self):
        self.done = True
        self.cancel_all()
        self.pool.shutdown(wait=False)


concurrent_manager = ConcurrentManager()
