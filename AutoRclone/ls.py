from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
from multiprocessing.pool import ThreadPool
import concurrent.futures
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
    

data=[]

def schet(data , service):
    name={}
    papki={}
    fails={}
    name['name']=data['name']
    name['id']=data['id']
    #name['files']=
    
    lenss=ls_files_dr_or_fold(data['id'],service)
    for www in lenss:
       name[www['name']]=len(ls_files_dr_or_fold(www['id'],service))
    #for i in lenss:
    #   print(i['name'])
    #   print(len(ls_files_dr_or_fold(i['id'],service)))

    print(name)
 
      #print('***Имя диска : ', name_nd)

       #lenss=ls_files_dr_or_fold(s_iddrive,service)
       #print('Папок вижу : ',len(lenss))
       #for i in lenss:
       #   print(i['name'])
       #   print(len(ls_files_dr_or_fold(i['id'],service)))
#
       #print('----------------------------------------')
    #return lenss

if __name__ == '__main__':
    #main()
    service=main()
    colvo_drive=drive_ls(service)
    print('Вижу дисков : ', len(colvo_drive))

    executor = concurrent.futures.ThreadPoolExecutor()

    for sps in colvo_drive:
        schet(sps,service) 
       #executor.submit(schet,sps,service)
