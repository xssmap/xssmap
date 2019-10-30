import requests
import urllib3
from queue import Queue
import thread
import threading
import time
from pybloom import ScalableBloomFilter
import re


class Crawler:
    def __init__(self, domain, threads, headers):
        self.domain = domain
        self.threads = threads
        self.headers = {}
        if headers != '':
            self.setheader(headers)
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

    def setheader(self, url):
        index = 0
        l = 0
        url += '\n'
        while index < url.__len__() - 1:
            index = url.find(':', index)
            index1 = url.find('\n', index)
            index2 = url.find('\n', index1 + 1)
            if ':' not in url[index1:index2]:
                while ':' not in url[index1:index2]:
                    index3 = index2
                    index2 = url.find('\n', index2 + 1)
                    if index2 <= 0:
                        index2 = index3
                        break
            else:
                index2 = index1
            if url[index + 1] != ' ':
                self.headers.update({url[l:index]: url[index + 1:index2].replace('\n', '')})
            else:
                self.headers.update({url[l:index]: url[index + 2:index2].replace('\n', '')})
            index = index2 + 1
            l = index

    def stepone(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        if 'http' in self.domain:
            try:
                r = requests.get(url=self.domain, verify=False, timeout=15, headers=self.headers)
            except requests.exceptions.Timeout:
                pass
            except requests.exceptions.ConnectionError:
                pass
        else:
            try:
                r = requests.get(url="http://" + self.domain, verify=False, timeout=15, headers=self.headers)
            except requests.exceptions.Timeout:
                pass
            except requests.exceptions.ConnectionError:
                pass
            if r.text.__len__() < 100:
                try:
                    r = requests.get(url="https://" + self.domain, verify=False, timeout=15, headers=self.headers)
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
                        url = url.replace('&amp;', '&')
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
        for i in range(0, self.threads):
            thread.start_new_thread(self.steptwo, ())
        time.sleep(99999)

    def steptwo(self):
        while True:
            self.lock.acquire()
            url = self.queue.get()
            self.lock.release()
            url = url.replace('&amp;', '&')
            if '?' in url and '=' in url:
                self.stepthree(url)
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            if 'http' in url:
                try:
                    r = requests.get(url=url, verify=False, timeout=15, headers=self.headers)
                except requests.exceptions.Timeout:
                    pass
                except requests.exceptions.ConnectionError:
                    pass
            else:
                try:
                    r = requests.get(url="http://" + url, verify=False, timeout=15, headers=self.headers)
                except requests.exceptions.Timeout:
                    pass
                except requests.exceptions.ConnectionError:
                    pass
                if r.text.__len__() < 100:
                    try:
                        r = requests.get(url="https://" + url, verify=False, timeout=15, headers=self.headers)
                    except requests.exceptions.Timeout:
                        pass
                    except requests.exceptions.ConnectionError:
                        pass
            content = r.text
            if 'oOUFFxQ312' in content:
                print url
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
        if not self.bloomfilter2.add(newurl):
            self.urlqueue.put(newurl)
            print newurl

crawler = Crawler("http://dushu.qq.com", 2, '''''')
crawler.stepone()
