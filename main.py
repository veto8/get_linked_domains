#!/usr/bin/env python

import platform, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import validators
import multiprocessing as mp

class GetDomains:
    def __init__(self, domain="myridia.com"):
        self.domain = domain
        self.t = 3 
        self.o = []
        self.o.append("https://" + domain)
        for i in range(200,210):
          self.o.append("https://{0}/dev_posts/view/{1}".format(domain,i))
        self.c = []
        self.e = []

    def start(self):
        print("...start")
        mp.set_start_method("spawn")
        while len(self.o):
            time.sleep(0.5)
            chunks = []
            for i in range(0, len(self.o), self.t):
              chunks.append(self.o[i:i + self.t])
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
              for proc in jobs:
                proc.join()
                
              for k,v in enumerate(return_dict.values()):
                 print(k)
                 #self.process_items(v)                  
                 print("open: {0} \t closed: {1} \t ext: {2}".format(len(self.o),len(self.c),len(self.e)))            



    def get_page_items(self,req_url, id, return_dict ):
        print("...req:\t{}".format(req_url))
        """
        if validators.url(req_url):        
          chrome_options = Options()
          chrome_options.add_argument("--headless=new")  # for Chrome >= 109

          browser = webdriver.Chrome(options=chrome_options)
          browser.get(req_url)
          soup = BeautifulSoup(browser.page_source, "html.parser")
          items = soup.find_all("a")
          #print(items)          
          return_dict[id] = items
        """

     

    def process_items(self, items):
        for i in items:
            # extract the url of the page
            url = i.get("href")

            # if the url has not starting protocol and domain, then  adding it
            if not url.startswith("https://"):
                url = "https://" + self.domain + url

            # remove ending forwardslash
            if url[-1] == "/":
                url = url[:-1]


            # if this url is already recorded skip loop
            if url in self.c or url in self.e:
                continue

            # if the url is for external, then save it to the external list
            if url.startswith("https://" + self.domain) == False:
                if url not in self.e:
                    self.e.append(url)
                continue

            if url not in self.o and url not in self.c:
                #print("...add:\t{}".format(url))
                if url not in self.o:
                    self.o.append(url)



if __name__ == "__main__":
    d = GetDomains("myridia.com")
    d.start()


