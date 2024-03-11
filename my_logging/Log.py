import logging
import os
from datetime import datetime


class Log:
    LOG_CLASS = __name__
    logger = logging.getLogger(LOG_CLASS)

    @staticmethod
    def set_output(output_type, log_level):
        level = getattr(logging, log_level.upper(), logging.NOTSET)
        Log.logger.setLevel(level)
        handler = logging.StreamHandler() if output_type.lower() == "console" else logging.FileHandler(
            Log.get_log_file_name())
        handler.setLevel(level)
        Log.logger.addHandler(handler)
        Log.logger.propagate = False

    @staticmethod
    def log_message(message, level, method_name=None):
        if level == "info":
            Log.logger.info(message)
        elif level == "warning":
            Log.logger.warning(f"{Log.LOG_CLASS}.{method_name} - {message}")
        elif level == "debug":
            Log.logger.debug(message)

    @staticmethod
    def get_log_file_name():
        log_dir = os.path.join(os.getcwd(), "output-logs")
        os.makedirs(log_dir, exist_ok=True)
        return os.path.join(log_dir, datetime.now().strftime("%Y-%m-%d;%H:%M:%S.log"))

# # Set the output type and log level
# Log.set_output("console", "DEBUG")
#
# # Log a debug message
# Log.log_message("This is a debug message", "debug")
#
# # Log an info message
# Log.log_message("This is an info message", "info")
#
# # Log a warning message
# Log.log_message("This is a warning message", "warning", "method_name")
