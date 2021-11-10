import requests
from bs4 import BeautifulSoup as bs

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
