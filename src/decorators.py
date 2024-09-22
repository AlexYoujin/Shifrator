import functools
import logging
import os


def log(module_name: str):
    def decorator_log(func):
        @functools.wraps(func)
        def wrapper_log(*args, **kwargs):
            log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
            os.makedirs(log_dir, exist_ok=True)
            log_filename = os.path.join(log_dir, f"{module_name}.log")

            logger = logging.getLogger(module_name)
            logger.setLevel(logging.INFO)

            # Очищаем обработчики, чтобы избежать дублирования
            if logger.hasHandlers():
                logger.handlers.clear()

            file_handler = logging.FileHandler(log_filename, mode='w')
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(file_formatter)

            stream_handler = logging.StreamHandler()
            stream_formatter = logging.Formatter(
                "%(name)s - %(levelname)s - %(message)s"
            )
            stream_handler.setFormatter(stream_formatter)

            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)

            func_name = func.__name__
            logger.info(f"Function {func_name} started. Inputs: {args}, {kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"Function {func_name} ended. Result: {result}")

                # Принудительный сброс буфера
                for handler in logger.handlers:
                    if isinstance(handler, logging.FileHandler):
                        handler.flush()

                return result
            except Exception as e:
                logger.error(f"Function {func_name} failed. Error: {e}. Inputs: {args}, {kwargs}")
                raise e

        return wrapper_log

    return decorator_log
