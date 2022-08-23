from __future__ import print_function
import os.path
from time import sleep
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os , subprocess
from multiprocessing.pool import ThreadPool
import concurrent.futures
from datetime import datetime, timedelta, time, date
from BIB_API import  service_avtoriz , spisok_fails_roditelya , perenos_fails_list
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/cloud-platform",
          "https://www.googleapis.com/auth/iam"]

service = service_avtoriz()
spisok_drive_pach='Spisok_drive_vrem.txt'
spisok_drive_vrem='Spisok_drive.txt'
rclone_config_pach='/root/.config/rclone/rclone.conf'

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
    return file_spis 

def countdown(text='',num_of_secs=10):
   while num_of_secs:
       m, s = divmod(num_of_secs, 60)
       min_sec_format = '{:02d}:{:02d}'.format(m, s)
       print(text + min_sec_format, end='\r')
       sleep(1)
       num_of_secs -= 1  

if __name__ == '__main__':
    
    #start=int(input('Начать с (enter) - нет : '))

    while True:
        scheduled_time = time(hour=8, minute=35, second=0) # Время Cтарта
        # Время следующего старта будет назначено на запланированное время следующих суток
        next_loop_start = datetime.combine(date.today() + timedelta(days=1), scheduled_time)
        delay = (next_loop_start - datetime.now()).seconds
        countdown('Время до старта : ', delay)
        os.rename(spisok_drive_vrem,spisok_drive_pach)
        with open(spisok_drive_pach, 'r') as t:
            id_disk_prov_txt=t.read().split('\n')
        id_disk_prov=[iii for iii in id_disk_prov_txt if iii != 'NONE']
        id_name=[x+1 for x,iii in enumerate(id_disk_prov_txt) if iii != 'NONE']


        print(id_disk_prov)
        ls_drive=drive_ls(service)
        new_vse=[]
        for ddd in ls_drive :
            if ddd['id'] not in id_disk_prov:
                new_vse.append(ddd['id'])
    
        new_ls_drive=new_vse[:len(id_disk_prov)]
        print('Переезд На')
        print(new_ls_drive)
        for i in range(len(new_ls_drive)):
            service.teamdrives().update(teamDriveId=new_ls_drive[i], body={"name": id_name[i]}).execute()
            try:
                perenos_files=spisok_fails_roditelya(id_disk_prov[i],id_disk_prov[i],service)
                print(perenos_files)
                perenos_files=[eee.get('id') for eee in perenos_files ]
                perenos_fails_list(perenos_files,new_ls_drive[i],service)
                print('ZAmenya Uspeh')
                process = subprocess.Popen(['python3', 'pot_dell.py', f'{id_disk_prov[i]}']) 
            except:
                try:
                   service.teamdrives().update(teamDriveId=id_disk_prov[i], body={"name": 'starii_'+str(i+1)}).execute()
                except:
                    pass
                print( '--------  Перенос не удался !!! ---------')
            ''' Заменим данные'''
            '''В список драйв '''
            f = open(spisok_drive_pach).read()
            new_f = f.replace(id_disk_prov[i],new_ls_drive[i])
            with open(spisok_drive_pach, 'w') as fdat:
               fdat.write(new_f)
            print('Заменили в ',spisok_drive_pach )
            '''В конфиге '''
            f = open(rclone_config_pach).read()
            new_f = f.replace(id_disk_prov[i],new_ls_drive[i])
            with open(rclone_config_pach, 'w') as fdat:
               fdat.write(new_f)
            print('Заменили в ',rclone_config_pach )
        countdown('До переименовывания - ',4800)
        os.rename(spisok_drive_pach,spisok_drive_vrem)
