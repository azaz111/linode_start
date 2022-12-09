from dataclasses import replace
import os
from time import sleep, time
import conf_bf
from glob import glob
from json import loads
from BIB_API import service_avtoriz
import pymysql , json ,subprocess
from sshtunnel import SSHTunnelForwarder
import time
import pymysql 
from base64 import b64decode
from sshtunnel import SSHTunnelForwarder
from BIB_API import bot
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from sys import argv
from datetime import datetime
try:
   from tqdm import tqdm
except:
    os.system('pip install tqdm')
    from tqdm import tqdm

start_time = datetime.now()
limit_time = datetime.now()
osn_serv=int(argv[1])
osn_lim=int(argv[2])
path=conf_bf.server_name
tabl_json=conf_bf.tabl_json
sch_pereezdov=0
sch_smen_time=0
id_cred=''
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

def chek_drive(poisk):# Проверка диска на удаление
    service = service_avtoriz_v3()
    with open('Spisok_drive.txt', 'rb') as t:
      id_disk_prov=t.readlines()[poisk-1][:-1].decode('utf-8')
    print('Чекаем диск '+ id_disk_prov)
    new_grives = service.teamdrives().list(pageSize=100).execute() #
    drive_lsp = new_grives.get('teamDrives')
    #print(drive_lsp)
    for qqq in drive_lsp :
      #print(qqq['id'])
      if qqq['id'] == str(id_disk_prov):
         return True
    return False

#def getConnection(): 
    connection = pymysql.connect(host='127.0.0.1', port=server.local_bind_port, user='chai_cred',
                      password='Q12w3e4003r!', database='credentals',
                      cursorclass=pymysql.cursors.DictCursor)
    return connection

#def download_new_json(nomber_start):
    token_j2=None
    global sch_pereezdov
    global sch_smen_time
    global limit_time
    global id_cred
    sch_pereezdov+=1
    sch_smen_time+=1
    if sch_smen_time>20:
       print("Орем о лимите проектов ")
       bot("Превышен лимит проектов\nCервер: %s номер %s"% (conf_bf.server_name,osn_serv) , [292529642,183787479])
       sleep(1200)
    else:
      if (datetime.now()-limit_time).total_seconds() > 1800 :
         limit_time=datetime.now()
         sch_smen_time=0
    try:
       os.system('rm -R accounts%s'%nomber_start)
       os.system('mkdir accounts%s'%nomber_start)
    except:
       pass

    server.start()
    mybd = getConnection()
    cur = mybd.cursor()
    cur.execute( f"SELECT * FROM {tabl_json} WHERE status = 'True' " ) # запросим все данные  
    rows = cur.fetchall()
    try:
        token_j2=rows[0]['json']
        with open('accounts%s/%s.json' % (nomber_start,nomber_start) , 'w') as token:
            token.write(token_j2.split('"private_key":')[0])
        with open('accounts%s/%s.json' % (nomber_start,nomber_start) , 'a') as token:
            ot=token_j2.find('"private_key":')
            do=token_j2.find('"client_email"')
            data=token_j2[ot:do]
            data=data.replace('\n','\\n')
            token.write(data[:-4])
            token.write('\n  ')
            token.write(token_j2[do:])
        id_cred=rows[0]['id']
        print('+++  Записались  +++ ')
        cur.execute( f"UPDATE {tabl_json} set status = 'False' WHERE id = {id_cred} ") # Обнавление данных
        mybd.commit()
        mybd.close()
    except:
        print('++++++++++++++НЕТ СВОБОДНЫХ Json(ов)++++++++++++++++++')
        bot("НЕТ СВОБОДНЫХ Json(ов)\nCервер: %s номер %s"% (conf_bf.server_name,osn_serv) , [292529642,183787479])
    server.stop()
    if token_j2 :
      return True
    else:
      return False
    
        
