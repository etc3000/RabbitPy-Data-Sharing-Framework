from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List
from uuid import uuid4
from message import Message

@dataclass
class User:
    """
    The User class represents a user with various attributes and methods related to file conversion and messaging.
    """
    userID: str = field(default_factory=lambda: str(uuid4()))
    want: List[str] = field(default_factory=list)
    convert: Dict[str, List[str]] = field(default_factory=dict)
    filepaths: List[Path] = field(default_factory=list)
    receivedMessages: Dict[str, Message] = field(default_factory=dict)
    filesRequested: Dict[str, List[str]] = field(default_factory=dict)
    translationsRequested: Dict[str, List[str]] = field(default_factory=dict)
    requestMessage: Message = None

    def __init__(self, user_id):
        self.user_id = user_id
        self.want_formats = []

    def add_want_format(self, format):
        self.want_formats.append(format)

    def has_want_format(self, format):
        return format in self.want_formats
    @property
    def want_formats(self) -> List[str]:
        return self.want

    @want_formats.setter
    def want_formats(self, value):
        self.want = value

    @property
    def convert_formats(self) -> Dict[str, List[str]]:
        return self.convert

    @convert_formats.setter
    def convert_formats(self, value):
        self.convert = value

    def get_destination_formats(self, original_format) -> List[str]:
        return self.convert.get(original_format, [])

    @property
    def all_filepaths(self) -> List[Path]:
        return self.filepaths

    @property
    def all_messages(self) -> Dict[str, Message]:
        return self.receivedMessages

    def get_message(self, message_id) -> Message:
        return self.receivedMessages.get(message_id)

    @property
    def user_id(self) -> str:
        return self.userID

    @user_id.setter
    def user_id(self, value):
        self.userID = value

    def get_files_requested(self, source_user_id) -> List[str]:
        return self.filesRequested.get(source_user_id, [])

    @property
    def current_request_message(self) -> Message:
        return self.requestMessage

    def get_translation_format_requests(self, filename) -> List[str]:
        return self.translationsRequested.get(filename, [])