from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
import os , math , time
import json
import subprocess
import threading
from BIB_API import service_avtoriz , perenos_fails_list , spisok_fails_q ,new_drive , \
           spisok_fails_roditelya,createRemoteFolder,peremesti_v_odnu , drive_ls ,_is_success , folder_all
def perenos(pap,drive):
    try:
        file = service.files().get(fileId=pap, supportsAllDrives=True, fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))

        print('Перекидываю ')
        file = service.files().update(fileId=pap,
                                      addParents=drive,
                                      supportsAllDrives=True, 
                                      removeParents=previous_parents, fields='id, parents').execute()
    except HttpError as err: 
        print('ОШИБКА : ' + err)
        if err.resp.get('content-type', '').startswith('application/json'):
            reason = json.loads(err.content).get('error').get('errors')[0].get('reason')
            print('ОШИБКА : ' + reason)
            print('Ждем дополнительные 10 секунд')
            time.sleep(100) 
successful = []

service = service_avtoriz()
sp_paps=folder_all(service)
sp_paps_name=[eee['name'] for eee in sp_paps ]
try:
    sp_paps_name.remove('PLOT')
except:
    pass
sp_paps_name=[eee[:-4] for eee in sp_paps_name ]
got_grive=[]
drive_bibl={}
pap_bibl={}
for ddd in drive_ls(service):
    if ddd['name'] in sp_paps_name:
        drive_bibl[ddd['name']]=ddd['id']
for ddd in sp_paps:
    if ddd['name'][:-4] in sp_paps_name:
        pap_bibl[ddd['name'][:-4]]=ddd['id']

print(list(pap_bibl))
print(len(list(pap_bibl)))

for i in list(pap_bibl):

    print('Hа диск :'+ i +' Id : '+ drive_bibl[i])
    print('папка ', pap_bibl[i])
    #perenos(pap_bibl[i],drive_bibl[i])
    thread = threading.Thread(target=perenos, args=(pap_bibl[i],drive_bibl[i],))
    thread.start()

print('ГОТОВО')
     


