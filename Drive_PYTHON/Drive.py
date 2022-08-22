
from cmath import exp
from time import sleep
import requests , os
try:
   from anticaptchaofficial.hcaptchaproxyless import *
except:
    os.system('pip install anticaptchaofficial')
    from anticaptchaofficial.hcaptchaproxyless import *
from multiprocessing.pool import ThreadPool
import concurrent.futures
import random
# смена с автропрокси Ротация: На каждый запроc
proxies = {
    "http": "http://111:111@162.19.151.193:10009",
    "https": "http://111:111@162.19.151.193:10009"}

API_KEY: str = "6cdfabe06c5d93700a785b6ec1abbe34"
URL_KEY: str ="https://td.msgsuite.workers.dev/"
SITE_KEY: str = "1b25fe2c-fa04-4ae0-b1b7-61d10597299c"
pash_orders = "acc.txt"   # Исходные данные 
pash_ua = "ua.txt"   # Исходные данные 



def cap(API_KEY , URL_KEY , SITE_KEY):
    global solver
    

    solver = hCaptchaProxyless()
    solver.set_verbose(1)
    solver.set_key(API_KEY)
    solver.set_website_url(URL_KEY)
    solver.set_website_key(SITE_KEY)
    
    solver.set_soft_id(0)
    
    g_response = solver.solve_and_return_solution()
    if g_response != 0:
        print("Ok token")#+g_response)
    else:
        print("task finished with error "+solver.error_code)
    return g_response


def register(email, name ,pop=0 ) -> str:
    header={'User-agent': ua[random.randint(0,len(ua)-1)]}
    if pop==12:
        return
    s: requests.Session = requests.session()
    ss=s.get("https://td.msgsuite.workers.dev",proxies=proxies)
    new_ip=requests.get('http://httpbin.org/ip',proxies=proxies).json()['origin']
    print(new_ip)
    if ss.status_code == 200:
        token=cap(API_KEY , URL_KEY , SITE_KEY)
        r = s.post("https://td.msgsuite.workers.dev/drive",
            json={
            'teamDriveName':name,
            'teamDriveThemeId':"random",
            'emailAddress':email,
            'channel':"0",
            'recaptcha':token
        },proxies=proxies,headers=header)
        print('Cтатус -------------------')
        print(r.status_code)
        print('Ответ -------------------')
        print(name+'___ '+r.text)
        print('-------------------')
        if r.text.find("Shared Drive has successfully been created !") != -1:
           print("Зареган Успешно ")
           solver.report_correct_recaptcha()
           return 'Ok'
        elif r.text.find("SyntaxError") != -1:
            print("Ошибка не получен !")
            solver.report_correct_recaptcha()
            return register(email, name , pop+1)
        elif r.text == "Captcha verification: invalid-input-response":
            solver.report_incorrect_recaptcha()
            print("Captcha invalid")
            return register(email, name, pop )
        elif r.text.find("today") != -1:
            print("Ошибка - надо сменить айпи !")
            solver.report_correct_recaptcha()
            return register(email, name, pop+1 )

    else:
        print('ERROR CONNECT')
        


if __name__ == '__main__':
    
    executor =concurrent.futures.ThreadPoolExecutor(max_workers=int(input('Сколько потоков ? :')))
    disc = int(input('Сколько дисков ? :'))
    try:
        '''почитали файл '''
        with open(pash_orders, "r", encoding="utf-8") as f:
            file_data: str = f.read()   
        with open(pash_ua, "r", encoding="utf-8") as f:
            ua: list = f.read().split('\n')   
    except Exception as e:
        input("File not found")

    for line in file_data.split("\n"):
        '''первый емайл  '''
        user_email: str = line
        print(user_email)
        for i in range(disc):
           executor.submit(register,user_email, f'Drive-{i}')
           sleep(0.5)
    print("Finished!")
    #exit()
