from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
from random import randint
import subprocess
import argparse
import fileinput
import time
from googleapiclient.errors import HttpError
import os, pickle
# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/iam',
    'https://www.googleapis.com/auth/cloudplatformprojects'
    ]

"""Shows basic usage of the Drive v3 API.
Prints the names and ids of the first 10 files the user has access to.
"""
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as t:
        creds = pickle.load(t)    

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_console()
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    with open('token.pickle', 'wb') as t:
        pickle.dump(creds, t)
        
service = build('drive', 'v3', credentials=creds)
print('ВЫполнено')

