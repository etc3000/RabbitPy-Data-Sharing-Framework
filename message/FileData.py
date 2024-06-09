class FileData:
    """
    The FileData class represents a file with its name and size.
    Attributes:
        filename (str): The name of the file.
        filesize (int): The size of the file in bytes.
    """
    def __init__(self, filename, filesize):
        """
        Initializes the FileData class with the filename and filesize.
        Args:
            filename (str): The name of the file.
            filesize (int): The size of the file in bytes.
        """
        self.filename = filename
        self.filesize = filesize

    def get_file_name(self):
        """
        Gets the name of the file.
        Returns:
            str: The name of the file.
        """
        return self.filename

    def get_file_size(self):
        """
        Gets the size of the file.
        Returns:
            int: The size of the file in bytes.
        """
        return self.filesize

    def __str__(self):
        """
        Returns a string representation of the FileData object.
        Returns:
            str: A string representation of the FileData object in the format "(filename, filesize)".
        """
        return f"({self.filename}, {self.filesize})"