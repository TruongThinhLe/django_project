import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import os
import subprocess
def auto_mean(word):
    request=requests.session()
    request.headers.update({'Content-Type':'text/html','Retry-After':'3600'})
    url='https://dictionary.cambridge.org/dictionary/english-vietnamese/'+word
    src=request.get(url,headers={'User-agent':'my bot'})
    soup=bs(src.content,"html.parser")
    type=soup.find_all("span",class_="pos dpos")[0].text
    mean=soup.find_all("span",class_="trans dtrans")[0].text
    example=soup.find_all("span",class_="eg deg")[0].text
    return [type,mean,example]
    print(mean[0].text)
    print(type[0].text)
    print(example[0].text)
def send_message():
    messenger=webdriver.Chrome(executable_path='/lib/chromium-browser/chromedriver')
    url='https://facebook.com'
    messenger.get(url)
    time.sleep(5)
def st_storage():
    cmd1=subprocess.run(['df','-h'],stdout=subprocess.PIPE,text=True)
    storage=cmd1.stdout[cmd1.stdout.find('root'):cmd1.stdout.find('devtmpfs')]
    return storage.replace('root','storage')
    