import os
import threading

from pathlib import Path
from ..user import User
from ..message import Message, ProcessMessage, MagicWormhole
from ..my_logging import Log
import pika


class ResearchAPI:
    """
    The main class for the Research API. It handles user interactions, file management, and messaging.
    """

    def __init__(self, log_type, log_level):
        Log.setOutput(log_type, log_level)
        self.user = User()
        self.connection = None
        self.received_filename = None

    def add_want_formats(self, *want_formats):
        self.user.add_want(want_formats)

    def add_file(self, filepath):
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
        self.connection.basic_publish(exchange='', routing_key='announce', body=announce_data.to_json())

    def add_convert_format(self, original_format, destination_format):
        self.user.add_convert(original_format, destination_format)

    def connect(self, uri=""):
        self.connection = pika.BlockingConnection(pika.URLParameters(uri))
        self.channel = self.connection.channel()

    def start_listening(self):
        if self.connection is None or self.channel is None:
            return
        else:
            MessageThread(self).start()
            Log.other(" [*] Begin listening to RabbitMQ server.")

    def get_received_file(self):
        cwd = os.getcwd()
        received_files_dir = Path(cwd, "received-files")

        if self.received_filename and received_files_dir.exists():
            file = Path(received_files_dir, self.received_filename)
            self.received_filename = None
            return [str(file), file.name.split(".")[1]]
        return [None, None]


class MessageThread(threading.Thread):
    def __init__(self, research_api):
        super(MessageThread, self).__init__()
        self.research_api = research_api
        self.channel = research_api.channel

    def run(self):
        deliver_callback = lambda consumer_tag, delivery: self.process(delivery)
        self.channel.basic_consume(self.research_api.queue_name, True, deliver_callback, lambda consumer_tag: None)

    def process(self, delivery):
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