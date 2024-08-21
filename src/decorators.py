import functools
import logging
import os
from datetime import datetime
import inspect


def log():
    def decorator_log(func):
        @functools.wraps(func)
        def wrapper_log(*args, **kwargs):
            # Определяем имя модуля, где находится функция
            module = inspect.getmodule(func)
            if module is None:
                # Если не удается определить модуль, используем __main__
                module_name = '__main__'
            else:
                module_name = module.__name__

            # Путь к папке logs в корне проекта
            log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
            os.makedirs(log_dir, exist_ok=True)  # Создаем папку logs, если ее нет
            log_filename = os.path.join(log_dir, f"{module_name}.log")

            # Настраиваем логгер
            logger = logging.getLogger(module_name)
            logger.setLevel(logging.INFO)

            handler = logging.FileHandler(log_filename)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)

            # Удаляем старые хендлеры, чтобы не дублировать логи
            if logger.hasHandlers():
                logger.handlers.clear()

            logger.addHandler(handler)

            func_name = func.__name__
            start_time = datetime.now()
            logger.info(f"Function {func_name} started. Inputs: {args}, {kwargs}")
            try:
                result = func(*args, **kwargs)
                end_time = datetime.now()
                logger.info(f"Function {func_name} ended. Result: {result}")
                return result
            except Exception as e:
                logger.error(f"Function {func_name} failed. Error: {e}. Inputs: {args}, {kwargs}")
                raise e

        return wrapper_log

    return decorator_log
