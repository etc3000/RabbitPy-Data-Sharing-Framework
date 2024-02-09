import os
import json
from typing import List, Dict, Union, Tuple
from ..message import MagicWormhole, Message, FileData
from ..rabbitmq import RabbitMQConnection
from ..user import User
from ..constants import Constants
from ..logging import Log


class ProcessMessage:
    """
    The ProcessMessage class is responsible for processing messages received from the RabbitMQ server.

    Attributes:
        user (User): The user who is processing the message.
        connection (RabbitMQConnection): The connection to the RabbitMQ server.
        message (str): The message to be processed.
    """

    def __init__(self, user: User, connection: RabbitMQConnection, message: str) -> None:
        """
        Initializes the ProcessMessage class with the user, connection, and message.

        Args:
            user (User): The user who is processing the message.
            connection (RabbitMQConnection): The connection to the RabbitMQ server.
            message (str): The message to be processed.
        """
        self.user = user
        root = json.loads(message)
        metadata = root[Constants.METADATA]

        # Ignore messages current user sent
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
        """
        Processes the message.

        Returns:
            Union[Wormhole.ReceiveObj, None]: The received object if the message type is "sent_data", None otherwise.
        """
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
        """
        Checks if the user has requested data and sends it if they have.

        Args:
            filepath (str): The path to the file.
        """
        if self.message_type == Constants.REQUEST_DATA:
            Wormhole.send(self.connection, self.user_id, self.message, filepath)
        elif self.message_type == Constants.CAN_TRANSLATE:
            self.want_converted_data()

    def wants_and_does_not_have_data(self) -> None:
        """
        Checks if the user wants data and does not have it, and requests it if they do.
        """
        if self.message_type == Constants.ANNOUNCE_MESSAGE:
            self.want_data(False)
        elif self.message_type == Constants.CAN_TRANSLATE:
            self.want_converted_data()

    def can_convert_data(self) -> None:
        """
        Checks if the user can convert data and requests it if they can.
        """
        if self.message_type == Constants.ANNOUNCE_MESSAGE:
            self.convert_data_announcement()
        elif self.message_type == Constants.REQUEST_DATA:
            self.want_data(True)

    def want_data(self, for_convert: bool) -> None:
        """
        Checks if the user wants data and requests it if they do.

        Args:
            for_convert (bool): True if the user wants to convert the data, False otherwise.
        """
        request_want_formats = self.want_formats
        data = self.message.get_file_data()
        request_message_id = self.message_id
        origin_sender_id = self.sender_id

        if for_convert:
            want_args = self.get_want_args()
            if None in want_args:
                return
            request_want_formats, data, request_message_id, origin_sender_id = want_args

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

    def get_want_args(self) -> Union[Tuple[List[str], List[FileData], str, str], Tuple[None, None, None, None]]:
        """
        Gets the arguments for the want request.

        Returns:
            Union[Tuple[List[str], List[FileData], str, str], Tuple[None, None, None, None]]: The arguments for the want request if they exist, None otherwise.
        """
        request_formats = self.message.get_request_formats()
        new_wanted_formats = []

        for want in self.want_formats:
            for key, dest_formats in self.convert_formats.items():
                if request_formats is not None and any(format in dest_formats for format in request_formats):
                    new_wanted_formats.append(key)

        origin_message_id = self.message.get_origin_message_id()
        origin_message = self.user.get_message(origin_message_id)

        if origin_message is None:
            return None, None, None, None

        return new_wanted_formats, origin_message.get_file_data(), origin_message_id, origin_message.get_sender_id()

    def convert_data_announcement(self) -> None:
        """
        Announces that the user can convert data.
        """
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

    def want_converted_data(self) -> None:
        """
        Checks if the user wants converted data and requests it if they do.
        """
        announced_convertable_formats = self.message.get_convert_formats()
        found_format = False
        request_format = None

        for want in self.want_formats:
            for dest_formats in announced_convertable_formats.values():
                if any(want in dest_format for dest_format in dest_formats):
                    request_format = want
                    found_format = True
                    break
            if found_format:
                break

        if self.message.get_file_data():
            filename = self.message.get_file_data()[0].get_file_name()
            already_requested = filename in self.user.get_translation_format_requests(
                filename) if self.user.get_translation_format_requests(filename) is not None else False

            if request_format and not already_requested:
                request_message = Message(self.user_id, Constants.REQUEST_DATA)
                for file_data in self.message.get_file_data():
                    request_message.request_file(file_data)
                request_message.add_request_formats(request_format)
                request_message.add_origin_message_id(self.message.get_origin_message_id())
                request_message.add_source_user_id(self.message.get_source_user_id())
                request_message.add_content(f"Requesting data to be converted to {request_format}")
                self.connection.direct(request_message, self.sender_id)
                self.user.add_translation_request(filename, request_format)

    def get_filepath(self) -> Union[str, None]:
        """
        Gets the file path.

        Returns:
            Union[str, None]: The file path if it exists, None otherwise.
        """
        for path in self.filepaths:
            filename = os.path.basename(path)
            for file_data in self.message.get_file_data():
                if file_data.get_file_name() == filename:
                    return path

        return None
