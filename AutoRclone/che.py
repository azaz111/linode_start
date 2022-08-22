from time import sleep
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
from datetime import datetime
from BIB_API import  ls_files_dr_or_fold
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/cloud-platform",
          "https://www.googleapis.com/auth/iam"]


def drive_ls(service):  # Cписок всех дисков
    file_spis=[]
    page_token = None
    while True:
        lsvse=service.teamdrives().list(pageSize=100,
                                        pageToken=page_token).execute() 

        print(lsvse)
        for file in lsvse.get('teamDrives'):
            # Изменение процесса
            file_spis.append(file)
            # print(file.get('name'), file.get('id'))
        page_token = lsvse.get('nextPageToken', None)
        if page_token is None:
            break 
    return file_spis  



def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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
    return service
    


if __name__ == '__main__':
    #main()
    data_dr={}
    service=main()
    colvo_drive=drive_ls(service)
    print('Вижу дисков : ', len(colvo_drive))

    while True :
        for www in colvo_drive:
            sleep(3)
            try:
                ls_files_dr_or_fold(www['id'],service)
                data_dr[www['id']]='Ok'
            except:
                data_dr[www['id']]='Udalen  - '+ datetime.now()
        print(data_dr)

