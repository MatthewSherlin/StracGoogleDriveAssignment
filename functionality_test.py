import unittest
import tempfile
import os
from drive import authenticate, list_files, upload_file, download_file, delete_file

class TestGoogleDriveFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.creds = authenticate()
        cls.test_file_name = 'testfile.txt'

        # Create a temporary file for testing
        cls.test_file_path = tempfile.mktemp()
        with open(cls.test_file_path, 'w') as f:
            f.write('This is a test file.')

        cls.downloaded_file_path = tempfile.mktemp()
        cls.file_id = None

    def test_upload_file(self):
        upload_file(self.creds, self.test_file_name, self.test_file_path)
        
        files = list_files(self.creds)
        if files is None:
            self.fail("Failed to retrieve files.")
        
        for file in files:
            if file['name'] == self.test_file_name:
                self.file_id = file['id']
                break
        
        self.assertIsNotNone(self.file_id, "File ID should not be None.")

    def test_download_file(self):
        # Make sure file is uploaded
        if self.file_id is None:
            self.test_upload_file()
        
        download_file(self.creds, self.file_id, self.downloaded_file_path)
        self.assertTrue(os.path.exists(self.downloaded_file_path), "Downloaded file should exist.")

    def test_delete_file(self):
        if self.file_id is None:
            self.test_upload_file()
        
        delete_file(self.creds, self.file_id)
        
        files = list_files(self.creds)
        if files is None:
            self.fail("Failed to retrieve files.")
        
        for file in files:
            if file['id'] == self.file_id:
                self.fail("File should have been deleted.")

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_file_path):
            os.remove(cls.test_file_path)
        
        if os.path.exists(cls.downloaded_file_path):
            os.remove(cls.downloaded_file_path)
        
        files = list_files(cls.creds)
        if files is None:
            cls.fail("Failed to retrieve files during tear down.")
        
        for file in files:
            if file['id'] == cls.file_id:
                delete_file(cls.creds, file['id'])

if __name__ == '__main__':
    unittest.main()
