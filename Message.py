import json
from metadata import Metadata  # Assuming you have a Metadata class in a separate file

class Message:
    def __init__(self, user_id, message_type):
        self.metadata = Metadata(user_id, message_type)
        self.content = None

    def add_file_path(self, file_path):
        try:
            valid_path = Path(file_path)
            self.metadata.set_data(valid_path)
        except (InvalidPathException, IOException) as e:
            print(e)

    def request_file(self, file_data):
        self.metadata.set_data(file_data)

    def add_request_formats(self, *wants):
        self.metadata.set_data_request_formats(wants)

    def add_request_formats_from_list(self, wants):
        for want in wants:
            self.metadata.set_data_request_formats(want)

    def add_convert_format(self, original_format, destination_format):
        self.metadata.set_data_convert_formats(original_format, destination_format)

    def add_origin_message_id(self, message_id):
        self.metadata.set_origin_message_id(message_id)

    def add_source_user_id(self, source_user_id):
        self.metadata.set_source_user_id(source_user_id)

    def add_content(self, content):
        self.content = content

    def to_json(self):
        message = {
            'metadata': self.metadata.to_json(),
            'content': self.content
        }
        return json.dumps(message)

    @classmethod
    def from_json(cls, message):
        root = json.loads(message)
        metadata_json = root['metadata']
        metadata = Metadata.from_json(metadata_json)
        content = root['content']
        return cls(metadata, content)

    def get_sender_id(self):
        return self.metadata.user_id

    def get_message_type(self):
        return self.metadata.message_type

    def get_message_id(self):
        return self.metadata.message_id

    def get_file_data(self):
        return self.metadata.data

    def get_request_formats(self):
        return self.metadata.data_request_formats

    def get_convert_formats(self):
        return self.metadata.data_convert_formats

    def get_origin_message_id(self):
        return self.metadata.origin_message_id

    def get_source_user_id(self):
        return self.metadata.source_user_id

    def __str__(self):
        return f"metadata = {self.metadata}, content = {self.content}\n"

    def get_metadata(self):
        return self.metadata

    def get_content(self):
        return self.content
