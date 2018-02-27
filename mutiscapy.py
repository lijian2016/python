import requests
import re
from bs4 import BeautifulSoup
import time
import  multiprocessing as mp
from urllib.request import urljoin

base_url = "https://morvanzhou.github.io/"

def crawl(url):
    # time.sleep(1)
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

pool = mp.Pool(8)
start = time.time()
count = 0
while(len(unseen)!=0):
    # url = unseen.pop()
    # html = crawl(url)
    # title,page_urls,url = parse(html)
    # seen.add(url)
    # unseen |= page_urls-seen
    # print(title,"   ",url)

    crawl_jobs = [pool.apply_async(crawl,args=(url,))for url in unseen]
    htmls = [j.get() for j in crawl_jobs]
    parse_jobs = [pool.apply_async(parse,args=(html,))for html in htmls]
    results = [j.get()for j in parse_jobs]
    seen.update(unseen)
    unseen.clear()

    for title,page_urls,url in results:
        unseen.update(page_urls-seen)
        count += 1
        print(count ,"    ",title, "   ", url)

end = time.time()
print(end-start)