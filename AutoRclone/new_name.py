from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
from BIB_API import drive_ls , ls_files_dr_or_fold
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/cloud-platform",
          "https://www.googleapis.com/auth/iam"]


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    n=0
    for sps in drive_ls(service): 
       n+=1
       name_nd = sps.get('name')
       print('Старое имя ' + name_nd + '----  Новое ' + str(n))
       s_iddrive = sps.get('id') 
       new_grives = service.teamdrives().update(teamDriveId=s_iddrive, body={"name": n}).execute()
       print(new_grives)
    
if __name__ == '__main__':
    main()