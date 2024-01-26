import os
import threading
from pathlib import Path

from rabbitmq.RabbitMQConnection import RabbitMQConnection  # Assuming you have a RabbitMQConnection class in a rabbitmq module
from user import User  # Assuming you have a User class in a user module
from message import Message, ProcessMessage, Wormhole  # Assuming you have these classes in a message module
from logging import Log  # Assuming you have a Log class in a logging module

class ResearchAPI:
    """
    The main class for the Research API. It handles user interactions, file management, and messaging.
    """
    def __init__(self, log_type, log_level):
        """
        Initialize the ResearchAPI instance.

        :param log_type: The type of logging to be used.
        :param log_level: The level of logging to be used.
        """
        Log.setOutput(log_type, log_level)
        self.user = User()
        self.connection = None
        self.received_filename = None

    def add_want_formats(self, *want_formats):
        """
        Add desired formats to the user's profile.

        :param want_formats: The formats the user wants to add.
        """
        self.user.add_want(want_formats)

    def add_file(self, filepath):
        """
        Add a file to the user's profile and announce it to the network.

        :param filepath: The path of the file to be added.
        """
        file = Path(filepath)
        if not file.exists():
            Log.error(f"Filepath does not exist for: '{filepath}'", "add_file")
            return
        self.user.add_filepaths(filepath)
        if self.connection is None:
            self.connect()
            if self.connection is None:
                return

        announce_data = Message(self.user.get_user_id(), Constants.ANNOUNCE_MESSAGE)
        for path in self.user.get_filepaths():
            announce_data.add_file_path(str(path))
        announce_data.add_content("I have data.")
        self.connection.announce(announce_data)

    def add_convert_format(self, original_format, destination_format):
        """
        Add a conversion format to the user's profile.

        :param original_format: The original format of the file.
        :param destination_format: The format to convert the file to.
        """
        self.user.add_convert(original_format, destination_format)

    def connect(self, uri=""):
        """
        Connect to the RabbitMQ server.

        :param uri: The URI of the RabbitMQ server.
        """
        self.connection = RabbitMQConnection(self.user, uri)
        if self.connection is None:
            return

    def start_listening(self):
        """
        Start listening for messages from the RabbitMQ server.
        """
        if self.connection is None or self.connection.get_channel() is None:
            return
        else:
            MessageThread(self).start()
            Log.other(" [*] Begin listening to RabbitMQ server.")

    def get_received_file(self):
        """
        Get the received file from the received-files directory.

        :return: The path and format of the received file.
        """
        cwd = os.getcwd()
        received_files_dir = Path(cwd, "received-files")

        if self.received_filename and received_files_dir.exists():
            file = Path(received_files_dir, self.received_filename)
            self.received_filename = None
            return [str(file), file.name.split(".")[1]]
        return [None, None]


class MessageThread(threading.Thread):
    """
    A thread for processing messages from the RabbitMQ server.
    """
    def __init__(self, research_api):
        """
        Initialize the MessageThread instance.

        :param research_api: The ResearchAPI instance to use for processing messages.
        """
        super(MessageThread, self).__init__()
        self.research_api = research_api
        self.channel = research_api.connection.get_channel()
        self.queue_name = research_api.connection.get_queue_name()

    def run(self):
        """
        Start the thread and begin processing messages.
        """
        try:
            deliver_callback = lambda consumer_tag, delivery: self.process(delivery)
            self.channel.basic_consume(self.queue_name, True, deliver_callback, lambda consumer_tag: None)
        except Exception as e:
            Log.error(str(e), self.__class__.__name__)

    def process(self, delivery):
        """
        Process a message from the RabbitMQ server.

        :param delivery: The message to be processed.
        """
        message = delivery.body.decode('utf-8')
        self.research_api.process(message)


# Assuming you have Constants class defined elsewhere
class Constants:
    """
    A class for storing constant values.
    """
    ANNOUNCE_MESSAGE = "announce_data"
    CAN_TRANSLATE = "can_translate"
    REQUEST_DATA = "request_data"
    SENT_DATA = "sent_data"
    METADATA = "metadata"
    USER_ID = "user_id"
    MESSAGE_ID = "message_id"
    MESSAGE_TYPE = "message_type"
    METADATA_FILEDATA = "data"
    DATA_CONVERT_FORMATS = "data_convert_formats"
    DATA_REQUEST_FORMATS = "data_request_formats"
    ORIGIN_MESSAGE_ID = "origin_message_id"
    SOURCE_USER_ID = "source_user_id"
    TIMESTAMP = "time_stamp"
    ORIGINAL_FORMAT = "original_format"
    DESTINATION_FORMATS = "destination_formats"
    FILENAME = "filename"
    FILESIZE = "filesize"
    CONTENT = "content"
    RABBITMQ_URI = "amqps://crnulcjb:jTi5qkc_4BJQy-J4fmMk6CEJn1_phN3x@shark.rmq.cloudamqp.com/crnulcjb"