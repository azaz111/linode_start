import os
from time import sleep
from argparse import ArgumentParser
import shutil
import threading
import subprocess
try:
   import pymysql
   from sshtunnel import SSHTunnelForwarder
except:
   os.system('pip install pymysql')
   os.system('pip install sshtunnel')
   import pymysql
   from sshtunnel import SSHTunnelForwarder
n=0
tabl='dbox'

server = SSHTunnelForwarder(
    ('149.248.8.216', 22),
    ssh_username='root',
    ssh_password='XUVLWMX5TEGDCHDU',
    remote_bind_address=('127.0.0.1', 3306))

def getConnection(): 
    connection = pymysql.connect(host='127.0.0.1', port=server.local_bind_port, user='chai_cred',
                      password='Q12w3e4003r!', database='credentals',
                      cursorclass=pymysql.cursors.DictCursor)
    return connection

def size_drive(disk_dirs="D://"):
   size=0
   try:
      total, used, free = shutil.disk_usage(disk_dirs)
      print("Total: %d GiB" % (total // (2**30)))
      print("Used: %d GiB" % (used // (2**30)))
      print("Free: %d GiB" % (free // (2**30)))  
      size= size + total // (2**30)
   except:
      pass
   return size

def download_token():
   server.start()
   mybd = getConnection()
   cur = mybd.cursor()
   cur.execute( f"SELECT * FROM {tabl} WHERE len=(SELECT min(len) FROM {tabl}) and status = 'True' " ) # запросим все данные  
   rows = cur.fetchall()
   print(len(rows))
   if len(rows) == 0:
      print('Нет свободных токенов !!!')
      mybd.commit()
      mybd.close()
      server.stop()
      sleep(20)
      return download_token()
   token=rows[0]['token']
   print(token)
   id=rows[0]['id']
   cur.execute( f"UPDATE {tabl} set status = 'False' WHERE id = {rows[0]['id']} ") # Обнавление данных
   mybd.commit()
   mybd.close()
   server.stop()
   return [token,id]

def vernem_true(id_v , conf_d):

   try:
      com=f'rclone ls {conf_d}:'
      comls= com.split(' ')
      process = subprocess.Popen(comls, stdout=subprocess.PIPE)
      process.wait()
      stat_len=len(str(process.communicate()[0]).split('\\n'))
      print('[ ! ] Plot account ' , str(stat_len))
   except:
      stat_len='error'

   server.start()
   mybd = getConnection()
   cur = mybd.cursor()
   cur.execute( f"UPDATE {tabl} set status = 'True' , len = '{stat_len}'  WHERE id = {id_v}") # Обнавление данных
   mybd.commit()
   mybd.close()
   server.stop()

def new_config():
   tokens=download_token()
   with open('/root/.config/rclone/rclone.conf', 'a') as f:
       f.write(f'\n[dbox_{str(n)}]\ntype = dropbox\ntoken = {tokens[0]}')
   return tokens[1]

def stat_progect(com : str , id_osvobodi , conf_d):
    comls= com.split(' ')
    #print(comls)
    process = subprocess.Popen(comls, stdout=subprocess.PIPE, universal_newlines=True)
    print( str(process.pid) )
    while True:
        line = process.stdout.readline()
        if line.find(' Transferred:')>-1:
            sleep(5)
            print('['+str(process.pid)+'] - '+line)
        if not line:
          break
    print('['+str(process.pid)+'] - PEREDAN vernem True id' + str(id_osvobodi))
    vernem_true(id_osvobodi, conf_d)

def transfer(dirs):
   global n
   unique=[]
   while True:
       dirfiles = os.listdir(dirs)
       for qqq in  dirfiles:
          if qqq not in unique and os.stat(dirs+'/'+qqq).st_size > 108650979000:
              sleep(5)
              if qqq[-3:] != 'txt':
                 os.rename(dirs+'/'+qqq , dirs+'/'+qqq[:-4]+'txt')
                 qqq=qqq[:-4]+'txt'
              print('запускаю транс  ' + qqq )
              id_osvobodi=new_config()
              com=f'rclone move {dirs}/{qqq} dbox_{str(n)}: --drive-stop-on-upload-limit --transfers 1 -P -v --log-file /root/rclone1.log'
              thread = threading.Thread(target=stat_progect, args=(com,id_osvobodi,f'dbox_{str(n)}',))
              thread.start()
              unique.append(qqq)
              if len(unique) > 20:
                 unique.pop(0)
              n=n+1
       sleep(30)


if __name__ == '__main__':
   parse = ArgumentParser(description=' Настройка трансфера плотов .')
   parse.add_argument('--pach','-p', default=None, help='Путь c плотами .')
   args = parse.parse_args()

   if args.pach:
     dirs=args.pach
   else:
     size_d=size_drive('/chtemp')
     if size_d>150 or size_d==0:
        dirs='/disk1' 
        try:
           os.system(f'screen -X -S sortirovka quit')
        except:
           pass
     else:
        dirs='/chtemp'
   print('Work dirs : ',dirs)

   try:
      os.remove('/root/.config/rclone/rclone.conf')
   except:
      pass
   transfer(dirs)
