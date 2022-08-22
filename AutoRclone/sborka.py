from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import io
from googleapiclient.errors import HttpError
from sys import argv
import subprocess
from BIB_API import service_avtoriz , perenos_fails_list , spisok_fails_q ,new_drive , \
           spisok_fails_roditelya,createRemoteFolder,peremesti_v_odnu , drive_ls ,_is_success
successful = []

service = service_avtoriz()
service2 = service_avtoriz('v2')
chto_sobirat=int(input('Какие папки собираем : "1"- 1.d  , "2" - copy :  '))

#if len(drive_ls(service)) == 21 :
#   s_iddrive=drive_ls(service)[0]['id']
#   mud_name=drive_ls(service)[0]['name']
#else:
#   print( 'НЕ пойму какого хрена вижу не стандартное количество дисков ') 
#   exit()

for q in drive_ls(service):
    if len(spisok_fails_q(service,q['id'],"mimeType = 'application/vnd.google-apps.folder' and name contains 'PLOT'"))>= 1: 
       id_papsbor=spisok_fails_q(service,q['id'],"mimeType = 'application/vnd.google-apps.folder' and name contains 'PLOT'")[0]['id']
sp_paps=[]
print(id_papsbor)
for q in drive_ls(service):
    if chto_sobirat == 1:
        try:
            id_p=spisok_fails_q(service,q['id'],"mimeType = 'application/vnd.google-apps.folder' and name contains '.d'")[0]['id']
            sp_paps.append(id_p)
        except:
            pass
    elif chto_sobirat == 2:
        try:
            id_p=spisok_fails_q(service,q['id'],"mimeType = 'application/vnd.google-apps.folder' and name contains '-copy'")[0]['id']
            sp_paps.append(id_p)
        except:
            pass    
    else:
        input ( 'НЕВЕРНОЕ ЗНАЧЕНИЕ ')    


print(' Папка СБОРКИ: ' + str(id_papsbor))
print(' НУжных папок : ' + str(len(sp_paps)))

print('Начинаю сборку')

n=0
for ttt in sp_paps:
    print(ttt)
    file = service.files().get(fileId=ttt, supportsAllDrives=True, fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))
    file = service.files().update(fileId=ttt,
                                  addParents=id_papsbor,
                                  supportsAllDrives=True, 
                                  removeParents=previous_parents, fields='id, parents').execute()
