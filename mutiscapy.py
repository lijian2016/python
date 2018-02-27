import requests
import re
from bs4 import BeautifulSoup
import time
import  multiprocessing as mp
from urllib.request import urljoin

base_url = "https://morvanzhou.github.io/"

def crawl(url):
    time.sleep(1)
    html = requests.get(url)
    return html.content.decode()

def parse(html):
    bsObj = BeautifulSoup(html,features="lxml")
    urls = bsObj.findAll("a",href=re.compile("^/.*?/$"))
    title = bsObj.h1.get_text()
    page_urls = set([urljoin(base_url,url.attrs["href"])for url in urls])
    url = bsObj.find("meta",property="og:url")["content"]
    return title,page_urls,url

unseen = set([base_url,])
seen = set()

while(len(unseen)!=0):
    url = unseen.pop()
    html = crawl(url)
    title,page_urls,url = parse(html)
    seen.add(url)
    unseen |= page_urls-seen
    print(title,"   ",url)
