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
import pymysql
from sshtunnel import SSHTunnelForwarder
from BIB_API import  service_avtoriz , spisok_fails_roditelya , perenos_fails_list
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/cloud-platform",
          "https://www.googleapis.com/auth/iam"]

service = service_avtoriz()
spisok_drive_pach='Spisok_drive_vrem.txt'
spisok_drive_vrem='Spisok_drive.txt'
rclone_config_pach='/root/.config/rclone/rclone.conf'

server = SSHTunnelForwarder(
    ('149.248.8.216', 22),
    ssh_username='root',
    ssh_password='XUVLWMX5TEGDCHDU',
    remote_bind_address=('127.0.0.1', 3306)
)

def getConnection(): 
    # Вы можете изменить параметры соединения.
    connection = pymysql.connect(host='127.0.0.1', port=server.local_bind_port, user='chai_cred',
                      password='Q12w3e4003r!', database='credentals',
                      cursorclass=pymysql.cursors.DictCursor)
    return connection

def stisok_drive_baza(id_drives : list,  status="True" ,tabl='Spisok_drive'):
    server.start()
    mybd = getConnection()
    cur = mybd.cursor()
    try:
        cur.execute( f"DROP TABLE IF EXISTS {tabl};")
    except:
        pass
    for id_drive in id_drives :
        try:
           cur.execute( f"INSERT INTO {tabl}(name , id_drive , status )  VALUES('{id_drive[0]}','{id_drive[1]}', '{status}');" )
        except:
           cur.execute( f"CREATE TABLE {tabl} (id int PRIMARY KEY AUTO_INCREMENT, name TEXT , id_drive TEXT , status TEXT);" )
           cur.execute(  f"INSERT INTO {tabl}(name ,id_drive , status )  VALUES('{id_drive[0]}','{id_drive[1]}', '{status}');" )
    mybd.commit()
    mybd.close()
    server.stop()

def stisok_drive_false(tabl='Spisok_drive'):
    server.start()
    mybd = getConnection()
    cur = mybd.cursor()
    cur.execute( f"UPDATE {tabl} set status = 'False' WHERE id < 1000 ")
    mybd.commit()
    mybd.close()
    server.stop()

def stisok_drive_get(tabl='Spisok_drive'):
    server.start()
    mybd = getConnection()
    cur = mybd.cursor()
    cur.execute( f"SELECT * FROM {tabl}" ) # запросим все данные  
    rows = cur.fetchall()
    sp_drive=[[x['name'],x['id_drive']] for x in rows]
    print(sp_drive)
    mybd.commit()
    mybd.close()
    server.stop()
    return sp_drive

def stisok_drive_set( new_id_drive , id_drive , tabl='Spisok_drive'):
    server.start()
    mybd = getConnection()
    cur = mybd.cursor()
    cur.execute( f"UPDATE {tabl} set status = 'True' , id_drive = '{new_id_drive}' WHERE id_drive = '{id_drive}' ")
    mybd.commit()
    mybd.close()
    server.stop()

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

    while True:
        scheduled_time = time(hour=8, minute=20, second=0) # Время Cтарта
        # Время следующего старта будет назначено на запланированное время следующих суток
        next_loop_start = datetime.combine(date.today() + timedelta(days=1), scheduled_time)
        delay = (next_loop_start - datetime.now()).seconds
        countdown('Время до старта : ', delay)
        stisok_drive_false()
        id_disk_prov=stisok_drive_get()
        print(id_disk_prov)
        ls_drive=drive_ls(service)
        new_vse=[]
        for ddd in ls_drive :
            if ddd['id'] not in id_disk_prov:
                new_vse.append(ddd['id'])
    
        new_ls_drive=new_vse[:len(id_disk_prov)]
        print('Переезд На')
        #print(new_ls_drive)
        for i in range(len(new_ls_drive)):
            service.teamdrives().update(teamDriveId=new_ls_drive[i], body={"name": id_disk_prov[i][0]}).execute()
            try:
                perenos_files=spisok_fails_roditelya(id_disk_prov[i][1],id_disk_prov[i][1],service)
                print(perenos_files)
                perenos_files=[eee.get('id') for eee in perenos_files ]
                perenos_fails_list(perenos_files,new_ls_drive[i],service)
                print('ZAmenya Uspeh')
                process = subprocess.Popen(['python3', 'pot_dell.py', f'{id_disk_prov[i][1]}']) 
            except:
                try:
                   service.teamdrives().update(teamDriveId=id_disk_prov[i][1], body={"name": 'starii_'+str(i+1)}).execute()
                except:
                    pass
                print( '--------  Перенос не удался !!! ---------')
            ''' Заменим данные'''
            '''В конфиге '''
            f = open(rclone_config_pach).read()
            new_f = f.replace(id_disk_prov[i][1],new_ls_drive[i])
            with open(rclone_config_pach, 'w') as fdat:
               fdat.write(new_f)
            print('Заменили %s на %s / ' % (id_disk_prov[i][1],new_ls_drive[i]) )
            stisok_drive_set(new_ls_drive[i],id_disk_prov[i][1])
        countdown('До переименовывания - ',4800)
