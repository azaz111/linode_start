import random , shutil
import subprocess , os , requests
from time import sleep 
import numpy as np
import yaml
from yaml.loader import SafeLoader
#try:
shutil.copyfile('/root/AutoRclone/BIB_API.py','BIB_API.py')
shutil.copyfile('/root/AutoRclone/token.json','token.json')
#except:
#    input('нехватает фалов ......')
from BIB_API import drive_ls , service_avtoriz , drivr_s_folder_all

def ipp():
    new_ip=requests.get('http://httpbin.org/ip').json()['origin']
    return new_ip.split('.')[3]

service=service_avtoriz()

paps_int=int(input('Сколько папок в работу ? : '))

paps_perens=drivr_s_folder_all(service)
print('Вижу папок : ', len(paps_perens ))
sp_folders_name=[iii for iii in paps_perens if iii['name'] != 'PLOT']
dup = [x for i, x in enumerate(sp_folders_name) if i != sp_folders_name.index(x)]
for x in dup:
    sp_folders_name.remove(x) 
#print('Из них дубликатов  : ',len(dup))
#for q in sp_folders_name:
#   for i range()

   #s_iddrive = q['parents'][0]
   #q_name=q['name']
   #os.mkdir(q_name)





#splits = np.array_split(sp_folders_name, len(sp_folders_name)/paps_int)
#for array in splits:
#    #print(list(array))
#    list_miner=[x['name'][:-4] for x in list(array)]
#    name_miner='_'.join(list_miner)
#    print(name_miner)
#    # документ YAML
#    yml = "config_ish.yaml"
#    with open(yml) as f:
#        data = yaml.load(f, Loader=SafeLoader)
#        print(data)
#    data['minerName']=ipp()+'_Miner_'+name_miner
#    data['path']=['/osnova'+x['name'][:-4]+'/'+x['name'] for x in list(array)]
#    
#    with open('config.yaml', 'w') as fw:
#        data = yaml.dump(data, fw, sort_keys=False, 
#                         default_flow_style=False)
#    input('------')
import subprocess
file_ = open("ouput.txt", "w")
subprocess.Popen("./miner", stdout=file_)