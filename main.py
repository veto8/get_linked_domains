#!/usr/bin/env python

import platform, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class GetDomains:
    def __init__(self, domain="myridia.com"):
        self.domain = domain
        self.o = []
        self.o.append("https://" + domain)
        self.c = []
        self.e = []

    def start(self):
        while len(self.o):
            time.sleep(0.5)
            print("...browser: {}".format(self.o[0]))
            self.browse_page(self.o[0])
            print("...open: {}".format(len(self.o)))
            print("...closed: {}".format(len(self.c)))
            print("...ext: {}".format(len(self.e)))
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        else:
            print("...stop")

    def browse_page(self, req_url):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # for Chrome >= 109

        browser = webdriver.Chrome(options=chrome_options)
        browser.get(req_url)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        items = soup.find_all("a")

        for i in items:
            url = i.get("href")
            if not url.startswith("https://"):
                url = "https://" + self.domain + url
                # print(url)
            if url[-1] == "/":
                url = url[:-1]
            if url.startswith("https://" + self.domain):
                if url == req_url:
                    if url not in self.c and url not in self.o:
                        self.c.append(url)
                else:
                    if url not in self.o and url not in self.c:
                        self.o.append(url)
            else:
                if url not in self.e:
                    self.e.append(url)

            if req_url in self.o:
                self.o.remove(req_url)
                if url not in self.c:
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
