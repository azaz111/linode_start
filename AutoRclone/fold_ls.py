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
    service=service_avtoriz()
    colvo_drive=drive_ls(service)
    paps_perens=drivr_s_folder_all(service)
    print('Вижу папок : ', len(paps_perens ))
    sp_drive_folders=[iii['parents'][0] for iii in paps_perens ]
    dup = [x for i, x in enumerate(sp_drive_folders) if i != sp_drive_folders.index(x)]
    for x in dup:
        sp_drive_folders.remove(x) 
    print('Из них дубликатов  : ',len(dup))

    with open("/root/AutoRclone/Spisok_drive2.txt", "w") as f_out:
       f_out.write('\n'.join(sp_drive_folders))
