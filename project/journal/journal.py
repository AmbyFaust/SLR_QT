import logging


class Journal:

    def __init__(self):
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.formatter)

        self.logger = logging.getLogger('journal')
        self.logger.addHandler(stream_handler)
        self.logger.setLevel(logging.INFO)

    def log(self, text, *, attr=None, module=None):
        if module is not None:
            msg = f'[{module}]. {text}'
        else:
            msg = f'{text}'

        msg += '\n'

        if self.logger and attr is not None:
            getattr(self.logger, attr)(msg)
        else:
            print(f'{msg}')
