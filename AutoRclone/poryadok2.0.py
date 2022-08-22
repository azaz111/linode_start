from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import io
from googleapiclient.errors import HttpError
import os , math , time
import json
from BIB_API import service_avtoriz , ls_fails_onlly , spisok_fails_q ,folder_po_id , \
           spisok_fails_roditelya,createRemoteFolder,peremesti_v_odnu , drive_ls ,_is_success
successful = []

service = service_avtoriz()
service2 = service_avtoriz('v2')
peremes = input('  С ПЕРЕМЕЩЕНИЕМ ?? "1"-да , "enter" - нет ')
s_iddrive = input('Укажи айди Диска : ')

#kol_vo = int(input('Укажи сколько : '))
kol_vo_fails = int(input('Укажи сколько файлов в папку : '))
id_rodf=input('Укажи айди папки с плотами : ')



def _is_success0(id, resp, exception):
    global successful
    print(resp)
    print(exception)
    if exception is None:
        successful.append(resp['id'])


vse_p=ls_fails_onlly(s_iddrive,service)
vse=[eee.get('id') for eee in vse_p ]
print('Вижу фалов')
print(len(vse))
fvfol=math.ceil(len(vse)/kol_vo_fails)                 # на склько делить папок
print('Раскладываем по : '+ str(fvfol))


#id_rodf=createRemoteFolder(service2, 'PLOT' , s_iddrive)       #------------------------------------------------------------------------ ИЗМЕНЯЕМО
if peremes: 
    peremesti_v_odnu(s_iddrive,id_rodf)

for www in folder_po_id(service,s_iddrive):                          # Удалить пустые папки
    if len(spisok_fails_roditelya(www['id'],s_iddrive,service))==0:
        print('удаляю папку'+www['name']) 
        service.files().delete(fileId=www['id'],supportsAllDrives=True).execute()

q=0
ser_fold=[]
while q!=fvfol:
   q+=1
   ser_fold.append(str(q)+'-1.d')

for qqq in ser_fold:
    id_kon=createRemoteFolder(service2, qqq , id_rodf)

sp_paps=spisok_fails_q(service,s_iddrive,"mimeType = 'application/vnd.google-apps.folder' and name contains '-1.d'")
print(' НУжных папок : ' + str(sp_paps))
for ttt in sp_paps:
    partiya=vse[:kol_vo_fails]
    n=0
    while True:
        try:
            time.sleep(0.5)
            if len(ls_fails_onlly(s_iddrive,service,ttt['id'])) == fvfol :
                print('Полная папка : ' + ttt['name'])
                v_fold2=[eee.get('id') for eee in ls_fails_onlly(s_iddrive,service,ttt['id'])]
                vse=list(set(vse)-set(v_fold2))
                break
            partiya=list(set(partiya)-set(successful))
            n+=1
            print('Переношу :'+ str(len(partiya)) + ' Перенос :' +str(n))
            batch = service.new_batch_http_request(callback=_is_success0)
            for i in partiya[:999]:
                if i not in successful:
                    batch.add(service.files().update(fileId=i,
                                            addParents=ttt['id'],
                                            supportsAllDrives=True, 
                                            removeParents=id_rodf, fields='id, parents'))# 
            
            print('Otpravka zaprosa')
            batch.execute()
            print('Uspeh : '  + str(len(successful)))
            if len(partiya) == 0:
               vse=list(set(vse)-set(successful))
               successful=[]
               print('Konec')
               break
        except Exception as e:
            print(str(e))

for www in folder_po_id(service,s_iddrive):                          # Удалить пустые папки
    if len(spisok_fails_roditelya(www['id'],s_iddrive,service))==0:
        print('удаляю папку'+www['name']) 
        service.files().delete(fileId=www['id'],supportsAllDrives=True).execute()

