import os
import json
from typing import List, Dict, Union, Tuple
from .MagicWormhole import Wormhole
from ..message import MagicWormhole, Message, FileData
from ..rmq import RabbitMQConnection
from ..user import User
from ..constants import Constants
from ..my_logging import Log


class ProcessMessage:
    def __init__(self, user: User, connection: RabbitMQConnection, message: str) -> None:
        self.user = user
        root = json.loads(message)
        metadata = root[Constants.METADATA]
        if metadata[Constants.USER_ID] != user.get_user_id():
            self.message = Message(message)
            self.sender_id = self.message.get_sender_id()
            self.message_type = self.message.get_message_type()
            self.message_id = self.message.get_message_id()
            self.user_id = self.user.get_user_id()
            self.filepaths = self.user.get_filepaths()
            self.want_formats = self.user.get_want_formats()
            self.convert_formats = self.user.get_convert_formats()
            self.connection = connection

    def process(self) -> Union[Wormhole.ReceiveObj, None]:
        if self.message is not None:
            Log.received(f" [x] Received {self.message}")
            self.user.add_received_message(self.message_id, self.message)
            requested_filepath = self.get_filepath()
            if requested_filepath is not None:
                self.has_requested_data(requested_filepath)
            if not self.want_formats and requested_filepath is None:
                self.wants_and_does_not_have_data()
            if self.convert_formats:
                self.can_convert_data()
            if self.message_type == Constants.SENT_DATA:
                filename = self.message.get_file_data()[0].get_file_name()
                return Wormhole.receive(self.connection, self.user.get_request_message(), self.message.get_content(),
                                        filename, self.sender_id)
        return None

    def has_requested_data(self, filepath: str) -> None:
        if self.message_type == Constants.REQUEST_DATA:
            Wormhole.send(self.connection, self.user_id, self.message, filepath)

    def wants_and_does_not_have_data(self) -> None:
        if self.message_type == Constants.ANNOUNCE_MESSAGE:
            self.want_data(False)

    def can_convert_data(self) -> None:
        if self.message_type == Constants.ANNOUNCE_MESSAGE:
            self.convert_data_announcement()

    def want_data(self, for_convert: bool) -> None:
        request_want_formats = self.want_formats
        data = self.message.get_file_data()
        request_message_id = self.message_id
        origin_sender_id = self.sender_id

        for file_data in data:
            filename = file_data.get_file_name()
            file_format = filename.split(".")[1]

            already_requested = filename in self.user.get_files_requested(
                origin_sender_id) if self.user.get_files_requested(origin_sender_id) is not None else False

            if file_format in request_want_formats and not already_requested:
                request_message = Message(self.user_id, Constants.REQUEST_DATA)
                request_message.add_request_formats(request_want_formats)
                request_message.request_file(file_data)
                request_message.add_origin_message_id(request_message_id)
                request_message.add_source_user_id(origin_sender_id)
                request_message.add_content(f"Requesting file '{filename}'")
                self.connection.direct(request_message, origin_sender_id)
                self.user.add_file_request(origin_sender_id, filename)
                self.user.add_request_message(request_message)
                break

    def convert_data_announcement(self) -> None:
        announced_data = self.message.get_file_data()
        request_data = []
        convertable_formats = {}

        for file_data in announced_data:
            file_format = file_data.get_file_name().split(".")[1]
            if file_format in self.convert_formats:
                request_data.append(file_data)
                convertable_formats[file_format] = self.convert_formats[file_format]

        request_message = Message(self.user_id, Constants.CAN_TRANSLATE)

        for file_data in request_data:
            request_message.request_file(file_data)

        for original_format, dest_formats in convertable_formats.items():
            for dest_format in dest_formats:
                request_message.add_convert_format(original_format, dest_format)

        request_message.add_origin_message_id(self.message_id)
        request_message.add_source_user_id(self.sender_id)
        request_message.add_content(f"I can convert the data from {convertable_formats}")
        self.connection.announce(request_message)

    def get_filepath(self) -> Union[str, None]:
        for path in self.filepaths:
            filename = os.path.basename(path)
            for file_data in self.message.get_file_data():
                if file_data.get_file_name() == filename:
                    return path

        return None
