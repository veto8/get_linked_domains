#!/usr/bin/env python

import platform, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import validators
import multiprocessing as mp
import networkx as nx
from pyvis.network import Network
import time,datetime


class GetDomains:
    def __init__(self, domain="127.0.0.1", proc=3):
        self.init_time = round(time.time())
        self.domain = domain
        self.p = proc
        self.o = []
        self.o.append("http://" + domain)
        self.graph = nx.DiGraph()
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
                      return_dict
                   ),
                 )
                jobs.append(p)
                p.start()                
              #print("...tread.................")
              print("proc: {0}\t open:{1}\t closed:{2}\t ext:{3}\t time passed: {4}".format(self.p,len(self.o),len(self.c),len(self.e),datetime.timedelta(seconds=round(time.time()) - self.init_time)))    
              
              for proc in jobs:
                proc.join()
                
              for k,v in enumerate(return_dict):
                 #print(v)
                 #print(return_dict[v])                  
                 self.graph.add_node(v)
                 for ii in return_dict[v]:
                   self.graph.add_node(ii)
                   self.graph.add_edge(v,ii,weight=.5, value=20)
                 self.process_items(return_dict[v])                  
            #break



    def get_page_items(self,req_url, return_dict ):
      _items = self.request_page(req_url)
      items = []
      if len(_items):
        for i in _items:
          if not i.startswith("http://"):
            i = "http://{0}{1}".format(self.domain , i)
          if i[-1] == "/":
            i = i[:-1]            
          items.append(i)
        return_dict[req_url] = items

    def request_page(self,req_url ):
        items = []        
        if validators.url(req_url):
          chrome_options = Options()
          chrome_options.add_argument("--headless=new")  # for Chrome >= 109
          browser = webdriver.Chrome(options=chrome_options)
          browser.get(req_url)
          soup = BeautifulSoup(browser.page_source, "html.parser")
          _items = soup.find_all("a")
          for i in _items:
            items.append(i.get("href"))
        return items

    def process_items(self, items):
        for url in items:
            
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
        net  = Network()        
        net.from_nx(self.graph)
        net.show("graph.html",notebook=False)        
        #print(self.c);

if __name__ == "__main__":
    d = GetDomains("127.0.0.1", 8)
    d.start()
    d.complete()    



