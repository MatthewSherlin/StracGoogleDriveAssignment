import unittest
import tempfile
import os
from app import app as flask_app
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = flask_app
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

        # Create a temporary file for testing
        cls.test_file_path = tempfile.mktemp()
        cls.test_file_name = 'testfile.txt'
        with open(cls.test_file_path, 'w') as f:
            f.write('This is a test file.')

        # Load credentials for Google Drive
        cls.credentials = Credentials.from_authorized_user_file('json/token.json')
        cls.service = build('drive', 'v3', credentials=cls.credentials)

    def setUp(self):
        # Initialize session for each test
        with self.client.session_transaction() as sess:
            sess['credentials'] = {
                'token': self.credentials.token,
                'refresh_token': self.credentials.refresh_token,
                'token_uri': self.credentials.token_uri,
                'client_id': self.credentials.client_id,
                'client_secret': self.credentials.client_secret,
                'scopes': self.credentials.scopes
            }

    def get_file_id(self, file_name):
        # Get file ID from file name
        results = self.service.files().list(q=f"name='{file_name}'", spaces='drive',
                                            fields='files(id, name)').execute()
        items = results.get('files', [])
        if items:
            return items[0]['id']
        return None

    # Test file upload
    def test_upload_file(self):
        with open(self.test_file_path, 'rb') as f:
            response = self.client.post('/upload', data={'file': (f, self.test_file_name)})
        # Check redirect
        self.assertEqual(response.status_code, 302)  
    
    #Test file download
    def test_download_file(self):
        
        self.test_upload_file()
        file_id = self.get_file_id(self.test_file_name)
        self.assertIsNotNone(file_id, "File ID should not be None")

        # Ensure 200 code
        response = self.client.get(f'/download/{file_id}')
        self.assertEqual(response.status_code, 200)

        with open(f'./{self.test_file_name}', 'wb') as f:
            f.write(response.data)

        self.assertTrue(os.path.exists(self.test_file_name))

        os.remove(self.test_file_name)

    # Test delete file        
    def test_delete_file(self):
        self.test_upload_file()
        file_id = self.get_file_id(self.test_file_name)
        self.assertIsNotNone(file_id, "File ID should not be None")

        response = self.client.post(f'/delete/{file_id}')
        self.assertEqual(response.status_code, 302)

    # Clean temporary files
    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_file_path):
            os.remove(cls.test_file_path)

if __name__ == '__main__':
    unittest.main()