def countdown(text='',num_of_secs=10):
   while num_of_secs:
       m, s = divmod(num_of_secs, 60)
       min_sec_format = '{:02d}:{:02d}'.format(m, s)
       print(text + min_sec_format, end='\r')
       time.sleep(1)
       num_of_secs -= 1  

#server = SSHTunnelForwarder(
#    ('149.248.8.216', 22),
#    ssh_username='root',
#    ssh_password='XUVLWMX5TEGDCHDU',
#    remote_bind_address=('127.0.0.1', 3306)
#)

def pap_mount(name_osnova,nomber_osnova):
   try:
      sleep(2)
      sum_plot=len(os.listdir(f'/{name_osnova}/{nomber_osnova}-1.d'))
      sleep(2)
   except:
      sum_plot=0
   return sum_plot

#def add_json_to_drive(id_drives,nomber_start):
   """ Привязываем джисоны к дискам """
   #print ('Привязываем джисоны к дискам' ,id_drives[0])
   drive=service_avtoriz_v3()
   accounts_to_add = []
   
   #print('Считываем джисоны')
   for id_drive in id_drives: 
      try:
         process = subprocess.Popen(['python3', 'masshare.py', '-d', id_drive ,'-p' , 'accounts%s'%nomber_start])
         process.wait()
         process.wait(timeout=5)
         print('Завершился')
      except subprocess.TimeoutExpired:
         process.terminate()
         sleep(5)
         print('Не ПРИВЯЗАНЫ')

def cikl():
   list_nomber=list(range(osn_serv+1,osn_lim+1))
   print(list_nomber)
   """ Монтируем + Проверка """
   schet=0
   x=osn_serv
   q=0

   for iii in tqdm(list_nomber):
      name_osnova='osnova'+str(iii)
      x += 1
      if pap_mount(name_osnova,iii) >= 1 :
         pass
         #print(f'Диск {name_osnova} смонтирован ')
      else:
         print(f'Нет плотов {name_osnova} - , косяк')
         if chek_drive(iii) == False:
            print("\033[31m{}\033[0m".format('   ...диск удален '))
         else:
            print("\033[32m{}\033[0m".format('   ...диск на месте '))
            # качаем джисоны 
            if chek_drive(iii) == False:
               break
             
            # берем айди диска 
            id_disk_prov=[]
            
            with open('Spisok_drive.txt', 'rb') as t:
                id_disk_prov.append(t.readlines()[iii-1][:-1].decode('utf-8'))
            
           
            

            name_osnova='osnova'+str(iii)
            while True:
               if chek_drive(iii) == False:
                  break
               schet=schet+1
               sleep(4)
               os.system (f'fusermount -uz /{name_osnova}/{iii}-1.d')
               sleep(2)
               os.system (f'screen -dmS "{name_osnova}" rclone mount {name_osnova}:{iii}-1.d /{name_osnova}/{iii}-1.d --vfs-read-chunk-size 1M --vfs-read-chunk-size-limit 0 --vfs-cache-mode full --max-read-ahead 0 --buffer-size off --no-checksum --no-modtime --read-only  --buffer-size off --dir-cache-time 960h --poll-interval 24h --allow-non-empty  --daemon')
               print( 'Пытаюсь повторно размонтировать')
               print(pap_mount(name_osnova,iii))
               if pap_mount(name_osnova,iii) >= 1 :
                  print("\033[32m{}\033[0m".format('   ...повторно прокатило'))
                  schet=0
                  break
               else:
                  print('------- Тут и так есть плоты "ЧТО ЕЩЕ НАДО ?"')
               if schet == 4:
                  schet=0
                  break  
   
   print("\033[32m{}\033[0m".format(' ВЫПОЛНЕНО ! Монтирование ЗАВЕРШЕНо ! \n Смен проекта %s\n Текущий json в базе %s \n Время работы %s'% (sch_pereezdov,id_cred,str(datetime.now() - start_time)[:-7])))


if __name__ == '__main__':
   while True:
      print('Приступаю к работе')
      cikl()
      countdown('Перерыв - ',120)




   

