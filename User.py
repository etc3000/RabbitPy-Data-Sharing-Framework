from pathlib import Path
from uuid import uuid4
from typing import List, Dict

from message import Message

class User:
    def __init__(self):
        self.userID = str(uuid4())
        self.want = []
        self.convert = {}
        self.filepaths = []
        self.receivedMessages = {}  # Key: MessageID, Value: Message
        self.filesRequested = {}  # Key: SourceUserID, Value: [Filenames]
        self.translationsRequested = {}  # Key: Filename, Value: [DestinationFormats]
        self.requestMessage = None

    def add_want(self, *want_formats):
        self.want.extend(want_formats)

    def add_convert(self, original, destination):
        self.convert.setdefault(original, []).append(destination)

    def add_filepaths(self, filepath):
        valid_path = Path(filepath)
        self.filepaths.append(valid_path)

    def add_received_message(self, message_id, message):
        self.receivedMessages[message_id] = message

    def add_file_request(self, source_user_id, filename):
        self.filesRequested.setdefault(source_user_id, []).append(filename)

    def remove_file_request(self, source_user_id, filename):
        self.filesRequested[source_user_id].remove(filename)
        if not self.filesRequested[source_user_id]:
            del self.filesRequested[source_user_id]

    def add_request_message(self, message):
        self.requestMessage = message

    def remove_request_message(self):
        self.requestMessage = None

    def add_translation_request(self, filename, destination_format):
        self.translationsRequested.setdefault(filename, []).append(destination_format)

    def remove_translation_request(self, filename, destination_format):
        if filename in self.translationsRequested:
            self.translationsRequested[filename].remove(destination_format)
            if not self.translationsRequested[filename]:
                del self.translationsRequested[filename]

    def get_want_formats(self) -> List[str]:
        return self.want

    def get_convert_formats(self) -> Dict[str, List[str]]:
        return self.convert

    def get_destination_formats(self, original_format) -> List[str]:
        return self.convert.get(original_format, [])

    def get_filepaths(self) -> List[Path]:
        return self.filepaths

    def get_all_messages(self) -> Dict[str, Message]:
        return self.receivedMessages

    def get_message(self, message_id) -> Message:
        return self.receivedMessages.get(message_id)

    def get_user_id(self) -> str:
        return self.userID

    def get_files_requested(self, source_user_id) -> List[str]:
        return self.filesRequested.get(source_user_id, [])

    def get_request_message(self) -> Message:
        return self.requestMessage

    def get_translation_format_requests(self, filename) -> List[str]:
        return self.translationsRequested.get(filename, [])
