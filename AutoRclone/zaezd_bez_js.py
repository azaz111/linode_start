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
from BIB_API import service_avtoriz , drive_ls , folder_all

def perenos(pap,drive):
    service_mp = service_avtoriz()
    try:
        file = service_mp.files().get(fileId=pap, supportsAllDrives=True, fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))

        print('Перекидываю ')
        file = service_mp.files().update(fileId=pap,
                                      addParents=drive,
                                      supportsAllDrives=True, 
                                      removeParents=previous_parents, fields='id, parents').execute()
        return
    except HttpError as err: 
        print('ОШИБКА : ' + err)
        if err.resp.get('content-type', '').startswith('application/json'):
            reason = json.loads(err.content).get('error').get('errors')[0].get('reason')
            print('ОШИБКА : ' + reason)
            print('Ждем дополнительные 10 секунд')
            time.sleep(10) 
        perenos(pap,drive)
    return

service = service_avtoriz()
paps_perens=folder_all(service)
sp_folders=[iii for iii in paps_perens if iii['name'] != 'PLOT']
plot_folders=[iii['parents'][0] for iii in paps_perens if iii['name'] == 'PLOT'][0]
if plot_folders:
    print('Найшли Plot', plot_folders)

    pass
else:
    input('Ненайдена папка PLOT')
drive_lsf=drive_ls(service)
drive_lsf=[iii['id'] for iii in drive_lsf if iii['id'] != plot_folders]

if len(drive_lsf) < len(sp_folders):
    input('Немогу разложить нехватает дисков')

for i , folders in enumerate(sp_folders):
    print('Папка  :'+ folders['id'] +' Id drive : '+ drive_lsf[i])
    time.sleep(0.2)
    thread = threading.Thread(target=perenos, args=(folders['id'],drive_lsf[i],))
    thread.start()
    #perenos(folders['id'],drive_lsf[i])

print('ГОТОВО')
     


