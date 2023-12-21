import unittest
from pathlib import Path
from message import Message
from user import User

class UserTest(unittest.TestCase):
    def setUp(self):
        self.user = User()

    def test_add_want(self):
        self.user.add_want("PDF", "DOCX")
        want_formats = self.user.get_want_formats()
        self.assertEqual(["PDF", "DOCX"], want_formats)

    def test_add_convert(self):
        self.user.add_convert("PDF", "TXT")
        self.user.add_convert("DOCX", "PDF")
        self.user.add_convert("DOCX", "TXT")

        self.assertEqual(["TXT"], self.user.get_destination_formats("PDF"))
        self.assertEqual(["PDF", "TXT"], self.user.get_destination_formats("DOCX"))
        self.assertIsNone(self.user.get_destination_formats("PPT"))  # Non-existing format

    def test_add_filepaths(self):
        self.user.add_filepaths("path/to/file1.txt")
        self.user.add_filepaths("path/to/file2.docx")

        filepaths = self.user.get_filepaths()
        self.assertEqual(2, len(filepaths))
        self.assertIn(Path("path/to/file1.txt"), filepaths)
        self.assertIn(Path("path/to/file2.docx"), filepaths)

    def test_add_received_message(self):
        message = Message("Hello, user!")
        self.user.add_received_message("123", message)

        self.assertEqual(message, self.user.get_message("123"))

    def test_add_file_request(self):
        self.user.add_file_request("sourceUser1", "file1.txt")
        self.user.add_file_request("sourceUser1", "file2.docx")
        self.user.add_file_request("sourceUser2", "file3.pdf")

        self.assertEqual(["file1.txt", "file2.docx"], self.user.get_files_requested("sourceUser1"))
        self.assertEqual(["file3.pdf"], self.user.get_files_requested("sourceUser2"))

    def test_remove_file_request(self):
        self.user.add_file_request("sourceUser1", "file1.txt")
        self.user.remove_file_request("sourceUser1", "file1.txt")

        self.assertIsNone(self.user.get_files_requested("sourceUser1"))

class TestUser:
    def main(self):
        api = ResearchAPI("console", "FINEST")
        api.connect()
        api.add_convert_format("csv", "png")
        api.add_want_formats("csv")
        api.start_listening()
        while True:
            received_file = api.get_received_file()
            received_filepath = received_file[0]
            received_file_format = received_file[1]
            if received_filepath is not None and received_file_format is not None and received_file_format == "csv":
                # do translation here

if __name__ == "__main__":
    unittest.main()
    test_user_instance = TestUser()
    test_user_instance.main()
