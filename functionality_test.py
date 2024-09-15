import unittest
import tempfile
import os
from drive import authenticate, list_files, upload_file, download_file, delete_file

class TestGoogleDriveFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.creds = authenticate()
        cls.test_file_name = 'testfile.txt'

        # Create a temporary file for uploading
        cls.test_file_path = tempfile.mktemp()
        with open(cls.test_file_path, 'w') as f:
            f.write('This is a test file.')

        # Create a temporary file for downloading
        cls.downloaded_file_path = tempfile.mktemp()

        cls.file_id = None

    def test_upload_file(self):
        # Upload the file
        upload_file(self.creds, self.test_file_name, self.test_file_path)
        
        # Verify the file is uploaded by listing files and checking for the file ID
        files = list_files(self.creds)
        if files is None:
            self.fail("Failed to retrieve files from Google Drive.")
        
        for file in files:
            if file['name'] == self.test_file_name:
                self.file_id = file['id']
                break
        
        self.assertIsNotNone(self.file_id, "File ID should not be None.")

    def test_download_file(self):
        # Ensure the file is uploaded first
        if self.file_id is None:
            self.test_upload_file()  # Upload the file if not uploaded already
        
        # Download the file
        download_file(self.creds, self.file_id, self.downloaded_file_path)
        
        # Verify the file was downloaded
        self.assertTrue(os.path.exists(self.downloaded_file_path), "Downloaded file should exist.")

    def test_delete_file(self):
        # Ensure the file is uploaded first
        if self.file_id is None:
            self.test_upload_file()  # Upload the file if not uploaded already
        
        # Delete the file
        delete_file(self.creds, self.file_id)
        
        # Verify file deletion
        files = list_files(self.creds)
        if files is None:
            self.fail("Failed to retrieve files from Google Drive.")
        
        for file in files:
            if file['id'] == self.file_id:
                self.fail("File should have been deleted.")

    @classmethod
    def tearDownClass(cls):
        # Clean up test files
        if os.path.exists(cls.test_file_path):
            os.remove(cls.test_file_path)
        
        if os.path.exists(cls.downloaded_file_path):
            os.remove(cls.downloaded_file_path)
        
        # Optionally list files to ensure clean-up
        files = list_files(cls.creds)
        if files is None:
            cls.fail("Failed to retrieve files from Google Drive during tear down.")
        
        for file in files:
            if file['id'] == cls.file_id:
                delete_file(cls.creds, file['id'])

if __name__ == '__main__':
    unittest.main()
