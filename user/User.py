from pathlib import Path
from uuid import uuid4
from typing import List, Dict

from ..message import Message

class User:
    """
    The User class represents a user with various attributes and methods related to file conversion and messaging.

    Attributes:
        userID (str): The unique identifier for the user.
        want (List[str]): The list of formats the user wants to convert files to.
        convert (Dict[str, List[str]]): The dictionary mapping original formats to destination formats the user can convert.
        filepaths (List[Path]): The list of filepaths the user has.
        receivedMessages (Dict[str, Message]): The dictionary of received messages, keyed by message ID.
        filesRequested (Dict[str, List[str]]): The dictionary of files requested by the user, keyed by source user ID.
        translationsRequested (Dict[str, List[str]]): The dictionary of translation requests, keyed by filename.
        requestMessage (Message): The current request message of the user.
    """

    def __init__(self):
        """
        Initializes the User class with default values for its attributes.
        """
        self.userID = str(uuid4())
        self.want = []
        self.convert = {}
        self.filepaths = []
        self.receivedMessages = {}  # Key: MessageID, Value: Message
        self.filesRequested = {}  # Key: SourceUserID, Value: [Filenames]
        self.translationsRequested = {}  # Key: Filename, Value: [DestinationFormats]
        self.requestMessage = None

    def add_want(self, *want_formats):
        """
        Adds the specified formats to the user's want list.

        Args:
            *want_formats: The formats to add to the user's want list.
        """
        self.want.extend(want_formats)

    def add_convert(self, original, destination):
        """
        Adds a conversion from the original format to the destination format to the user's convert dictionary.

        Args:
            original (str): The original format.
            destination (str): The destination format.
        """
        self.convert.setdefault(original, []).append(destination)

    def add_filepaths(self, filepath):
        """
        Adds the specified filepath to the user's filepaths list.

        Args:
            filepath (str): The filepath to add to the user's filepaths list.
        """
        valid_path = Path(filepath)
        self.filepaths.append(valid_path)

    def add_received_message(self, message_id, message):
        """
        Adds the specified message to the user's receivedMessages dictionary.

        Args:
            message_id (str): The ID of the message.
            message (Message): The message to add to the user's receivedMessages dictionary.
        """
        self.receivedMessages[message_id] = message

    def add_file_request(self, source_user_id, filename):
        """
        Adds a file request for the specified filename from the specified source user to the user's filesRequested dictionary.

        Args:
            source_user_id (str): The ID of the source user.
            filename (str): The filename of the file to request.
        """
        self.filesRequested.setdefault(source_user_id, []).append(filename)

    def remove_file_request(self, source_user_id, filename):
        """
        Removes a file request for the specified filename from the specified source user from the user's filesRequested dictionary.

        Args:
            source_user_id (str): The ID of the source user.
            filename (str): The filename of the file to remove the request for.
        """
        self.filesRequested[source_user_id].remove(filename)
        if not self.filesRequested[source_user_id]:
            del self.filesRequested[source_user_id]

    def add_request_message(self, message):
        """
        Sets the user's requestMessage attribute to the specified message.

        Args:
            message (Message): The message to set as the user's requestMessage.
        """
        self.requestMessage = message

    def remove_request_message(self):
        """
        Removes the user's current request message.
        """
        self.requestMessage = None

    def add_translation_request(self, filename, destination_format):
        """
        Adds a translation request for the specified filename to the specified destination format to the user's translationsRequested dictionary.

        Args:
            filename (str): The filename of the file to request a translation for.
            destination_format (str): The destination format to request a translation to.
        """
        self.translationsRequested.setdefault(filename, []).append(destination_format)

    def remove_translation_request(self, filename, destination_format):
        """
        Removes a translation request for the specified filename to the specified destination format from the user's translationsRequested dictionary.

        Args:
            filename (str): The filename of the file to remove the translation request for.
            destination_format (str): The destination format to remove the translation request for.
        """
        if filename in self.translationsRequested:
            self.translationsRequested[filename].remove(destination_format)
            if not self.translationsRequested[filename]:
                del self.translationsRequested[filename]

    def get_want_formats(self) -> List[str]:
        """
        Gets the user's want list.

        Returns:
            List[str]: The user's want list.
        """
        return self.want

    def get_convert_formats(self) -> Dict[str, List[str]]:
        """
        Gets the user's convert dictionary.

        Returns:
            Dict[str, List[str]]: The user's convert dictionary.
        """
        return self.convert

    def get_destination_formats(self, original_format) -> List[str]:
        """
        Gets the destination formats for the specified original format from the user's convert dictionary.

        Args:
            original_format (str): The original format to get the destination formats for.

        Returns:
            List[str]: The destination formats for the specified original format.
        """
        return self.convert.get(original_format, [])

    def get_filepaths(self) -> List[Path]:
        """
        Gets the user's filepaths list.

        Returns:
            List[Path]: The user's filepaths list.
        """
        return self.filepaths

    def get_all_messages(self) -> Dict[str, Message]:
        """
        Gets the user's receivedMessages dictionary.

        Returns:
            Dict[str, Message]: The user's receivedMessages dictionary.
        """
        return self.receivedMessages

    def get_message(self, message_id) -> Message:
        """
        Gets the message with the specified ID from the user's receivedMessages dictionary.

        Args:
            message_id (str): The ID of the message to get.

        Returns:
            Message: The message with the specified ID.
        """
        return self.receivedMessages.get(message_id)

    def get_user_id(self) -> str:
        """
        Gets the user's ID.

        Returns:
            str: The user's ID.
        """
        return self.userID

    def get_files_requested(self, source_user_id) -> List[str]:
        """
        Gets the filenames of the files requested by the user from the specified source user.

        Args:
            source_user_id (str): The ID of the source user to get the filenames of the files requested from.

        Returns:
            List[str]: The filenames of the files requested by the user from the specified source user.
        """
        return self.filesRequested.get(source_user_id, [])

    def get_request_message(self) -> Message:
        """
        Gets the user's current request message.

        Returns:
            Message: The user's current request message.
        """
        return self.requestMessage

    def get_translation_format_requests(self, filename) -> List[str]:
        """
        Gets the destination formats for the specified filename from the user's translationsRequested dictionary.

        Args:
            filename (str): The filename to get the destination formats for.

        Returns:
            List[str]: The destination formats for the specified filename.
        """
        return self.translationsRequested.get(filename, [])