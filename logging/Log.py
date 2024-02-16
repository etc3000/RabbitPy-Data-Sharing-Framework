# import logging
# import os
# from datetime import datetime
#
#
# class Log:
#     """
#     A utility class for logging messages. This class should not be instantiated.
#     """
#     LOG_CLASS = Log.__name__
#
#     # Set up the basic configuration for the logger
#     logging.basicConfig(level=logging.NOTSET)
#     logger = logging.getLogger(LOG_CLASS)
#
#     def __init__(self):
#         """
#         Raises an error if an attempt is made to instantiate the Log class.
#         """
#         raise ValueError("Log class should not be instantiated.")
#
#     @staticmethod
#     def set_output(output_type, log_level):
#         """
#         Sets the output type and log level for the logger.
#
#         Args:
#             output_type (str): The type of output (e.g., "file" or "console").
#             log_level (str): The level of logging (e.g., "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL").
#         """
#         log_level = log_level.upper()
#         output_type = output_type.lower()
#         level = getattr(logging, log_level, logging.NOTSET)
#         Log.logger.setLevel(level)
#         Log.set_output_helper(output_type, level)
#
#     @staticmethod
#     def set_output_helper(output_type, log_level):
#         """
#         Helper method to set the output type and log level for the logger.
#
#         Args:
#             output_type (str): The type of output (e.g., "file" or "console").
#             log_level (str): The level of logging (e.g., "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL").
#         """
#         handler = None
#         if output_type == "file":
#             try:
#                 handler = logging.FileHandler(Log.get_log_file_name())
#                 handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
#             except (IOError, OSError) as e:
#                 print(e)
#         else:
#             handler = logging.StreamHandler()
#
#         handler.setLevel(log_level)
#         Log.logger.addHandler(handler)
#         Log.logger.propagate = False
#
#     @staticmethod
#     def other(message):
#         """
#         Logs an informational message.
#
#         Args:
#             message (str): The message to log.
#         """
#         Log.logger.info(message)
#
#     @staticmethod
#     def error(message, method_name):
#         """
#         Logs a warning message.
#
#         Args:
#             message (str): The message to log.
#             method_name (str): The name of the method where the error occurred.
#         """
#         Log.logger.warning(f"{Log.LOG_CLASS}.{method_name} - {message}")
#
#     @staticmethod
#     def debug(message, class_name, command):
#         """
#         Logs a debug message.
#
#         Args:
#             message (str): The message to log.
#             class_name (str): The name of the class where the debug message is being logged.
#             command (str): The command or method where the debug message is being logged.
#         """
#         Log.logger.debug(f"{class_name}.{command} - {message}")
#
#     @staticmethod
#     def sent(message):
#         """
#         Logs a message indicating that something was sent.
#
#         Args:
#             message (str): The message to log.
#         """
#         Log.logger.info(f"{Log.LOG_CLASS}.SENT - {message}")
#
#     @staticmethod
#     def received(message):
#         """
#         Logs a message indicating that something was received.
#
#         Args:
#             message (str): The message to log.
#         """
#         Log.logger.info(f"{Log.LOG_CLASS}.RECEIVED - {message}")
#
#     @staticmethod
#     def get_log_file_name():
#         """
#         Generates a log file name based on the current date and time.
#
#         Returns:
#             str: The generated log file name.
#         """
#         cwd = os.getcwd()
#         log_dir = os.path.join(cwd, "output-logs")
#
#         if not os.path.exists(log_dir):
#             os.mkdir(log_dir)
#
#         filename = datetime.now().strftime("%Y-%m-%d;%H:%M:%S.log")
#
#         return os.path.join(log_dir, filename)
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
        handler = logging.StreamHandler() if output_type.lower() == "console" else logging.FileHandler(Log.get_log_file_name())
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