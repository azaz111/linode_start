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


kakoi=int(input('Какой майнер ставим Господин !!! \n PP - 1 \n OG - 2 \n ~: '))

if kakoi == 1:
    type_miner='pp'
    api='chiapp00-5a6f-4555-acce-0355548e9139'
elif kakoi == 2:
    type_miner='og'
    api='950554c1-2786-4caa-9c8b-dc8461019dd5'
else:
    input('НЕТ ТАКОГО ВАРИАНТА')


def ipp():
    new_ip=requests.get('http://httpbin.org/ip').json()['origin']
    return new_ip.split('.')[3]

service=service_avtoriz()

vibor=int(input ('Как запустить ? \n  По указанному количеству дисков - 1\n  По текущим папкам с плотами - 2 \n  Свои папки (через пробел) -3 \n: '))


def vibor_m():
    list_miner=[]
    paps_int=int(input('Сколько папок майним + в конфиг ? : '))

    if vibor==2:
       #paps_perens=drivr_s_folder_all(service)
       paps_perens=[{'name':'1-2.d'},{'name':'2-1.d'},{'name':'3-3.d'},{'name':'4-4.d'}]

       sp_folders_name=[iii for iii in paps_perens if iii['name'] != 'PLOT']
       dup = [x for i, x in enumerate(sp_folders_name) if i != sp_folders_name.index(x)]
       for x in dup:
           sp_folders_name.remove(x) 
       splits = np.array_split(sp_folders_name, len(sp_folders_name)/paps_int)
       for array in splits:
           list_miner.append([x['name'][:-4] for x in list(array)])
       return(list_miner)

    if vibor==1:
        
        inss=int(input('Количество дисков : '))
        name_miner=list(range(1,inss+1))
        splits = np.array_split(name_miner, len(name_miner)/paps_int)
        for array in splits:
            list_miner.append([str(x) for x in list(array)])
        return(list_miner)

for q in vibor_m():
   q_name=ipp()+'_Miner_'+'_'.join(q)
   os.mkdir(q_name)
   shutil.copyfile('miner'+type_miner,q_name+'/miner')
   os.system('chmod 777 '+q_name+'/miner')
   # документ YAML
   yml = "config_ish.yaml"
   with open(yml) as f:
       data = yaml.load(f, Loader=SafeLoader)
       print(data)
   data['log']['path']=q_name+'/log/'
   data['minerName']=q_name
   data['apiKey']=api
   data['path']=['/osnova'+x+'/'+x+'-1.d' for x in q]

   print(data['path'])
   with open(q_name+'/config.yaml', 'w') as fw:
       data = yaml.dump(data, fw, sort_keys=False, 
                        default_flow_style=False)
   
   file_ = open(q_name+"/ouput.txt", "w")
   com='./miner'
   
   print(com.split(' '))
   os.chdir(q_name)
   process=subprocess.Popen(com, stdout=file_)
   os.chdir('..')
   with open(q_name+'/pid.log','w') as f :
     f.write(str(process.pid))
   