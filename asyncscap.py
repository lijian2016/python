import requests
import re
from bs4 import BeautifulSoup
import time
import  multiprocessing as mp
from urllib.request import urljoin
import aiohttp
import asyncio

base_url = "https://morvanzhou.github.io/"

async  def crawl(session,url):
    html = await  session.get(url)
    return await html.text()

def parse(html):
    bsObj = BeautifulSoup(html,features="lxml")
    urls = bsObj.findAll("a",href=re.compile("^/.*?/$"))
    title = bsObj.h1.get_text()
    page_urls = set([urljoin(base_url,url.attrs["href"])for url in urls])
    url = bsObj.find("meta",property="og:url")["content"]
    return title,page_urls,url

unseen = set([base_url,])
seen = set()
count = 0

pool = mp.Pool(8)
async def main(loop):
    global  count
    async with aiohttp.ClientSession() as session:
        while(len(unseen)!=0):
            crawl_jobs = [loop.create_task(crawl(session,url)) for url in unseen]
            finished,unfinished = await asyncio.wait(crawl_jobs)

            seen.update(unseen)
            unseen.clear()

            htmls = [j.result() for j in finished]
            parse_jobs = [pool.apply_async(parse,args=(html,)) for html in htmls]
            results = [j.get() for j in parse_jobs]
            for title, page_urls, url in results:
                unseen.update(page_urls-seen)
                count += 1
                print(count ,"    ",title, "   ", url)

if __name__=="__main__":
    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
    end = time.time()
    print(end-start)