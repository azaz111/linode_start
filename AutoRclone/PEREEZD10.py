import os.path
from time import sleep
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
import os , subprocess
from datetime import datetime, timedelta, time, date
from BIB_API import  service_avtoriz , spisok_fails_roditelya , perenos_fails_list
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import json 
#get current time
d = datetime.now()
try:
   from loguru import logger
   import apprise
except ModuleNotFoundError :
    os.system('pip install apprise')
    os.system('pip install loguru\n')
    from loguru import logger
    import apprise

logger.add('logger_pereezd.log', format="{time} - {level} - {message}")
apobj = apprise.Apprise()
apobj.add('tgram://5458358981:AAHmEsED5yN09uD2yNrpFdi9lBia7yZ59CQ/183787479/292529642')


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/cloud-platform",
          "https://www.googleapis.com/auth/iam"]

service = service_avtoriz()
spisok_drive_pach='Spisok_drive_vrem.txt'
spisok_drive_vrem='Spisok_drive.txt'
rclone_config_pach='/root/.config/rclone/rclone.conf'

def file_all_f(service,rodit=None): # Список папок (на диске или в папке) выход: список фалов
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

def move_one_file(new_file_l,id_foldnazna,service):  # Перенос  файла в указанную папрку или диск вход : Список айди которые нужно перенести и айди родителя     
    try:
        file = service.files().get(fileId=new_file_l, supportsAllDrives=True, fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        #print(f'perenos :{new_file_l}')
        file = service.files().update(fileId=new_file_l,
                                  addParents=id_foldnazna,
                                  supportsAllDrives=True, 
                                  removeParents=previous_parents, fields='id, parents').execute()# перемещаем в бекапную папку
        return True
    except HttpError as err: 
        if err.resp.get('content-type', '').startswith('application/json'):
            reason = json.loads(err.content).get('error').get('errors')[0].get('reason')
            print(reason)
        return False

def drive_ls(service):  # Cписок всех дисков
    file_spis=[]
    page_token = None
    while True:
        lsvse=service.teamdrives().list(pageSize=100,
                                        pageToken=page_token).execute() 

        for file in lsvse.get('teamDrives'):
            # Изменение процесса
            file_spis.append(file)
        page_token = lsvse.get('nextPageToken', None)
        if page_token is None:
            break 
    logger.info(f'Получили список дисков {len(file_spis)}') 
    return file_spis 

def countdown(text='',num_of_secs=10):
   while num_of_secs:
       m, s = divmod(num_of_secs, 60)
       min_sec_format = '{:02d}:{:02d}'.format(m, s)
       print(text + min_sec_format, end='\r')
       sleep(1)
       num_of_secs -= 1  

def main_s(i,scet=1):
    global new_ls_drive
    #os.rename(spisok_drive_pach,spisok_drive_vrem)
    # Проверим диск на доступность 
    service=service_avtoriz()
    print('start : ',id_disk_prov[i])
    perenos_files=file_all_f(service,id_disk_prov[i]) # Папки для переноса
    print(perenos_files)

    # получаем  первый  свободный диск  
    new_drive=new_ls_drive[i]
    for file_one in perenos_files:
        if move_one_file(file_one['id'],new_drive,service):
            r=service.teamdrives().update(teamDriveId=new_drive, body={"name":f'{d.strftime("%d")}_Drive_{i}' }).execute()
            print('rename: ',r)
            process = subprocess.Popen(['python3', 'pot_dell.py', f'{id_disk_prov[i]}']) 
            logger.info('Удачно перенесено')
        else:
            logger.error(f'Перенос на {new_drive}')
            return main_s(i,scet=scet+1)

    '''В список драйв '''
    f = open(spisok_drive_pach).read()
    new_f = f.replace(id_disk_prov[i],new_drive)
    with open(spisok_drive_pach, 'w') as fdat:
       fdat.write(new_f)
    '''В конфиге '''
    f = open(rclone_config_pach).read()
    new_f = f.replace(id_disk_prov[i],new_drive)
    with open(rclone_config_pach, 'w') as fdat:
       fdat.write(new_f)
    logger.info(f'Переезд Uspeh c диска {id_disk_prov[i]} на диск {new_drive} . Порыток {scet}')
    return
    


if __name__ == '__main__':
    if not os.path.exists(spisok_drive_vrem):
        input('Нет списка драйв !')

    while True:
        scheduled_time = time(hour=8, minute=11, second=30) # Время Cтарта
        # Время следующего старта будет назначено на запланированное время следующих суток
        next_loop_start = datetime.combine(date.today() + timedelta(days=1), scheduled_time)
        delay = (next_loop_start - datetime.now()).seconds
        countdown('Время до старта : ', delay)
        os.rename(spisok_drive_vrem,spisok_drive_pach)
        
        # Читаем диски с текстовика
        with open(spisok_drive_pach, 'r') as t:
            id_disk_prov_txt=t.read().split('\n')
        id_disk_prov=[iii for iii in id_disk_prov_txt if iii != 'NONE'] # 
        #id_name=[x+1 for x,iii in enumerate(id_disk_prov_txt) if iii != 'NONE']
        logger.info(f'Дисков для сьезда : {len(id_disk_prov)}')


        # Читаем диски для переезда
        ls_drive=drive_ls(service)
        new_vse=[]
        for ddd in ls_drive :
            if ddd['id'] not in id_disk_prov:
                new_vse.append(ddd['id'])
    
        new_ls_drive=new_vse[:]
        all_task=[]

        if len(id_disk_prov)+10>len(ls_drive)/2:
            apobj.notify(title=f"❗️❗️❗️ Переезд  : Error ",
                      body=f'Недостаточно дисков для переезда ! ')
            input('Недостаточно дисков для переезда !')

        apobj.notify(title=f"✅  Старт Переезда ",
                     body=f'Дисков для переноса :  {len(id_disk_prov)}')              
        executor = ThreadPoolExecutor(max_workers=20)
        for i in range(len(id_disk_prov)):
           #main_s(i)
           all_task.append(executor.submit(main_s, (i)))
        wait(all_task, return_when=ALL_COMPLETED)
        apobj.notify(body=f"🆗🆗🆗 Переезд окончен") 
        countdown('До переименовывания - ',4800)
        os.rename(spisok_drive_pach,spisok_drive_vrem)
        apobj.notify(body=f"✅✅ Переименован ✅✅") 

