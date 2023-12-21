import json
from datetime import datetime
from file_data import FileData  # Assuming you have a FileData class in a separate file
from pathlib import Path

class Metadata:
    def __init__(self, user_id, message_type):
        self.user_id = user_id
        self.message_type = message_type
        self.message_id = str(uuid.uuid4())
        self.data = []
        self.data_request_formats = []
        self.data_convert_formats = {}
        self.origin_message_id = ""
        self.source_user_id = ""
        self.timestamp = datetime.now().isoformat()

    def set_data(self, file_path):
        try:
            filename = file_path.name
            filesize = str(file_path.stat().st_size)
            self.data.append(FileData(filename, filesize))
        except (IOError, FileNotFoundError) as e:
            print(e)

    def set_data_request_formats(self, *wants):
        self.data_request_formats.extend(wants)

    def set_data_convert_formats(self, original, destination):
        self.data_convert_formats.setdefault(original, []).append(destination)

    def set_origin_message_id(self, origin_message_id):
        self.origin_message_id = origin_message_id

    def set_source_user_id(self, source_user_id):
        self.source_user_id = source_user_id

    def to_json(self):
        metadata_json = {
            'user_id': self.user_id,
            'message_type': self.message_type,
            'message_id': self.message_id,
            'metadata_filedata': self.data_to_json(),
            'data_request_formats': self.request_formats_to_json(),
            'data_convert_formats': self.convert_formats_to_json(),
            'origin_message_id': self.origin_message_id,
            'source_user_id': self.source_user_id,
            'timestamp': self.timestamp
        }
        return metadata_json

    def data_to_json(self):
        return [{'filename': file.get_file_name(), 'filesize': file.get_file_size()} for file in self.data]

    def convert_formats_to_json(self):
        return [{'original_format': original, 'destination_formats': destinations} for original, destinations in
                self.data_convert_formats.items()]

    def request_formats_to_json(self):
        return self.data_request_formats

    @classmethod
    def from_json(cls, metadata_json_obj):
        metadata = cls(metadata_json_obj['user_id'], metadata_json_obj['message_type'])
        metadata.message_id = metadata_json_obj['message_id']
        metadata.data = [FileData(file['filename'], file['filesize']) for file in metadata_json_obj['metadata_filedata']]
        metadata.data_request_formats = metadata_json_obj['data_request_formats']
        metadata.data_convert_formats = {entry['original_format']: entry['destination_formats'] for entry in
                                         metadata_json_obj['data_convert_formats']}
        metadata.origin_message_id = metadata_json_obj['origin_message_id']
        metadata.source_user_id = metadata_json_obj['source_user_id']
        metadata.timestamp = metadata_json_obj['timestamp']
        return metadata

    def __str__(self):
        return f"user_id: {self.user_id}, message_id: {self.message_id}, message_type: {self.message_type}\n" \
               f"data: {self.data}, data_convert_formats: {self.data_convert_formats}, " \
               f"data_request_formats: {self.data_request_formats}\n" \
               f"timestamp: {self.timestamp}, origin_message_id: {self.origin_message_id}, " \
               f"source_user_id: {self.source_user_id}"
