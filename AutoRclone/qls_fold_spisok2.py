from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
from multiprocessing.pool import ThreadPool
import concurrent.futures
from BIB_API import drive_ls , service_avtoriz , drivr_s_folder_all

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

    try:
        with open("/root/.config/rclone/rclone.conf" , "r") as f:
            fff=f.read()
            ot=fff.find('{')
            do=fff.find('}')
            print(fff[ot:do+1])
            data_token=fff[ot:do+1]
            print('token nayden')
    except:
        data_token=input('ВВЕДИ ТОКЕН : ')
    
    old_data=''
    #    q=0
    
    for q in range(1,300):
       try:

           old_data_ish=f'[osnova{str(q)}]\ntype = drive\nscope = drive\ntoken = {data_token}\nteam_drive = {sp_data[str(q)]}\nroot_folder_id =\nservice_account_file = /root/AutoRclone/accounts{q}/{q}.json'
           old_data=old_data+'\n\n'+old_data_ish
           sp_drive_folders.append(sp_data[str(q)])
       except:
           old_data_ish=f'[osnova{str(q)}]\ntype = drive\nscope = drive\ntoken = {data_token}\nteam_drive = NONE\nroot_folder_id =\nservice_account_file = /root/AutoRclone/accounts{q}/{q}.json'
           old_data=old_data+'\n\n'+old_data_ish
           sp_drive_folders.append('NONE')
    #print(old_data)   
    with open('/root/.config/rclone/rclone.conf', 'w') as f:
       f.write(old_data)
    while True:
        if sp_drive_folders[len(sp_drive_folders)-1] == 'NONE':
           sp_drive_folders.pop(len(sp_drive_folders)-1)
        else:
           break
    with open("/root/AutoRclone/Spisok_drive.txt", "w") as f_out:
       f_out.write('\n'.join(sp_drive_folders))
    print("Ok") 