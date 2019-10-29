import requests
import urllib3
from queue import Queue
import thread
import threading
import time
from pybloom import ScalableBloomFilter
import re


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
        self.urlqueue = Queue()
        self.lock = threading.RLock()
        self.bloomfilter = ScalableBloomFilter(initial_capacity=10000, error_rate=0.001, mode=ScalableBloomFilter.LARGE_SET_GROWTH)
        self.bloomfilter2 = ScalableBloomFilter(initial_capacity=10000, error_rate=0.001, mode=ScalableBloomFilter.LARGE_SET_GROWTH)
        self.blacklist = ['.css', '.jpg', '.mp4', '.png', '.gif', '.avi', '.jpeg', '.ico', '.mp3']
        self.rule = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    def black(self, url):
        for i in self.blacklist:
            if i in url:
                return False
        return True

    def stepthree(self, url):
        url += '&'
        index2 = url.find('=') + 1
        newurl = url[0:url.find('=') + 1] + 'xss'
        while True:
            index1 = url.find('&', index2 + 1)
            index2 = url.find('=', index2 + 1)
            if index1 > 0 and index2 > 0:
                newurl += url[index1:index2] + '=xss'
            else:
                break
        print newurl

    def black2(self, domain, url):
        if '.js' in url and '.jsp' not in url:
            if self.domain in url or self.domain1 in url or self.domain2 in url:
                return True
            else:
                return False
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
            try:
                r = requests.get(url=self.domain, verify=False, timeout=15)
            except requests.exceptions.Timeout:
                pass
            except requests.exceptions.ConnectionError:
                pass
        else:
            try:
                r = requests.get(url="http://" + self.domain, verify=False, timeout=15)
            except requests.exceptions.Timeout:
                pass
            except requests.exceptions.ConnectionError:
                pass
            if r.text.__len__() < 100:
                try:
                    r = requests.get(url="https://" + self.domain, verify=False, timeout=15)
                except requests.exceptions.Timeout:
                    pass
                except requests.exceptions.ConnectionError:
                    pass
        content = r.text
        href = re.findall(self.rule, content)
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
            self.lock.release()
            if '?' in url and '=' in url:
                self.stepthree(url)
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            if 'http' in url:
                r = requests.get(url=url, verify=False, timeout=15)
            else:
                r = requests.get(url="http://" + url, verify=False, timeout=15)
                if r.text.__len__() < 100:
                    r = requests.get(url="https://" + url, verify=False, timeout=15)
            content = r.text
            href = re.findall(self.rule, content)
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
crawler.stepthree("http://www.baidu.com/?abc=1fesgfoij&b=fdsaiofhji&c=12&d=&e1=fsda")
