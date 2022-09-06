from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
from multiprocessing.pool import ThreadPool
import concurrent.futures
from sshtunnel import SSHTunnelForwarder
import pymysql
from BIB_API import drive_ls , service_avtoriz , drivr_s_folder_all


def new_badfix_tabl(tabl,len_drive):
    server.start()
    mybd = getConnection(user='badfix',password='adwWdw!2',database='badfix')
    cur = mybd.cursor()
    try:
        cur.execute( f"DROP TABLE IF EXISTS {tabl};")
    except:
        pass
    for qww in range(len_drive):
        try:
           cur.execute( f"INSERT INTO {tabl}(Name , id_drive , status , time , len_plots)  VALUES('osnova_{qww+1}','none','False','none', 0);" )
        except:
           cur.execute( f"CREATE TABLE {tabl} (id int PRIMARY KEY AUTO_INCREMENT, Name TEXT , id_drive TEXT , status TEXT, time TEXT, len_plots int);" )
           cur.execute( f"INSERT INTO {tabl}(Name , id_drive , status , time , len_plots)  VALUES('osnova_{qww+1}','none','False','none', 0);" ) # Добавляем данные1
    print('База создана')
    mybd.commit()
    cur.close()
    mybd.close()
    server.stop()


server = SSHTunnelForwarder(
    ('149.248.8.216', 22),
    ssh_username='root',
    ssh_password='XUVLWMX5TEGDCHDU',
    remote_bind_address=('127.0.0.1', 3306)
)


def getConnection(user='chai_cred',password='Q12w3e4003r!',database='credentals'): 
    # Вы можете изменить параметры соединения.
    connection = pymysql.connect(host='127.0.0.1', port=server.local_bind_port, user=user,
                      password=password, database=database,
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



if __name__ == '__main__':
    sp_data={}
    service=service_avtoriz()
    #colvo_drive=drive_ls(service)
    paps_perens=drivr_s_folder_all(service)
    print('Вижу папок : ', len(paps_perens ))
    #print(paps_perens )

    sp_folders_name=[iii for iii in paps_perens if iii['name'] != 'PLOT']
    dup = [x for i, x in enumerate(sp_folders_name) if i != sp_folders_name.index(x)]
    for x in dup:
        sp_folders_name.remove(x) 
    print('Из них дубликатов  : ',len(dup))
    #print(sp_folders_name)
    sp_drive_folders=[]
    for q in sp_folders_name:
        sp_data[q['name'][:-4]]=q['parents'][0]
    #print(sp_data)

    sp_sp=[]
    #print(sp_data)
    for x in range(1,300):
        if str(x) in list(sp_data):
           sp_sp.append([str(x)+'-1.d',sp_data[str(x)]])
        else:
           sp_sp.append(['NONE','NONE'])
    #%print(sp_sp)       


    while True:
        if sp_sp[len(sp_sp)-1][0] == 'NONE':
           sp_sp.pop()
        else:
           break
    stisok_drive_baza(sp_sp)
    new_badfix_tabl('badfix_tabl_'+input('Введи "pp" или "og" : '),len(sp_sp))
    print("Ok") 
