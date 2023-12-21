import os
import subprocess
from threading import Thread
from typing import List
from message import Message


class Wormhole:
    cwd = os.getcwd()

    def __init__(self):
        pass

    @staticmethod
    def check_filename(existing_filenames: List[str], filename: str) -> str:
        if filename in existing_filenames:
            while True:
                if filename not in existing_filenames:
                    return filename
                filename_split = filename.split(".")
                name, file_format = filename_split[0], filename_split[1]
                try:
                    last = str(name[-1])
                    file_num = int(last) + 1
                    filename = f"{name[:-2]}-{file_num}.{file_format}"
                except ValueError:
                    filename = f"{name}-2.{file_format}"

        return filename

    @staticmethod
    def receive(connection, request_message, command, filename, sender_id):
        command_builder = [command, "--accept-file"]
        received_dir = os.path.join(Wormhole.cwd, "received-files")
        original_filename = filename

        # check if received-files directory exists, create if it does not
        if not os.path.exists(received_dir):
            os.mkdir(received_dir)

        # to bypass "yes" input for wormhole receive
        command_builder.append(f"-o {filename}")

        # check if filename already exists
        existing_filenames = os.listdir(received_dir)
        filename = Wormhole.check_filename(existing_filenames, filename)

        # receive the file as the filename
        command_builder.append(f"-o {filename}")

        running = Wormhole.execute(command_builder, received_dir, connection, request_message)
        return Wormhole.ReceiveObj(filename, running, sender_id, original_filename)

    @staticmethod
    def send(connection, user_id, message, filepath):
        command = f"wormhole send {filepath}"
        Wormhole.execute(command, Wormhole.cwd, connection, user_id, message, filepath)

    @staticmethod
    def execute(command, working_directory, connection=None, user_id=None, message=None, filepath=None):
        def run_thread():
            process = subprocess.Popen(command, cwd=working_directory, shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, text=True)
            process.communicate()
            process.stdout.close()
            process.stderr.close()

            if connection is not None and user_id is not None and message is not None and filepath is not None:
                connection.direct(message, user_id, f"File '{os.path.basename(filepath)}' sent successfully.")

        thread = Thread(target=run_thread)
        thread.start()
        return thread

    class ReceiveObj:

        def __init__(self, new_filename, running, source_user_id, original_filename):
            self.new_filename = new_filename
            self.running = running
            self.source_user_id = source_user_id
            self.original_filename = original_filename

        def get_new_filename(self):
            return self.new_filename

        def get_running_thread(self):
            return self.running

        def get_source_user_id(self):
            return self.source_user_id

        def get_original_filename(self):
            return self.original_filename

        def get_file_format(self):
            return self.new_filename.split(".")[1]
