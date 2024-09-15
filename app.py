from flask import Flask, redirect, request, session, url_for, render_template, send_from_directory
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import tempfile
import drive

app = Flask(__name__)
app.secret_key = 'testing_key'
SCOPES = ['https://www.googleapis.com/auth/drive']

# Start OAuth authorization flow
@app.route('/authorize')
def authorize():
    flow = InstalledAppFlow.from_client_secrets_file(
        'json/client_secret.json',
        SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    authorization_url, _ = flow.authorization_url(access_type='offline', prompt='consent')
    return redirect(authorization_url)

# Handle OAuth callback
@app.route('/oauth2callback')
def oauth2callback():
    flow = InstalledAppFlow.from_client_secrets_file(
        'json/client_secret.json',
        SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    session['credentials'] = drive.credentials_to_dict(credentials)
    return redirect(url_for('index'))

# Display file list or redirect to authorization
@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect(url_for('authorize'))
    
    credentials = Credentials.from_authorized_user_info(session['credentials'])
    files = drive.list_files(credentials)
    return render_template('index.html', files=files)

# Upload a file to Google Drive
@app.route('/upload', methods=['POST'])
def upload():
    if 'credentials' not in session:
        return redirect(url_for('authorize'))
    
    file = request.files['file']
    if file:
        file_path = os.path.join(tempfile.gettempdir(), file.filename)
        file.save(file_path)
        credentials = Credentials.from_authorized_user_info(session['credentials'])
        drive.upload_file(credentials, file.filename, file_path)
        os.remove(file_path)
        return redirect(url_for('index'))
    return 'No file uploaded.'

# Download a file from Google Drive
@app.route('/download/<file_id>', methods=['GET'])
def download(file_id):
    if 'credentials' not in session:
        return redirect(url_for('authorize'))
    
    credentials = Credentials.from_authorized_user_info(session['credentials'])
    temp_file_path = os.path.join(tempfile.gettempdir(), file_id)
    drive.download_file(credentials, file_id, temp_file_path)
    
    return send_from_directory(directory=tempfile.gettempdir(), path=file_id, as_attachment=True)

# Delete a file from Google Drive
@app.route('/delete/<file_id>', methods=['POST'])
def delete(file_id):
    if 'credentials' not in session:
        return redirect(url_for('authorize'))
    
    credentials = Credentials.from_authorized_user_info(session['credentials'])
    drive.delete_file(credentials, file_id)
    
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(ssl_context='adhoc', debug=True)
