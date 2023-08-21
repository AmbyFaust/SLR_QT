from external import concurrent_manager, waiter

from project.journal import Journal

# журналирование
journal = Journal()


# работа с потоками
concur_manager = concurrent_manager
concur_waiter = waiter.Waiter
