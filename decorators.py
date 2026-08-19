import os
from datetime import datetime

def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            with open(path, 'a', encoding='utf-8') as file:
                result = old_function(*args, **kwargs)
                file.write(f'{datetime.now()} Вызывается функция {old_function.__name__} с аргументами {args} и {kwargs} результат {result} ')
                return result
        return new_function
    return __logger