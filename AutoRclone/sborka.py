from time import sleep
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import io
from googleapiclient.errors import HttpError
from sys import argv
import subprocess
from BIB_API import service_avtoriz ,  drive_ls , folder_all
import threading

def sborka(ttt,previous_parents,id_papsbor):
    service_sborka = service_avtoriz()
    try:
        file = service_sborka.files().update(fileId=ttt,
                                      addParents=id_papsbor,
                                      supportsAllDrives=True, 
                                      removeParents=previous_parents, fields='id, parents').execute()
        return
    except:
        print('на повтор')
        sleep(20)
        sborka(ttt,previous_parents,id_papsbor)


chto_sobirat=int(input('Какие папки собираем : "1"- 1.d  , "2" - copy :  '))


service = service_avtoriz()
paps_perens=folder_all(service)
sp_folders=[iii for iii in paps_perens if iii['name'] != 'PLOT']
plot_folders=[[iii['parents'][0],iii['id']] for iii in paps_perens if iii['name'] == 'PLOT'][0]
if plot_folders:
    print('Найшли Plot ', plot_folders[1])
    print('Найшли Plot на диске ', plot_folders[0])
    #print('id Plot', folder_all(service,plot_folders)[0]['parents'][0])
    pass
else:
    input('Ненайдена папка PLOT')

if chto_sobirat == 1:
    print('ВЫбор 1')
    #print(sp_folders)
    sp_folders=[iii for iii in sp_folders if iii['name'].endswith('1.d')]
    sp_folders=[iii for iii in sp_folders if iii['parents'][0]!= plot_folders[1]]
    print('Папок сборки : ',len(sp_folders))

elif chto_sobirat == 2 :
    print('ВЫбор 2')
    #print(sp_folders)
    sp_folders=[iii for iii in sp_folders if iii['name'].endswith('copy.d')]
    sp_folders=[iii for iii in sp_folders if iii['parents'][0]!= plot_folders[1]]
    print('Папок сборки  copy : ',len(sp_folders))

else:
    print('Нет такого значения')




print('Начинаю сборку')

for folders in sp_folders:
    print('Папка  :'+ folders['id'] )
    sleep(0.2)
    thread = threading.Thread(target=sborka, args=(folders['id'],folders['parents'][0],plot_folders[1],))
    thread.start()
    #sborka(folders['id'],folders['parents'][0],plot_folders[1])





