import logging
import os
from datetime import datetime

class Log:
    LOG_CLASS = Log.__name__

    logging.basicConfig(level=logging.NOTSET)
    logger = logging.getLogger(LOG_CLASS)

    def __init__(self):
        raise ValueError("Log class should not be instantiated.")

    @staticmethod
    def set_output(output_type, log_level):
        log_level = log_level.upper()
        output_type = output_type.lower()
        level = getattr(logging, log_level, logging.NOTSET)
        Log.logger.setLevel(level)
        Log.set_output_helper(output_type, level)

    @staticmethod
    def set_output_helper(output_type, log_level):
        handler = None
        if output_type == "file":
            try:
                handler = logging.FileHandler(Log.get_log_file_name())
                handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            except (IOError, OSError) as e:
                print(e)
        else:
            handler = logging.StreamHandler()

        handler.setLevel(log_level)
        Log.logger.addHandler(handler)
        Log.logger.propagate = False

    @staticmethod
    def other(message):
        Log.logger.info(message)

    @staticmethod
    def error(message, method_name):
        Log.logger.warning(f"{Log.LOG_CLASS}.{method_name} - {message}")

    @staticmethod
    def debug(message, class_name, command):
        Log.logger.debug(f"{class_name}.{command} - {message}")

    @staticmethod
    def sent(message):
        Log.logger.info(f"{Log.LOG_CLASS}.SENT - {message}")

    @staticmethod
    def received(message):
        Log.logger.info(f"{Log.LOG_CLASS}.RECEIVED - {message}")

    @staticmethod
    def get_log_file_name():
        cwd = os.getcwd()
        log_dir = os.path.join(cwd, "output-logs")

        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        filename = datetime.now().strftime("%Y-%m-%d;%H:%M:%S.log")

        return os.path.join(log_dir, filename)
