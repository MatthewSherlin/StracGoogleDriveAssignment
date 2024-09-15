from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import os


SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    creds = None
    if os.path.exists('json/token.json'):
        creds = Credentials.from_authorized_user_file('json/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'json/client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('json/token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def list_files(creds):
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(pageSize=10, fields="files(id, name)").execute()
    items = results.get('files', [])
    return items

def upload_file(creds, file_name, file_path):
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, mimetype='application/octet-stream')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'File ID: {file.get("id")}')

def download_file(creds, file_id, file_path):
    service = build('drive', 'v3', credentials=creds)
    request = service.files().get_media(fileId=file_id)
    with open(file_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()

def delete_file(creds, file_id):
    service = build('drive', 'v3', credentials=creds)
    service.files().delete(fileId=file_id).execute()
    print(f'File {file_id} deleted.')

def credentials_to_dict(creds):
    return {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }
