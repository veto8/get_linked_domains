#!/usr/bin/env python

import platform, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import validators
import multiprocessing as mp

class GetDomains:
    def __init__(self, domain="127.0.0.1", proc=3):
        self.domain = domain
        self.p = proc
        self.o = []
        self.o.append("http://" + domain)
        #for i in range(1,100):
        #  self.o.append("http://{0}/sku/{1}.html".format(domain,i))
        self.c = []
        self.e = []

    def start(self):
        print("...start")
        mp.set_start_method("spawn")
        while len(self.o):
            time.sleep(0.5)
            chunks = []
            for i in range(0, len(self.o), self.p):
              chunks.append(self.o[i:i + self.p])
            for i in chunks:
              jobs = []
              manager = mp.Manager()
              return_dict = manager.dict()
              for k,v in enumerate(i):
                #print(v)
                self.c.append(v)
                self.o.remove(v)                                  
                p = mp.Process(
                  target=self.get_page_items,
                  args=(
                      v,
                      k,
                      return_dict
                   ),
                 )
                jobs.append(p)
                p.start()                
              #print("...tread.................")
              print("proc: {0} \t open: {1} \t closed: {2} \t ext: {3}".format(self.p,len(self.o),len(self.c),len(self.e)))                        
              
              for proc in jobs:
                proc.join()
                
              for k,v in enumerate(return_dict.values()):
                 #print(k)
                 self.process_items(v)                  




    def get_page_items(self,req_url, id, return_dict ):
        if validators.url(req_url):
          #print("...req:\t{}".format(req_url))
          chrome_options = Options()
          chrome_options.add_argument("--headless=new")  # for Chrome >= 109

          browser = webdriver.Chrome(options=chrome_options)
          browser.get(req_url)
          soup = BeautifulSoup(browser.page_source, "html.parser")
          _items = soup.find_all("a")
          items = []
          for i in _items:
            items.append(i.get("href"))          
          #print(items)          
          return_dict[id] = items

    def request_page(self,req_url ):
        if validators.url(req_url):
          #print("...req:\t{}".format(req_url))
          chrome_options = Options()
          chrome_options.add_argument("--headless=new")  # for Chrome >= 109
          browser = webdriver.Chrome(options=chrome_options)
          browser.get(req_url)
          soup = BeautifulSoup(browser.page_source, "html.parser")
          _items = soup.find_all("a")
          items = []
          for i in _items:
            items.append(i.get("href"))
          print(items)

    def process_items(self, items):
        for url in items:
            # extract the url of the page

            # if the url has not starting protocol and domain, then  adding it
            if not url.startswith("http://"):
                url = "http://" + self.domain + url

            # remove ending forwardslash
            if url[-1] == "/":
                url = url[:-1]


            # if this url is already recorded skip loop
            if url in self.c or url in self.e:
                continue

            # if the url is for external, then save it to the external list
            if url.startswith("http://" + self.domain) == False:
                if url not in self.e:
                    self.e.append(url)
                continue

            if url not in self.o and url not in self.c:
                #print("...add:\t{}".format(url))
                if url not in self.o:
                    self.o.append(url)

    def complete(self):
        print("...completed!");
        print(self.c);        

if __name__ == "__main__":
    d = GetDomains("127.0.0.1", 6)
    d.start()
    d.complete()    
    #d.request_page("http://127.0.0.1")


