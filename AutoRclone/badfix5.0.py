from dataclasses import replace
import os
from time import sleep, time
from BIB_API import  bot , drive_ls , service_avtoriz_v3 , ls_files_dr_or_fold
import pymysql , json ,subprocess
from msql_baza5 import new_badfix_tabl , write_baza_badfix , bf_trye
import pymysql 
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import ktokakoi
from datetime import datetime
from multiprocessing.pool import ThreadPool
import concurrent.futures
import threading
import pymysql
from sshtunnel import SSHTunnelForwarder

start_time = datetime.now()
limit_time = datetime.now()

sch_pereezdov=0
sch_smen_time=0
id_cred=''

server = SSHTunnelForwarder(
    ('149.248.8.216', 22),
    ssh_username='root',
    ssh_password='XUVLWMX5TEGDCHDU',
    remote_bind_address=('127.0.0.1', 3306)
)

def download_new_json(nomber_start):
    token_j2=None
    try:
       os.system('rm -R accounts%s'%nomber_start)
       os.system('mkdir accounts%s'%nomber_start)
    except:
       pass
    try:
        token_j2=bf_trye()
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
    except:
        print('++++++++++++++НЕТ СВОБОДНЫХ Json(ов)++++++++++++++++++')
        bot("НЕТ СВОБОДНЫХ Json(ов)\n ПОТОК №  %s"% nomber_start , [292529642,183787479])
    if token_j2 :
      return True
    else:
      return False

def getConnection(): 
    # Вы можете изменить параметры соединения.
    connection = pymysql.connect(host='127.0.0.1', port=server.local_bind_port, user='chai_cred',
                      password='Q12w3e4003r!', database='credentals',
                      cursorclass=pymysql.cursors.DictCursor)
    return connection

def stisok_drive_get(id,tabl='Spisok_drive'):
    server.start()
    mybd = getConnection()
    cur = mybd.cursor()
    cur.execute( f"SELECT * FROM {tabl} WHERE id = '{id}' " ) # запросим все данные  
    rows = cur.fetchall()
    sp_drive=[[x['name'],x['id_drive']] for x in rows][0]
    print(sp_drive)
    mybd.commit()
    mybd.close()
    server.stop()
    return sp_drive

def chek_drive(poisk):# Проверка диска на удаление
    service = service_avtoriz_v3()
    id_disk_prov=stisok_drive_get(poisk)[1]
    print('Чекаем диск '+ id_disk_prov)
    drive_lsp = drive_ls(service)
    for qqq in drive_lsp :
      #print(qqq['id'])
      if qqq['id'] == str(id_disk_prov) and len(ls_files_dr_or_fold(qqq['id'],service)) > 0 :
         return id_disk_prov
    return False

def countdown(text='',num_of_secs=10):
   while num_of_secs:
       m, s = divmod(num_of_secs, 60)
       min_sec_format = '{:02d}:{:02d}'.format(m, s)
       print(text + min_sec_format, end='\r')
       time.sleep(1)
       num_of_secs -= 1  

def pap_mount(name_osnova,nomber_osnova):
   try:
      sleep(2)
      sum_plot=len(os.listdir(f'/{name_osnova}/{nomber_osnova}-1.d'))
      sleep(2)
   except:
      sum_plot=0
      print(sum_plot)
   return sum_plot

def add_json_to_drive(id_drives,nomber_start):
   """ Привязываем джисоны к дискам """
   try:
      process = subprocess.Popen(['python3', 'masshare.py', '-d', id_drives ,'-p' , 'accounts%s'%nomber_start])
      process.wait(timeout=10)
      print('Завершился')
      return True
   except subprocess.TimeoutExpired:
      process.terminate()
      sleep(10)
      return False

         
def cikl(iii,schet_err=0):
   try:
      id_drive=chek_drive(iii)
      """ Монтируем + Проверка """
      schet=0
      name_osnova='osnova'+str(iii)
      sum_plot=pap_mount(name_osnova,iii)
      if sum_plot >= 1 :
       status=True

      else:
        print(f'Нет плотов {name_osnova} - , косяк')
        if id_drive == False:
           print("\033[31m{}\033[0m".format('   ...диск удален '))
           status=False
        else:
           print("\033[32m{}\033[0m".format('   ...диск на месте '))
           # качаем джисоны 
           if download_new_json(iii) == False:
              print( 'download_FALSE')
              sleep(150)
              return cikl(iii)
 
           if add_json_to_drive(id_drive,iii) == False:
              print( 'add_json_to_drive_FALSE')
              sleep(10)
              return cikl(iii)
           
           
           while True:
              if chek_drive(iii) == False:
                 break

              schet=schet+1
              sleep(4)
              os.system (f'fusermount -uz /{name_osnova}/{iii}-1.d')
              sleep(2)
              os.system (f'screen -dmS "{name_osnova}" rclone mount {name_osnova}:{iii}-1.d /{name_osnova}/{iii}-1.d --allow-non-empty --daemon  --multi-thread-streams 1024 --multi-thread-cutoff 128M --network-mode  --vfs-read-chunk-size-limit off --buffer-size 0K --vfs-read-chunk-size 64K --vfs-read-wait 0ms -v')
              print( 'Пытаюсь повторно размонтировать')
              #print(pap_mount(name_osnova,iii))
              if pap_mount(name_osnova,iii) >= 1 :
                 print("\033[32m{}\033[0m".format('   ...повторно прокатило'))
                 status=True
                 schet=0
                 break
              if schet == 4:
                 status=False
                 schet=0
                 break  
   
      '''Запишем в базу успешный чек'''
      write_baza_badfix(str(iii),str(id_drive),str(status),sum_plot,time())
      ''' ожидаем до следующего цикла '''
      sleep(300)
      '''Повторяем цикл'''
      return cikl(iii)
   except Exception as e:
      sleep(160)
      with open('Badfix_error_log.txt' , 'a' ) as f:
         f.write(f'Potok № {iii} . ) Error : '+ str(e) + '\n')

      if schet_err < 200: # Количество допустимых ошибок 
         cikl(iii,schet_err+1)
      
      write_baza_badfix(str(iii),str(id_drive),'False',sum_plot,time())

if __name__ == '__main__':
   nomb_serv=None
   for qqq in  os.listdir('/root'):
       if qqq.startswith('pp'):
           nomb_serv=qqq
           print(nomb_serv)
       elif qqq.startswith('og'):
           nomb_serv=qqq
           print(nomb_serv)
   #print(ktokakoi.data)
   if nomb_serv:
       try:
          nomera_s=[x[1] for x in ktokakoi.data if x[0]==nomb_serv][0]
       except:
          print('Не знаю такого имени сервера или нет фала ktokakoi.py')
   else:
      input('Имя сервера не найдено ......... Запуск не возможен')
   print(nomera_s)
   #new_badfix_tabl(len(len_spisok))

   for iii in nomera_s:
      sleep(0.7)
      #cikl(iii)
      thread = threading.Thread(target=cikl, args=(iii,))
      thread.start()
