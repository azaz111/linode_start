import time 
import pymysql
from sshtunnel import SSHTunnelForwarder


what_og=False
what_bazis=input(' PP - 1 , Og - enter')

if what_bazis:
    what_pp=input('Номер сервера PP ?:' )
    tabl='badfix_tabl_pp'+what_pp
else:
    what_og=input('Номер сервера OG ?:' )
    tabl='badfix_tabl_og'+what_og

tabl_json='Project_baza'


server = SSHTunnelForwarder(
    ('149.248.8.216', 22),
    ssh_username='root',
    ssh_password='XUVLWMX5TEGDCHDU',
    remote_bind_address=('127.0.0.1', 3306)
)
server.start()
print('   ...connect')


def getConnection(user='badfix',password='adwWdw!2',database='badfix'): 
    # Вы можете изменить параметры соединения.
    connection = pymysql.connect(host='127.0.0.1', port=server.local_bind_port, user=user,
                      password=password, database=database,
                      cursorclass=pymysql.cursors.DictCursor)
    return connection

def new_badfix_tabl(len_drive):
    mybd = getConnection()
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


def write_baza_badfix(iii,id_drive,status,len_plots,time_o=1):
    mybd = getConnection()
    cur = mybd.cursor()  
    cur.execute( f"UPDATE  {tabl} set  id_drive = '{id_drive}' , status = '{status}' , time = '{time_o}' , len_plots = '{len_plots}' WHERE id = {iii}  " ) # запросим все данные  
    mybd.commit()
    cur.close()
    mybd.close()

def delete_baza_badfix(tabl,i):
    mybd = getConnection()
    cur = mybd.cursor()  
    cur.execute( f"DELETE FROM {tabl} WHERE id>{i}  " ) # запросим все данные  
    mybd.commit()
    cur.close()
    mybd.close()


def read(tabl):
    mybd = getConnection()
    cur = mybd.cursor()
    cur.execute( f"SELECT * FROM {tabl}" ) # запросим все данные  
    rows = cur.fetchall()
    mybd.commit()
    cur.close()
    mybd.close()
    return rows


def bf_trye():
    mybd = getConnection('chai_cred','Q12w3e4003r!','credentals')
    cur = mybd.cursor()
    cur.execute( f"SELECT * FROM {tabl_json} WHERE status = 'True' " ) # запросим все данные  
    rows = cur.fetchall()
    token_j2=rows[0]['json']
    id_cred=rows[0]['id']
    cur.execute( f"UPDATE {tabl_json} set status = 'False' WHERE id = {id_cred} ") # Обнавление данных
    mybd.commit()
    cur.close()
    mybd.close()
    return token_j2



