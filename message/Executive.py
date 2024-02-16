# import os
# import subprocess
# import threading
# import tempfile
# from pathlib import Path
# from message import Message  # Assuming you have a Message class defined
# from rabbitmq import RabbitMQConnection  # Assuming you have a RabbitMQConnection class defined
# from logging import Log  # Assuming you have a Log class defined
#
# class Executive:
#     """
#     The Executive class is responsible for executing commands in a separate thread.
#     It also handles the communication with the RabbitMQ server.
#     """
#
#     def __init__(self):
#         """
#         Initializes the Executive class.
#         """
#         self.done = False
#         self.process = None
#         self.running = None
#
#         # Special command
#         self._cwd_to_follow = "CWD_TO_FOLLOW"
#
#         # M1 Mac paths
#         self.homebrew_bin = "/opt/homebrew/bin"
#         self.homebrew_sbin = "/opt/homebrew/sbin"
#         self.homebrew_path = ":/opt/homebrew/bin:/opt/homebrew/sbin"
#
#         # Current working dir
#         self._cwd = None
#
#         # For executing wormhole send
#         self.connection = None
#         self.user_id = None
#         self.filepath = None
#         self.origin_message_id = None
#         self.request_user_id = None
#
#         # Message sent to request the data
#         self.request_message = None
#
#     def set_cwd(self, cwd):
#         """
#         Sets the current working directory.
#
#         Args:
#             cwd (str): The path to the current working directory.
#         """
#         self._cwd = cwd
#
#     def set_connection(self, connection):
#         """
#         Sets the RabbitMQ connection.
#
#         Args:
#             connection (RabbitMQConnection): The RabbitMQ connection.
#         """
#         self.connection = connection
#
#     def set_user_id(self, user_id):
#         """
#         Sets the user ID.
#
#         Args:
#             user_id (str): The user ID.
#         """
#         self.user_id = user_id
#
#     def set_filepath(self, filepath):
#         """
#         Sets the file path.
#
#         Args:
#             filepath (str): The file path.
#         """
#         self.filepath = filepath
#
#     def set_required_message_content(self, message):
#         """
#         Sets the required message content.
#
#         Args:
#             message (Message): The message.
#         """
#         self.origin_message_id = message.get_origin_message_id()
#         self.request_user_id = message.get_sender_id()
#
#     def set_request_message(self, message):
#         """
#         Sets the request message.
#
#         Args:
#             message (Message): The request message.
#         """
#         self.request_message = message
#
#     @staticmethod
#     def is_mac():
#         """
#         Checks if the operating system is Mac.
#
#         Returns:
#             bool: True if the operating system is Mac, False otherwise.
#         """
#         os_name = os.uname().sysname
#         return os_name.lower().startswith("darwin")
#
#     def is_m1(self):
#         """
#         Checks if the Mac is an M1 Mac.
#
#         Returns:
#             bool: True if the Mac is an M1 Mac, False otherwise.
#         """
#         brew_bin = Path(self.homebrew_bin)
#         brew_sbin = Path(self.homebrew_sbin)
#         return brew_bin.exists() and brew_bin.is_dir() and brew_sbin.exists() and brew_sbin.is_dir()
#
#     def send_message(self, command):
#         """
#         Sends a message to the RabbitMQ server.
#
#         Args:
#             command (str): The command to send.
#         """
#         send_data = Message(self.user_id, "sent_data")
#         send_data.add_file_path(self.filepath)
#         send_data.add_origin_message_id(self.origin_message_id)
#         send_data.add_source_user_id(self.user_id)
#         send_data.add_content(command)
#         self.connection.direct(send_data, self.request_user_id)
#
#     def request_data_again(self):
#         """
#         Requests the data again from the RabbitMQ server.
#         """
#         origin_sender_id = self.request_message.get_source_user_id()
#         self.connection.direct(self.request_message, origin_sender_id)
#
#     def temp_file_script(self, command):
#         """
#         Creates a temporary file script.
#
#         Args:
#             command (str): The command to write to the script.
#
#         Returns:
#             file: The temporary file.
#         """
#         file = None
#         try:
#             file = tempfile.NamedTemporaryFile(prefix="bCNU", delete=False)
#
#             with open(file.name, "w") as script_file:
#                 script_file.write("#!/bin/bash\n")
#
#                 # Change working dir?
#                 if self._cwd is not None:
#                     script_file.write(f'echo {self._cwd_to_follow}\n')
#                     script_file.write(f'cd {self._cwd}\n')
#                     script_file.write("pwd\n")
#
#                 # Update environment path if running on M1 Mac
#                 if self.is_mac() and self.is_m1():
#                     path = os.environ.get("PATH", "") + self.homebrew_path
#                     script_file.write(f'export PATH={path}\n')
#
#                 script_file.write(f"{command}\n")
#
#         except Exception as e:
#             print(e)
#         return file
#
#     def execute(self, command):
#         """
#         Executes a command in a separate thread.
#
#         Args:
#             command (str): The command to execute.
#         """
#         file = self.temp_file_script(command)
#         if file is None:
#             return
#
#         try:
#             process = subprocess.Popen(["bash", file.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
#                                        text=True, shell=False)
#
#             std_out_reader = process.stdout
#             std_err_reader = process.stderr
#
#             def runnable():
#                 try:
#                     process.wait()
#                     self.done = True
#                 except Exception as e:
#                     print(e)
#
#             def reader():
#                 try:
#                     while not self.done:
#                         line = std_out_reader.readline()
#                         if line:
#                             Log.debug(line, __class__.__name__, command)
#                             if "wormhole receive" in line:
#                                 self.send_message(line)
#                             if "ERROR" in line and "receive" in command:
#                                 self.request_data_again()
#                         else:
#                             try:
#                                 threading.Event().wait(0.05)
#                             except Exception as e:
#                                 print(e)
#
#                     # Flush final lines after process ended
#                     process.stdout.flush()
#                     reading = True
#                     while reading:
#                         line = std_out_reader.readline()
#                         if not line:
#                             reading = False
#                         else:
#                             Log.debug(line, __class__.__name__, command)
#
#                     # Really done
#                     std_out_reader.close()
#
#                     reading = True
#                     while reading:
#                         line = std_err_reader.readline()
#                         if not line:
#                             reading = False
#                         else:
#                             Log.error(line, __class__.__name__, command)
#
#                     std_err_reader.close()
#                 except Exception as e:
#                     print(e)
#
#                 os.remove(file.name)
#
#             self.running = threading.Thread(target=runnable)
#             self.running.start()
#             threading.Thread(target=reader).start()
#
#         except Exception as e:
#             Log.error(str(e), __class__.__name__, command)
#
#     def get_running_thread(self):
#         """
#         Gets the running thread.
#
#         Returns:
#             threading.Thread: The running thread.
#         """
#         return self.running
#
#     @staticmethod
#     def execute_static(command, dir=None):
#         """
#         Executes a command in a separate thread.
#
#         Args:
#             command (str): The command to execute.
#             dir (str, optional): The directory to execute the command in. Defaults to None.
#
#         Returns:
#             threading.Thread: The running thread.
#         """
#         executive = Executive()
#
#         if dir and dir.exists() and dir.is_dir():
#             executive.set_cwd(dir)
#
#         executive.execute(command)
#         return executive.get_running_thread()
#
#     @staticmethod
#     def execute_static_with_connection(command, dir, connection, request_message):
#         """
#         Executes a command in a separate thread with a connection to the RabbitMQ server.
#
#         Args:
#             command (str): The command to execute.
#             dir (str): The directory to execute the command in.
#             connection (RabbitMQConnection): The RabbitMQ connection.
#             request_message (Message): The request message.
#
#         Returns:
#             threading.Thread: The running thread.
#         """
#         executive = Executive()
#
#         if dir and dir.exists() and dir.is_dir():
#             executive.set_cwd(dir)
#
#         executive.set_request_message(request_message)
#         executive.set_connection(connection)
#         executive.execute(command)
#         return executive.get_running_thread()
#
#     @staticmethod
#     def execute_static_with_params(command, dir, connection, user_id, message, filepath):
#         """
#         Executes a command in a separate thread with parameters.
#
#         Args:
#             command (str): The command to execute.
#             dir (str): The directory to execute the command in.
#             connection (RabbitMQConnection): The RabbitMQ connection.
#             user_id (str): The user ID.
#             message (Message): The message.
#             filepath (str): The file path.
#         """
#         executive = Executive()
#         if dir and dir.exists() and dir.is_dir():
#             executive.set_cwd(dir)
#
#         executive.set_required_message_content(message)
#         executive.set_filepath(filepath)
#         executive.set_user_id(user_id)
#         executive.set_connection(connection)
#         executive.execute(command)
import os
import subprocess
import threading
import tempfile
from pathlib import Path
from ..message import Message
from ..rabbitmq import RabbitMQConnection
from ..logging import Log

