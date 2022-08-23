from time import sleep
import pymysql
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
from multiprocessing.pool import ThreadPool
import concurrent.futures
from BIB_API import drive_ls , service_avtoriz , drivr_s_folder_all
from sshtunnel import SSHTunnelForwarder

tabl='drive_control'

what_bazis=input(' PP - 1 , Og - enter')

if what_bazis:
    what_pp=input('Номер сервера PP ?:' )
    name='pp'+what_pp
else:
    what_og=input('Номер сервера OG ?:' )
    name='og'+what_og


server = SSHTunnelForwarder(
    ('149.248.8.216', 22),
    ssh_username='root',
    ssh_password='XUVLWMX5TEGDCHDU',
    remote_bind_address=('127.0.0.1', 3306)
)

def getConnection(user='badfix',password='adwWdw!2',database='badfix'): 
    # Вы можете изменить параметры соединения.
    connection = pymysql.connect(host='127.0.0.1', port=server.local_bind_port, user=user,
                      password=password, database=database,
                      cursorclass=pymysql.cursors.DictCursor)
    return connection

def new_drive_control(folder,drive):
    server.start()
    mybd = getConnection()
    cur = mybd.cursor()
    try:
       cur.execute( f"INSERT INTO {tabl}(Name , papok , drive )  VALUES('{name}',{folder},{drive});" )
    except:
       cur.execute( f"CREATE TABLE {tabl} (id int PRIMARY KEY AUTO_INCREMENT, Name TEXT , papok int, drive int);" )
       cur.execute( f"INSERT INTO {tabl}(Name , papok , drive) VALUES('{name}',{folder},{drive});" )
    mybd.commit()
    mybd.close()
    server.stop()

if __name__ == '__main__':
    while True:
        try:
           service=service_avtoriz()
           colvo_drive=drive_ls(service)
           paps_perens=drivr_s_folder_all(service)
           print('Вижу папок : ', len(paps_perens ))
           
           colvo_drive=drive_ls(service)
           print('Вижу дисков : ', len(colvo_drive))
       
           new_drive_control(len(paps_perens ),len(colvo_drive))
        except:
            pass
        sleep(200)
