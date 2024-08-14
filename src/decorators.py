import functools
import logging
import sys
from datetime import datetime


def log(filename=None):
    # Конфигурация логирования
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if filename:
        handler = logging.FileHandler(filename)
    else:
        handler = logging.StreamHandler(
            sys.stdout
        )  # Используем sys.stdout для вывода в консоль

    formatter = logging.Formatter("%(levelname)s:%(message)s")
    handler.setFormatter(formatter)

    # Удаляем предыдущие хендлеры
    if logger.handlers:
        logger.handlers.clear()

    logger.addHandler(handler)

    def decorator_log(func):
        @functools.wraps(func)
        def wrapper_log(*args, **kwargs):
            func_name = func.__name__
            start_time = datetime.now()
            logger.info(
                f"Function {func_name} started at {start_time}. Inputs: {args}, {kwargs}"
            )
            try:
                result = func(*args, **kwargs)
                end_time = datetime.now()
                logger.info(
                    f"Function {func_name} ended at {end_time}. Result: {result}"
                )
                return result
            except Exception as e:
                end_time = datetime.now()
                logger.error(
                    f"Function {func_name} failed at {end_time}. Error: {e}. Inputs: {args}, {kwargs}"
                )
                raise e

        return wrapper_log

    return decorator_log
