import os
import subprocess
import threading
import tempfile
from pathlib import Path
from ..message import Message
from ..rmq import RabbitMQConnection
from ..my_logging import Log

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
        process = subprocess.Popen(["bash", file.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                   shell=False)
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
