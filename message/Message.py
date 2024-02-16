import json
from pathlib import Path
from Metadata import *  # Assuming you have a Metadata class in a separate file
# import InvalidPathException, IOException


class Message:
    """
    The Message class represents a message with various attributes and methods related to file conversion and messaging.

    Attributes:
        metadata (Metadata): The metadata of the message.
        content (str): The content of the message.
    """

    def __init__(self, user_id, message_type):
        """
        Initializes the Message class with the user ID and message type.

        Args:
            user_id (str): The ID of the user.
            message_type (str): The type of the message.
        """
        self.metadata = Metadata(user_id, message_type)
        self.content = None

    def add_file_path(self, file_path):
        """
        Adds the specified file path to the message's metadata.

        Args:
            file_path (str): The file path to add to the message's metadata.
        """
        try:
            valid_path = Path(file_path)
            self.metadata.set_data(valid_path)
        except (InvalidPathException, IOException) as e:
            print(e)

    def request_file(self, file_data):
        """
        Requests a file by adding its data to the message's metadata.

        Args:
            file_data: The data of the file to request.
        """
        self.metadata.set_data(file_data)

    def add_request_formats(self, *wants):
        """
        Adds the specified formats to the message's metadata.

        Args:
            *wants: The formats to add to the message's metadata.
        """
        self.metadata.set_data_request_formats(wants)

    def add_request_formats_from_list(self, wants):
        """
        Adds the formats from the specified list to the message's metadata.

        Args:
            wants (list): The list of formats to add to the message's metadata.
        """
        for want in wants:
            self.metadata.set_data_request_formats(want)

    def add_convert_format(self, original_format, destination_format):
        """
        Adds a conversion from the original format to the destination format to the message's metadata.

        Args:
            original_format (str): The original format.
            destination_format (str): The destination format.
        """
        self.metadata.set_data_convert_formats(original_format, destination_format)

    def add_origin_message_id(self, message_id):
        """
        Adds the specified origin message ID to the message's metadata.

        Args:
            message_id (str): The origin message ID to add to the message's metadata.
        """
        self.metadata.set_origin_message_id(message_id)

    def add_source_user_id(self, source_user_id):
        """
        Adds the specified source user ID to the message's metadata.

        Args:
            source_user_id (str): The source user ID to add to the message's metadata.
        """
        self.metadata.set_source_user_id(source_user_id)

    def add_content(self, content):
        """
        Sets the content of the message.

        Args:
            content (str): The content to set.
        """
        self.content = content

    def to_json(self):
        """
        Converts the message to a JSON string.

        Returns:
            str: The JSON string representation of the message.
        """
        message = {
            'metadata': self.metadata.to_json(),
            'content': self.content
        }
        return json.dumps(message)

    @classmethod
    def from_json(cls, message):
        """
        Creates a Message object from a JSON string.

        Args:
            message (str): The JSON string representation of the message.

        Returns:
            Message: The Message object created from the JSON string.
        """
        root = json.loads(message)
        metadata_json = root['metadata']
        metadata = Metadata.from_json(metadata_json)
        content = root['content']
        return cls(metadata, content)

    def get_sender_id(self):
        """
        Gets the sender ID of the message.

        Returns:
            str: The sender ID of the message.
        """
        return self.metadata.user_id

    def get_message_type(self):
        """
        Gets the type of the message.

        Returns:
            str: The type of the message.
        """
        return self.metadata.message_type

    def get_message_id(self):
        """
        Gets the ID of the message.

        Returns:
            str: The ID of the message.
        """
        return self.metadata.message_id

    def get_file_data(self):
        """
        Gets the file data of the message.

        Returns:
            The file data of the message.
        """
        return self.metadata.data

    def get_request_formats(self):
        """
        Gets the request formats of the message.

        Returns:
            The request formats of the message.
        """
        return self.metadata.data_request_formats

    def get_convert_formats(self):
        """
        Gets the convert formats of the message.

        Returns:
            The convert formats of the message.
        """
        return self.metadata.data_convert_formats

    def get_origin_message_id(self):
        """
        Gets the origin message ID of the message.

        Returns:
            str: The origin message ID of the message.
        """
        return self.metadata.origin_message_id

    def get_source_user_id(self):
        """
        Gets the source user ID of the message.

        Returns:
            str: The source user ID of the message.
        """
        return self.metadata.source_user_id

    def __str__(self):
        """
        Returns a string representation of the message.

        Returns:
            str: A string representation of the message.
        """
        return f"metadata = {self.metadata}, content = {self.content}\n"

    def get_metadata(self):
        """
        Gets the metadata of the message.

        Returns:
            Metadata: The metadata of the message.
        """
        return self.metadata

    def get_content(self):
        """
        Gets the content of the message.

        Returns:
            str: The content of the message.
        """
        return self.content
