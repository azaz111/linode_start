from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import io
from googleapiclient.errors import HttpError
import os , math
from sys import argv
import json
from BIB_API import service_avtoriz , ls_fails_onlly , spisok_fails_q ,folder_po_id , \
           spisok_fails_roditelya,createRemoteFolder,peremesti_v_odnu , drive_ls ,_is_success
successful = []

service = service_avtoriz()
service2 = service_avtoriz('v2')

if len(drive_ls(service)) == 1 :
   s_iddrive=drive_ls(service)[0]['id']
   mud_name=drive_ls(service)[0]['name']
else:
   print( 'НЕ пойму какого хрена вижу больше одного диска ') 
   exit()



id_rodf=createRemoteFolder(service2, 'PLOT' , s_iddrive)
peremesti_v_odnu(s_iddrive,id_rodf)


#lenss1=spisok_fails_roditelya(fold,s_iddrive,service)
#spp1=[eee.get('name') for eee in lenss1 ]
#lenss2=spisok_fails_roditelya(fold,s_iddrive,service)
#spp2=[eee.get('name') for eee in lenss2 ]
##print(lenss1)
##obschie=obschie+lenss
#print('naideno 1 : '+str(len(lenss1)))
#print('----------------------------------------')
#print('naideno 2 : '+str(len(lenss2)))
#print('----------------------------------------')
#list3=list(set(spp1)-set(spp2)) 
##print(list3)
#print(len(list3))
#file_ids=[]
#
#for i in lenss1:
#    spp0=i.get('name')
#    if spp0 in list3:
#        file_ids.append(i)  # Список с разницей





