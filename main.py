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
        self.o = []
        self.o.append("https://" + domain)
        self.o.append("https://" + domain + "/dev_posts/view/4136")
        self.c = []
        self.e = []

    def start(self):
        while len(self.o):
            time.sleep(0.5)

            # items = self.get_page_items(req_url)
            mp.set_start_method("spawn")
            q = mp.Queue()
            q2 = mp.Queue()
            jobs = []

            req_url = self.o[0]
            p = mp.Process(
                target=self.get_page_items,
                args=(
                    q,
                    req_url,
                ),
            )
            jobs.append(p)

            req_url2 = self.o[1]
            p2 = mp.Process(
                target=self.get_page_items,
                args=(
                    q2,
                    req_url2,
                ),
            )
            jobs.append(p2)

            time.sleep(1)
            p.start()
            p2.start()
            print(q.get())
            print(q2.get())
            for i in jobs:
                i.join()
            # p.join()
            break
            # self.process_items(items, req_url)
            """
            list(set(self.o))
            list(set(self.c))
            list(set(self.e))
            print("open: {}".format(len(self.o)))
            print("closed: {}".format(len(self.c)))
            print("ext: {}".format(len(self.e)))
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            """
        else:
            print("...stop")

    def get_page_items(self, q, req_url):
        print("...req:\t{}".format(self.o[0]))

        if req_url in self.c:
            if req_url in self.o:
                self.o.remove(req_url)
            return

        if not validators.url(req_url):
            if req_url in self.o:
                self.o.remove(req_url)
            return

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # for Chrome >= 109

        browser = webdriver.Chrome(options=chrome_options)
        browser.get(req_url)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        items = soup.find_all("a")
        q.put(items)
        return items

    def process_items(self, items, req_url):
        for i in items:
            # extract the url of the page
            url = i.get("href")

            # if the url has not starting protocol and domain, then  adding it
            if not url.startswith("https://"):
                url = "https://" + self.domain + url

            # remove ending forwardslash
            if url[-1] == "/":
                url = url[:-1]

            if req_url == url:
                if req_url not in self.c:
                    self.c.append(req_url)
                if req_url in self.o:
                    self.o.remove(req_url)
                continue

            # if this url is already recorded skip loop
            if url in self.c or url in self.e:
                continue

            # if the url is for external, then save it to the external list
            if url.startswith("https://" + self.domain) == False:
                if url not in self.e:
                    self.e.append(url)
                continue

            if url not in self.o and url not in self.c:
                print("...add:\t{}".format(url))
                if url not in self.o:
                    self.o.append(url)

        if req_url in self.o:
            print("...rm:\t{}".format(req_url))
            self.o.remove(req_url)
            self.c.append(req_url)


if __name__ == "__main__":
    d = GetDomains("myridia.com")
    d.start()


#    if len(sys.argv) == 2:
#        if sys.argv[1].startswith("--token="):
#            a = sys.argv[1].split("=")
#            token = a[1]
#            main(token)
#    else:
#        print("...missing token")
#        print("...example of usage:")
#        print("./main.py --token=ghp_2GcjnhBdwa9v4aoB4ABC123xsxDRBL84JaZDA")
