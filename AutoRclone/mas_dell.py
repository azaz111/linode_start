from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from argparse import ArgumentParser
from os.path import exists 
import os
from json import loads
from glob import glob
import pickle
from google.oauth2.credentials import Credentials
successful = []


def _is_success(id, resp, exception):
    global successful

    if exception is None:
        successful.append(resp['emailAddress'])


def permission_id_for_email(service, email):
  """Prints the Permission ID for an email address.

  Args:
    service: Drive API service instance.
    email: Email address to retrieve ID for.
  """

  id_resp = service.permissions().getIdForEmail(email=email).execute()
  return id_resp['id']

def spis_permis(service,drive_id):  
    file_spis=[]
    page_token = None
    while True:
        lsvse=service.permissions().list(fileId=drive_id, 
                                       fields='nextPageToken , permissions(id,role)',
                                       supportsAllDrives=True,
                                       pageToken=page_token).execute() 
    
        for file in lsvse.get('permissions'):
            # Изменение процесса
            file_spis.append(file)
            # print(file.get('name'), file.get('id'))
        page_token = lsvse.get('nextPageToken', None)
        if page_token is None:
            break 
    return file_spis  

def masshare(drive_id=None, path='accounts', token='token.json', credentials='credentials.json'):
    global successful

    SCOPES = ["https://www.googleapis.com/auth/drive",
              "https://www.googleapis.com/auth/cloud-platform",
              "https://www.googleapis.com/auth/iam"]
    creds = None

    if os.path.exists(token):
        creds = Credentials.from_authorized_user_file(token, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials, SCOPES)
            creds = flow.run_local_server(port=0)

    drive = build("drive", "v3", credentials=creds)
    accounts_to_add = []
    permission_id= []

    

    #print('Fetching emails')
    for i in glob('%s/*.json' % path):
        accounts_to_add.append(loads(open(i, 'r').read())['client_email'])
    #print('emails len : '+ str( len(accounts_to_add)))


    spp2=[]
    
    for eee in spis_permis(drive,drive_id):
       #print(eee)
       if eee['role'] != 'organizer':
           spp2.append(eee['id'])
    print('Oбнаруженно привязок %s'%len(spp2) )
    while True:
        batch = drive.new_batch_http_request()
        for i in spp2:
            if i not in successful:
                batch.add(drive.permissions().delete(fileId=drive_id, permissionId=i, supportsAllDrives=True))
        print('Adding')
        batch.execute()

        if len(spis_permis(drive,drive_id)) <= 4:
            break
    

    

if __name__ == '__main__':
    parse = ArgumentParser(description='A tool to add service accounts to a shared drive from a folder containing credential files.')
    parse.add_argument('--path', '-p', default='accounts', help='Specify an alternative path to the service accounts folder.')
    parse.add_argument('--token', default='token.json', help='Specify the pickle token file path.')
    parse.add_argument('--credentials', default='credentials.json', help='Specify the credentials file path.')
    parsereq = parse.add_argument_group('required arguments')
    parsereq.add_argument('--drive-id', '-d', help='The ID of the Shared Drive.', required=True)
    args = parse.parse_args()
    masshare(
        drive_id=args.drive_id,
        path=args.path,
        token=args.token,
        credentials=args.credentials
    )
