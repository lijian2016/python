from bs4 import BeautifulSoup
import requests
import re
import random
import datetime
from requests import Session
import time

#hhw
random.seed(datetime.datetime.now())
baseUrl = "https://baike.baidu.com"
his = ["/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711"]
s = Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
while(True):
    time.sleep(random.randrange(1,3))
    url = baseUrl + his[-1]
    html = s.get(url)
    bsObj = BeautifulSoup(html.content.decode("utf-8"),"lxml")
    print(bsObj.find("h1").get_text(),'    url:',his[-1])
    subUrls = bsObj.findAll("a",target="_blank",href=re.compile("/item/(%.{2})+$"))

    if(len(subUrls)!=0):
        his.append(subUrls[random.randint(0,len(subUrls)-1)].attrs["href"])
    else:
        his.pop()