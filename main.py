#!/usr/bin/env python

import platform, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import validators
import multiprocessing as mp
import networkx as nx
from pyvis.network import Network
import time, datetime
import json
import requests
import csv


class GetDomains:
    def __init__(self, domain="127.0.0.1", protocol="https", proc=3, delay=0.1):
        self.init_time = round(time.time())
        self.domain = domain
        self.protocol = "{0}://".format(protocol)
        self.p = proc
        self.o = []
        self.o.append("http://" + domain)
        self.graph = nx.DiGraph()
        self.c = []
        self.e = []
        self.b = []
        self.delay = delay

    def start(self):
        print("...start")
        mp.set_start_method("spawn")
        while len(self.o):
            time.sleep(self.delay)
            chunks = []
            for i in range(0, len(self.o), self.p):
                chunks.append(self.o[i : i + self.p])
            for i in chunks:
                jobs = []
                manager = mp.Manager()
                return_dict = manager.dict()
                for k, v in enumerate(i):
                    self.c.append(v)
                    self.o.remove(v)

                    p = mp.Process(
                        target=self.get_page_items,
                        args=(v, return_dict),
                    )
                    jobs.append(p)
                    p.start()
                # print("...tread.................")
                msg = """ proc: {0} \t open:{1} \t closed:{2} \t ext:{3} \t broken: {4} \t time: {5}""".format(
                    self.p,
                    len(self.o),
                    len(self.c),
                    len(self.e),
                    len(self.b),
                    datetime.timedelta(seconds=round(time.time()) - self.init_time),
                )

                print(msg)

                for proc in jobs:
                    proc.join()

                for k, v in enumerate(return_dict):
                    # Check if request url was ok
                    if return_dict[v] == False:
                        self.b.append(v)
                        self.c.remove(v)
                        continue

                    self.graph.add_node(v)
                    for ii in return_dict[v]:
                        self.graph.add_node(ii)
                        self.graph.add_edge(v, ii, weight=0.5, value=20)
                    self.process_items(return_dict[v])
            # break

    def get_page_items(self, req_url, return_dict):
        items = []
        if validators.url(req_url):
            check = requests.head(req_url)
            if check.status_code == 200:
                _items = self.request_page(req_url)
                if len(_items):
                    for i in _items:
                        if (
                            i.startswith("https://") == False
                            and i.startswith("http://") == False
                        ):
                            i = "{0}{1}{2}".format(self.protocol, self.domain, i)
                        if i[-1] == "/":
                            i = i[:-1]
                        items.append(i)
            else:
                items = False
        return_dict[req_url] = items

    def request_page(self, req_url):
        items = []
        # print(req_url)
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
        # processing here new items
        for url in items:
            # if this url is already recorded skip loop
            if url in self.c or url in self.e:
                continue

            # if the url is for external, then save it to the external list
            if (
                url.startswith("{0}{1}".format("https://", self.domain)) == False
                and url.startswith("{0}{1}".format("http://", self.domain)) == False
            ):
                if url not in self.e:
                    self.e.append(url)
                continue

            if url not in self.o and url not in self.c:
                # print("...add:\t{}".format(url))
                if url not in self.o:
                    self.o.append(url)

    def complete(self):
        print("...completed!")
        net = Network()
        # with open('GFG', 'w') as f:
        # net.from_nx(self.graph)
        # net.show("graph.html", notebook=False)
        # print(self.c);
        with open("links.csv", "w", newline="") as f:
            writer = csv.writer(f)
            for i in self.c:
                writer.writerow([i])

        with open("broken.csv", "w", newline="") as f:
            writer = csv.writer(f)
            for i in self.b:
                writer.writerow([i])

        with open("external.csv", "w", newline="") as f:
            writer = csv.writer(f)
            for i in self.e:
                writer.writerow([i])


if __name__ == "__main__":
    d = GetDomains("127.0.0.1", "http", 5)
    d.start()
    d.complete()
