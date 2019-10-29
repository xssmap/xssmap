import requests
import re
import urllib3
from queue import Queue
import thread
import threading
import time
from pybloom import ScalableBloomFilter


class Crawler:
    def __init__(self, domain):
        self.domain = domain
        if 'https' in self.domain:
            self.domain1 = self.domain.replace('https://', '')
            self.domain2 = 'http://' + self.domain1
        elif 'http' in self.domain:
            self.domain1 = self.domain.replace('http://', '')
            self.domain2 = 'https://' + self.domain1
        else:
            self.domain1 = 'http://' + self.domain
            self.domain2 = 'https://' + self.domain
        self.queue = Queue()
        self.lock = threading.RLock()
        self.bloomfilter = ScalableBloomFilter(initial_capacity=1000, error_rate=0.001, mode=ScalableBloomFilter.LARGE_SET_GROWTH)
        self.blacklist = ['.css', '.js', '.jpg', '.mp4', '.png', '.gif', '.avi', '.jpeg', '.ico', '.mp3']

    def black(self, url):
        for i in self.blacklist:
            if i in url:
                return False
        return True

    @staticmethod
    def black2(domain, url):
        if '.' + domain in url:
            return False
        if '=' + domain in url:
            return False
        if '/' + domain in url:
            return False
        if domain in url:
            return True
        else:
            return False

    def stepone(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        if 'http' in self.domain:
            r = requests.get(url=self.domain, verify=False)
        else:
            r = requests.get(url="http://" + self.domain, verify=False)
            if r.text.__len__() < 100:
                r = requests.get(url="https://" + self.domain, verify=False)
        content = r.text
        href = re.findall('href="(.*?)"', content)
        if href.__len__() > 0:
            for url in href:
                if self.black(url):
                    if url.__len__() > 0:
                        if url[0] == '/':
                            url = url.replace('//', '')
                    if self.black2(self.domain, url):
                        if not self.bloomfilter.add(url):
                            self.queue.put(url)
                        continue
                    if self.black2(self.domain1, url):
                        if not self.bloomfilter.add(url):
                            self.queue.put(url)
                        continue
                    if self.black2(self.domain2, url):
                        if not self.bloomfilter.add(url):
                            self.queue.put(url)
                        continue
        for i in range(0, 20):
            thread.start_new_thread(self.steptwo, ())
        time.sleep(1000)

    def steptwo(self):
        while True:
            self.lock.acquire()
            url = self.queue.get()
            print url
            self.lock.release()
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            if 'http' in url:
                r = requests.get(url=url, verify=False)
            else:
                r = requests.get(url="http://" + url, verify=False)
                if r.text.__len__() < 100:
                    r = requests.get(url="https://" + url, verify=False)
            content = r.text
            href = re.findall('href="(.*?)"', content)
            if href.__len__() > 0:
                for url in href:
                    if url.__len__() > 0:
                        if url[0] == '/':
                            url = url.replace('//', '')
                    if self.black(url):
                        if self.black2(self.domain, url):
                            if not self.bloomfilter.add(url):
                                self.queue.put(url)
                            continue
                        if self.black2(self.domain1, url):
                            if not self.bloomfilter.add(url):
                                self.queue.put(url)
                            continue
                        if self.black2(self.domain2, url):
                            if not self.bloomfilter.add(url):
                                self.queue.put(url)
                            continue

crawler = Crawler("dushu.qq.com")
crawler.stepone()
