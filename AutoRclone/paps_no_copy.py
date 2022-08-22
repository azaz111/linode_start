import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/cloud-platform",
          "https://www.googleapis.com/auth/iam"]
def folder_po_id(service,rodit=None): # Список папок (на диске или в папке) выход: список фалов
    if rodit :
       filtr = f"mimeType = 'application/vnd.google-apps.folder' and '{rodit}' in parents"
    else:
        filtr = f"mimeType = 'application/vnd.google-apps.folder'"
    folder_ids = service.files().list(corpora='allDrives', 
                                      includeItemsFromAllDrives=True, 
                                      supportsAllDrives=True,
                                      q=filtr, 
                                      fields="nextPageToken, files(id,name)").execute() # Список папок на диске
 
    folder_idss = folder_ids.get('files')
    return folder_idss

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
    #n=0
    file={}
    vse_pap=folder_po_id(service)
    #print(vse_pap)
    print('Найдено папок : ', len(vse_pap))
    for iii in vse_pap:
        if iii['name'].find('-copy')>1:

            file['title'] = iii['name'].replace('-copy', '')
            file['name'] = iii['name'].replace('-copy', '')
            print(file)
            nnn=service.files().update(fileId=iii['id'],
                                   supportsAllDrives=True, 
                                   body=file).execute()
            print(nnn['name']+ ' : '+nnn['id'])
    print('Готово')
    
if __name__ == '__main__':
    main()
