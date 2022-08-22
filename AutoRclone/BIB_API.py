from warnings import filters
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import io
from googleapiclient.errors import HttpError
import os , pickle
from sys import argv
import json , time
import subprocess
from random import randint
from os.path import exists

#successful=[]
def service_avtoriz_v3(token='token.json'):# АВТОРИЗАЦИЯ  Drive API v3  
    SCOPES = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/iam',
    'https://www.googleapis.com/auth/cloudplatformprojects'
    ]
    creds = Credentials.from_authorized_user_file(token, SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service
    
def service_avtoriz(v2=None):# АВТОРИЗАЦИЯ  Drive API v3 по умолчанию v2 по запросу 
    SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/iam']

    """АВТОРИЗАЦИЯ  Drive v3 API.."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as t:
            creds = pickle.load(t)    
    
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
        with open('token.pickle', 'wb') as t:
            pickle.dump(creds, t)
    if v2:
        v='v2'
    else:
        v='v3'
    service = build('drive', v , credentials=creds)
    return service

def drive_ls(service):  # Cписок всех дисков
    file_spis=[]
    page_token = None
    while True:
        lsvse=service.teamdrives().list(pageSize=100,
                                        pageToken=page_token).execute() 

        #print(lsvse)
        for file in lsvse.get('teamDrives'):
            # Изменение процесса
            file_spis.append(file)
            # print(file.get('name'), file.get('id'))
        page_token = lsvse.get('nextPageToken', None)
        if page_token is None:
            break 
    return file_spis  

def new_drive(service,i): # Создаем новый диск подключаем джисоны вход : желаемое имя  выход data drive
       new_grive = service.teamdrives().create(requestId=randint(1,9999999), body={"name":f"{i}"}).execute() #создать диск
       new_grive_id=new_grive['id'] 
       process = subprocess.Popen(['python3', 'masshare.py', '-d', f'{new_grive_id}'])
       process.wait()
       return new_grive

def spisok_fails_q(service,s_iddrive,q): # Список всех файлов cвой фильтр   
    file_spis=[]
    page_token = None
    while True:
        response = service.files().list(spaces='drive',
                                        q=q,
                                        corpora='drive',
                                        includeItemsFromAllDrives=True,
                                        supportsAllDrives=True,
                                        driveId=s_iddrive,
                                        fields='nextPageToken, files(id, name)',
                                        pageToken=page_token).execute() 
    
        for file in response.get('files', []):
            # Изменение процесса
            file_spis.append(file)
            # print(file.get('name'), file.get('id'))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break     
    return file_spis

def folder_po_id(service,delit,rodit=None): # Список папок (на диске или в папке) выход: список фалов
    file_spis=[]
    page_token = None
    if rodit :
       filtr = f"mimeType = 'application/vnd.google-apps.folder' and '{rodit}' in parents"
    else:
        filtr = f"mimeType = 'application/vnd.google-apps.folder'"
    while True:
        folder_ids = service.files().list(corpora='drive', 
                                          includeItemsFromAllDrives=True, 
                                          supportsAllDrives=True,
                                          q=filtr, 
                                          driveId=delit, fields="nextPageToken, files(id,name)",
                                          pageToken=page_token).execute() 
        #print(folder_ids)
        for file in folder_ids.get('files'):
            # Изменение процесса
            file_spis.append(file)
            # print(file.get('name'), file.get('id'))     
        page_token = folder_ids.get('nextPageToken', None)
        if page_token is None:
            break 
    return file_spis 

def spisok_fails_roditelya(fold,s_iddrive,service,colvo=None): # Список всех файлов В указанной папке ! вход папка , диск. выход: список фалов  
    if colvo:
        pass
    else:
        colvo=10000
    file_spis=[]
    page_token = None
    while True:
        response = service.files().list(spaces='drive',
                                        q=f"'{fold}' in parents",
                                        corpora='drive',
                                        includeItemsFromAllDrives=True,
                                        supportsAllDrives=True,
                                        driveId=s_iddrive,
                                        fields='nextPageToken, files(id, name)',
                                        pageToken=page_token).execute() 
    
        for file in response.get('files', []):
            # Изменение процесса
            file_spis.append(file)
            # print(file.get('name'), file.get('id'))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break     
    return file_spis[:colvo]

def createRemoteFolder(service2, folderName, parentID = None):# Создаем новую папку  вход имя -- выход айди папки  
    #print(f'vzghu imya {folderName}')
    body = {'title': folderName,
      'mimeType': "application/vnd.google-apps.folder"
    }
    if parentID:
        body['parents'] = [{'id': parentID}]
    root_folder = service2.files().insert(supportsTeamDrives=True , body = body ).execute() 
    return root_folder['id']

def nev_json_autoriz(json_pach,SCOPES): # Авторизация с новым джисоном вход номер джисона выход новый сервисе
   SERVICE_ACCOUNT_FILE = json_pach
   credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
   service = build('drive', 'v3', credentials=credentials)
   #print('new json avtorizaciya : '+str(json_nomber))
   return service

def ls_files_dr_or_fold(s_iddrive,service,colvo=None): # Список всех файлов на диске или папке вход айди папки выход список (доп параметр количество желаемых фалов)
    if colvo:
        pass
    else:
        colvo=200000
    file_spis=[]
    page_token = None
    while True:
        response = service.files().list(q=f"'{s_iddrive}' in parents",
                                        corpora='allDrives',
                                        includeItemsFromAllDrives=True,
                                        supportsAllDrives=True,
                                        fields='nextPageToken, files(id, name)',
                                        pageToken=page_token).execute() 
    
        for file in response.get('files', []):
            file_spis.append(file)
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break  
    return file_spis[:colvo]

def ls_fails_onlly(s_iddrive,service,rodit=None): # Список всех файлов на диске в виде айди (возможно исключение родителя) 
    #q = f"{fold} in parents"
    #print(q)
    if rodit :
       filtr = f"mimeType != 'application/vnd.google-apps.folder' and '{rodit}' in parents"
    else:
        filtr = f"mimeType != 'application/vnd.google-apps.folder'"
    file_spis=[]
    page_token = None
    while True:
        response = service.files().list(spaces='drive',corpora='drive',
                                        q=filtr,
                                        includeItemsFromAllDrives=True,
                                        supportsAllDrives=True,
                                        driveId=s_iddrive,
                                        fields='nextPageToken, files(id, name,parents)',
                                        pageToken=page_token).execute() 
    
        for file in response.get('files', []):
            # Изменение процесса
            file_spis.append(file)
            # print(file.get('name'), file.get('id'))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break     
    return file_spis

def perenos_fails_list(new_file_l,id_foldnazna,service):  # Перенос  файла в указанную папрку или диск вход : Список айди которые нужно перенести и айди родителя     
   file = service.files().get(fileId=new_file_l[0], supportsAllDrives=True, fields='parents').execute()
   previous_parents = ",".join(file.get('parents'))
   for new_file in new_file_l:
       print(f'perenos :{new_file}')
       file = service.files().update(fileId=new_file,
                                     addParents=id_foldnazna,
                                     supportsAllDrives=True, 
                                     removeParents=previous_parents, fields='id, parents').execute()# перемещаем в бекапную папку

def poisk_or_sozd(service,folder_idsm,name_poisk): # Поиск если есть и создание если нет , нового диска  вход : Список (name,id)  дисков в которых искать выход : айди диска     
    razn = 0
    for sps in folder_idsm:  ## Если надо создали диск "разн" если есть то взяли айди
       name_prov = sps.get('name')
       if name_prov == name_poisk :
          razn_grive_id = sps.get('id')
          razn = 1
    if razn == 1 :
        print("drive - true = " + razn_grive_id)
    else:
        razn_grive = service.teamdrives().create(requestId=randint(1,9999999), body={"name":f"{name_poisk}"}).execute() #создать новый диск 
        razn_grive_id = razn_grive['id']
        process = subprocess.Popen(['python3', 'masshare.py', '-d', f'{razn_grive_id}'])
        process.wait()
    return razn_grive_id

def err_rezult(err): # Получаем тип ошибки (except HttpError as err:)
   if err.resp.get('content-type', '').startswith('application/json'):
      reason = json.loads(err.content).get('error').get('errors')[0].get('reason')
   return reason

def copi_files(service,id_ishod,id_nazna): # Копирование в указанного родителя ! вход: айди файла для копирования , папка назначения выход: труе если удачно ,  тип ошибки если неудачно
   try:
      print('copirovanie')
      new_file = service.files().copy( fileId=id_ishod , supportsTeamDrives=True ).execute() 
      new_file = new_file.get('id')
      print(f'kopia = {new_file} ')
      

      file = service.files().get(fileId=new_file, supportsAllDrives=True, fields='parents').execute()
      previous_parents = ",".join(file.get('parents')) 
      file = service.files().update(fileId=new_file,
                                    addParents=id_nazna,
                                    supportsAllDrives=True, 
                                    removeParents=previous_parents, fields='id, parents').execute()# перемещаем в бекапную папку 
      reason = 'uspeh'
   except HttpError as err: 
          if err.resp.get('content-type', '').startswith('application/json'):
              reason = json.loads(err.content).get('error').get('errors')[0].get('reason')
   return reason

def spis_permis(service,drive_id):  # Получить список разрешений прав доступа
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

def json_na_drive(drive_id=None, path='accounts', token='token.pickle', credentials='credentials.json'):
    pass

def _is_success(id, resp, exception):
    global successful

    if exception is None:
        #print(id)
        #print(resp)
        #print(exception)
        successful.append(resp['id'])

def peremesti_v_odnu(s_iddrive,id_foldnazna):# Все фалы в одну папку
    global successful
    service = service_avtoriz()
    ls_files=ls_fails_onlly(s_iddrive,service)
    print('Сортирую . '+str(len(ls_files)))

    id_foldnazna_iskl=ls_fails_onlly(s_iddrive,service,id_foldnazna) # Создаем Исключения
    successful=[eee.get('id') for eee in id_foldnazna_iskl ]

    parents={}
    for i in ls_files:
        parents[str(i['id'])]=[str(",".join(i['parents']))] # Создаем библиотеку ключей
    
    ls_files=[eee.get('id') for eee in ls_files ]
    while True :
        try:
            ls_files=list(set(ls_files)-set(successful))
            batch = service.new_batch_http_request(callback=_is_success) 
            for i in ls_files[:999]:
                batch.add(service.files().update(fileId=i,
                                        addParents=id_foldnazna,
                                        supportsAllDrives=True, 
                                        removeParents=",".join(parents.get(i)), fields='id, parents'))
            print('Otpravka zaprosa')
            batch.execute()
            time.sleep(5)
            if len(ls_files) == 0:
                successful=[]
                print('Konec')
                break
        except Exception as e:
            print(str(e))


def folder_all(service,rodit=None): # Список папок (на диске или в папке) выход: список фалов
    file_spis=[]
    page_token = None
    if rodit :
       filtr = f"mimeType = 'application/vnd.google-apps.folder' and '{rodit}' in parents"
    else:
        filtr = f"mimeType = 'application/vnd.google-apps.folder'"
    while True:
        folder_ids = service.files().list(corpora='allDrives', 
                                          includeItemsFromAllDrives=True, 
                                          supportsAllDrives=True,
                                          q=filtr, 
                                          fields="nextPageToken, files(id,parents,name)",
                                          pageToken=page_token).execute() 
        #print(folder_ids)
        for file in folder_ids.get('files'):
            # Изменение процесса
            file_spis.append(file)
            # print(file.get('name'), file.get('id'))     
        page_token = folder_ids.get('nextPageToken', None)
        if page_token is None:
            break 
    return file_spis 

def drivr_s_folder_all(service,rodit=None): # Список папок (на диске или в папке) выход: список фалов
    file_spis=[]
    page_token = None
    if rodit :
       filtr = f"mimeType = 'application/vnd.google-apps.folder' and '{rodit}' in parents"
    else:
        filtr = f"mimeType = 'application/vnd.google-apps.folder'"
    while True:
        folder_ids = service.files().list(corpora='allDrives', 
                                          includeItemsFromAllDrives=True, 
                                          supportsAllDrives=True,
                                          q=filtr, 
                                          fields="nextPageToken, files(parents,name)",
                                          pageToken=page_token).execute() 
        #print(folder_ids)
        for file in folder_ids.get('files'):
            # Изменение процесса
            file_spis.append(file)
            # print(file.get('name'), file.get('id'))     
        page_token = folder_ids.get('nextPageToken', None)
        if page_token is None:
            break 
    return file_spis 

def bot(mas , komu):
    #komu=[183787479,292529642]
    os.system('pip install aiogram')
    from aiogram.utils import executor
    from aiogram import Bot, Dispatcher
    bot = Bot(token='5256993370:AAFDtPpjGOvz1ZvsA-On2Bhzh3HGb53R7Gs')
    dp = Dispatcher(bot)
    async def somefunc(masge):
        for komu_m in komu:
           await bot.send_message(komu_m, masge)
     
    executor.start(dp, somefunc(mas))
 