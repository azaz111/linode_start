import os

from BIB_API import drive_ls , service_avtoriz , drivr_s_folder_all

if __name__ == '__main__':
    sp_data={}
    service=service_avtoriz()
    paps_perens=drivr_s_folder_all(service)
    print('Вижу папок : ', len(paps_perens ))

    sp_folders_name=[iii for iii in paps_perens if iii['name'] != 'PLOT']
    dup = [x for i, x in enumerate(sp_folders_name) if i != sp_folders_name.index(x)]
    for x in dup:
        sp_folders_name.remove(x) 
    #print('Из них дубликатов  : ',len(dup))


    for q in sp_folders_name:
       s_iddrive = q['parents'][0]
       q_name=q['name']
       #sp_data[q['name'][:-4]]=q['parents'][0]
       print(f'Диск {s_iddrive} Имя папки   {q_name} --  Истановим имя диску  {q_name[:-4]}')

       new_grives = service.teamdrives().update(teamDriveId=s_iddrive, body={"name": q_name[:-4]}).execute()
       print(new_grives)
    

    #with open("/root/AutoRclone/Spisok_drive2.txt", "w") as f_out:
    #   f_out.write('\n'.join(sp_drive_folders))
