## Strac Google Drive Integrated Application 

This simple tool was developed for Strac take home exam.

This application integrates with the Google Drive API to provide functionalities for listing, uploading, downloading, and deleting files. The app is built using Python, Flask, Google Drive’s API for seamless file management.

The application authenticates the users with OAuth 2.0 and allows for simple maniuplation of the Google Drive.


## Full Installation

Getting started:

Clone the Repo

```
git clone https://github.com/MatthewSherlin/Strac_GoogleDrive.git
```

Create and activate a virtual environment
```
py -m venv venv
venv\Scripts\activate
```
Install all necessary dependencies using requirement.txt
```
pip install -r requirements.txt
```
Configure your API
* Create a json/ directory in the project root.
* Place your client_secret.json and token.json files in the json/ directory. These files are essential for authenticating with Google Drive.

In production environment, configuring your secret key for Flask would be an important step, however for simplicity and just testing purposes, the secret key is initialized.
## Running the project

To run the main driver of the project
```
py app.py
```
This will run the project in https because this is a requirement for OAuth 2.0 due to security reasons.
The server will start up on https://127.0.0.1:5000/. Open this URL in your web browser to use the application.



## Assumptions and Design Decisions
* The application relies on Google Drive API for file operations. Ensure that your Google Cloud project has the necessary API enabled and credentials properly configured.
* The Flask application secret key is stored typically in a config.json file for security reasons. The design was made quite simple and less secure because of the testing environment and timing. If the application was planned for production environment, things such as this would be much more secure.
* The ignoring of the secret files requires users to follow the same naming convention.