class Executive:
    def __init__(self):
        self.done = False
        self.process = None
        self.running = None
        self._cwd = None
        self.connection = None
        self.user_id = None
        self.filepath = None
        self.origin_message_id = None
        self.request_user_id = None
        self.request_message = None

    def set_cwd(self, cwd):
        self._cwd = cwd

    def set_connection(self, connection):
        self.connection = connection

    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_filepath(self, filepath):
        self.filepath = filepath

    def set_required_message_content(self, message):
        self.origin_message_id = message.get_origin_message_id()
        self.request_user_id = message.get_sender_id()

    def set_request_message(self, message):
        self.request_message = message

    def send_message(self, command):
        send_data = Message(self.user_id, "sent_data")
        send_data.add_file_path(self.filepath)
        send_data.add_origin_message_id(self.origin_message_id)
        send_data.add_source_user_id(self.user_id)
        send_data.add_content(command)
        self.connection.direct(send_data, self.request_user_id)

    def request_data_again(self):
        origin_sender_id = self.request_message.get_source_user_id()
        self.connection.direct(self.request_message, origin_sender_id)

    def temp_file_script(self, command):
        file = tempfile.NamedTemporaryFile(prefix="bCNU", delete=False)
        with open(file.name, "w") as script_file:
            script_file.write("#!/bin/bash\n")
            if self._cwd is not None:
                script_file.write(f'cd {self._cwd}\n')
            script_file.write(f"{command}\n")
        return file

    def execute(self, command):
        file = self.temp_file_script(command)
        if file is None:
            return
        process = subprocess.Popen(["bash", file.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=False)
        std_out_reader = process.stdout
        std_err_reader = process.stderr
        class_name = self.__class__.__name__

        def runnable():
            process.wait()
            self.done = True

        def reader():
            while not self.done:
                line = std_out_reader.readline()
                if line:
                    Log.debug(line, class_name, command)
                    if "wormhole receive" in line:
                        self.send_message(line)
                    if "ERROR" in line and "receive" in command:
                        self.request_data_again()
                else:
                    threading.Event().wait(0.05)
            std_out_reader.close()
            std_err_reader.close()
            os.remove(file.name)

        self.running = threading.Thread(target=runnable)
        self.running.start()
        threading.Thread(target=reader).start()

    def get_running_thread(self):
        return self.running

    @staticmethod
    def execute_static(command, dir=None):
        executive = Executive()
        if dir and dir.exists() and dir.is_dir():
            executive.set_cwd(dir)
        executive.execute(command)
        return executive.get_running_thread()

    @staticmethod
    def execute_static_with_connection(command, dir, connection, request_message):
        executive = Executive()
        if dir and dir.exists() and dir.is_dir():
            executive.set_cwd(dir)
        executive.set_request_message(request_message)
        executive.set_connection(connection)
        executive.execute(command)
        return executive.get_running_thread()

    @staticmethod
    def execute_static_with_params(command, dir, connection, user_id, message, filepath):
        executive = Executive()
        if dir and dir.exists() and dir.is_dir():
            executive.set_cwd(dir)
        executive.set_required_message_content(message)
        executive.set_filepath(filepath)
        executive.set_user_id(user_id)
        executive.set_connection(connection)
        executive.execute(command)