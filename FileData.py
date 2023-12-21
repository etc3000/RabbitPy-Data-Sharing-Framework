class FileData:
    def __init__(self, filename, filesize):
        self.filename = filename
        self.filesize = filesize

    def get_file_name(self):
        return self.filename

    def get_file_size(self):
        return self.filesize

    def __str__(self):
        return f"({self.filename}, {self.filesize})"
