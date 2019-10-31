import requests
import urllib3
from queue import Queue
import thread
import threading
from pybloom import ScalableBloomFilter
import re
import time


class Crawler:
    def __init__(self, domain, threads, headers):
        self.domain = domain
        if self.domain[self.domain.__len__() - 1] == '/':
            self.domain = self.domain[0:self.domain.__len__() - 1]
        self.threads = threads
        self.cookies = {}
        self.headers = {}
        self.count = 0
        self.realdomain = ''
        if headers != '':
            self.setheader(headers)
        if 'https' in self.domain:
            self.domain1 = self.domain.replace('https://', '')
            self.domain2 = 'http://' + self.domain1
            self.domain3 = 'http%3A%2F%2F' + self.domain1
            self.domain4 = 'https%3A%2F%2F' + self.domain1
        elif 'http' in self.domain:
            self.domain1 = self.domain.replace('http://', '')
            self.domain2 = 'https://' + self.domain1
            self.domain3 = 'http%3A%2F%2F' + self.domain1
            self.domain4 = 'https%3A%2F%2F' + self.domain1
        else:
            self.domain1 = 'http://' + self.domain
            self.domain2 = 'https://' + self.domain
            self.domain3 = 'http%3A%2F%2F' + self.domain
            self.domain4 = 'https%3A%2F%2F' + self.domain
        self.queue = Queue()
        self.urlqueue = Queue()
        self.lock = threading.RLock()
        self.lock2 = threading.RLock()
        self.bloomfilter = ScalableBloomFilter(initial_capacity=10000, error_rate=0.001, mode=ScalableBloomFilter.LARGE_SET_GROWTH)
        self.bloomfilter2 = ScalableBloomFilter(initial_capacity=10000, error_rate=0.001, mode=ScalableBloomFilter.LARGE_SET_GROWTH)
        self.blacklist = ['<', '{', '\'', '"', '.css', '.jpg', '.mp4', '.png', '.gif', '.avi', '.jpeg', '.ico', '.mp3', '.pdf', 'docx', 'doc', 'bmp', '.rmvb', '.zip', '.rar', '.exe', '.ppt', '.pptx', 'xls']
        self.rule = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    def black(self, url):
        for i in self.blacklist:
            if i in url:
                return False
        return True

    def black2(self, url):
        if '.js' in url and '.jsp' not in url:
            if self.domain in url or self.domain1 in url or self.domain2 in url or self.domain3 in url or self.domain4 in url:
                return True
            else:
                return False
        if '.' + self.domain in url:
            return False
        if '.' + self.domain1 in url:
            return False
        if '.' + self.domain2 in url:
            return False
        if '.' + self.domain3 in url:
            return False
        if '.' + self.domain4 in url:
            return False
        if '=' + self.domain in url:
            return False
        if '=' + self.domain1 in url:
            return False
        if '=' + self.domain2 in url:
            return False
        if '=' + self.domain3 in url:
            return False
        if '=' + self.domain4 in url:
            return False
        if '/' + self.domain in url and '//' + self.domain not in url:
            return False
        if '/' + self.domain1 in url and '//' + self.domain1 not in url:
            return False
        if '/' + self.domain2 in url and '//' + self.domain2 not in url:
            return False
        if '/' + self.domain3 in url and '//' + self.domain3 not in url:
            return False
        if '/' + self.domain4 in url and '//' + self.domain4 not in url:
            return False
        if self.domain in url or self.domain1 in url or self.domain2 in url or self.domain3 in url or self.domain4 in url:
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

    def setcookies(self, cookies):
        index = cookies.find('=')
        index2 = cookies.find(';')
        index3 = 0
        self.lock2.acquire()
        self.cookies.update({cookies[0:index]: cookies[index + 2:index2]})
        self.lock2.release()
        while cookies.find(',', index) > 0:
            index = cookies.find(',', index3)
            while cookies[index + 2] == '0' or cookies[index + 2] == '1' or cookies[index + 2] == '2' or cookies[index + 2] == '3':
                index = cookies.find(',', index + 1)
            index2 = cookies.find('=', index)
            index3 = cookies.find(';', index2)
            self.lock2.acquire()
            self.cookies.update({cookies[index + 2:index2]: cookies[index2 + 1:index3]})
            self.lock2.release()
            index = cookies.find(',', index + 1)
            while cookies[index + 2] == '0' or cookies[index + 2] == '1' or cookies[index + 2] == '2' or cookies[index + 2] == '3':
                index = cookies.find(',', index + 1)

    def stepone(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        r = None
        if 'http' in self.domain:
            try:
                r = requests.get(url=self.domain, verify=False, timeout=(10, 15), headers=self.headers, stream=True)
                self.realdomain = self.domain
            except requests.exceptions.Timeout:
                pass
            except requests.exceptions.ConnectionError:
                pass
            except requests.exceptions.ChunkedEncodingError:
                pass

        else:
            try:
                r = requests.get(url="http://" + self.domain, verify=False, timeout=(10, 15), headers=self.headers, stream=True)
                self.realdomain = 'http://' + self.domain
            except requests.exceptions.Timeout:
                pass
            except requests.exceptions.ConnectionError:
                pass
            except requests.exceptions.ChunkedEncodingError:
                pass
            if r.text.__len__() < 100:
                try:
                    r = requests.get(url="https://" + self.domain, verify=False, timeout=(10, 15), headers=self.headers, stream=True)
                    self.realdomain = 'https://' + self.domain
                except requests.exceptions.Timeout:
                    pass
                except requests.exceptions.ConnectionError:
                    pass
                except requests.exceptions.ChunkedEncodingError:
                    pass
        content = r.text
        if r.headers.get('Set-Cookie'):
            cookies = r.headers['Set-Cookie']
            self.setcookies(cookies)
        href = re.findall(self.rule, content)
        href2 = re.findall('href="(.*?)"', content)
        if href.__len__() > 0:
            for url in href:
                if self.black(url):
                    if url.__len__() > 0:
                        if url[0] == '/':
                            url = url.replace('//', '')
                        url = url.replace('&amp;', '&')
                    if self.black2(url):
                        if not self.bloomfilter.add(url):
                            self.queue.put(url)
        if href2.__len__() > 0:
            for url in href2:
                if '//' not in url:
                    if self.black(url):
                        if url.__len__() > 0:
                            url = url.replace('&amp;', '&')
                            if url[0] != '/':
                                url = '/' + url
                            if self.black2(self.realdomain + url):
                                if not self.bloomfilter.add(self.realdomain + url):
                                    self.queue.put(self.realdomain + url)
        for i in range(0, 100):
            self.queue.put("https://www.baidu.com")
        locks = []
        for i in range(0, self.threads):
            lock = threading.Lock()
            locks.append(lock)
            thread.start_new_thread(self.steptwo, (lock,))
        time.sleep(15)
        for lock in locks:
            while lock.locked():
                pass
        print "success"

    def steptwo(self, minilock):
        minilock.acquire()
        while True:
            self.lock.acquire()
            self.count += 1
            if self.queue.qsize() < 1:
                self.lock.release()
                break
            url = self.queue.get()
            self.lock.release()
            url = url.replace('&amp;', '&')
            if '?' in url and '=' in url:
                self.stepthree(url)
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            if 'http' in url:
                try:
                    if self.headers:
                        r = requests.get(url=url, verify=False, timeout=(10, 15), headers=self.headers, stream=True)
                    else:
                        r = requests.get(url=url, verify=False, timeout=(10, 15), headers=self.headers, stream=True, cookies=self.cookies)
                except requests.exceptions.Timeout:
                    pass
                except requests.exceptions.ConnectionError:
                    pass
                except requests.exceptions.ChunkedEncodingError:
                    pass
            else:
                try:
                    if self.headers:
                        r = requests.get(url="http://" + url, verify=False, timeout=(10, 15), headers=self.headers, stream=True)
                    else:
                        r = requests.get(url="http://" + url, verify=False, timeout=(10, 15), headers=self.headers, stream=True, cookies=self.cookies)
                except requests.exceptions.Timeout:
                    pass
                except requests.exceptions.ConnectionError:
                    pass
                except requests.exceptions.ChunkedEncodingError:
                    pass
                if r.text.__len__() < 100:
                    try:
                        if self.headers:
                            r = requests.get(url="https://" + url, verify=False, timeout=(10, 15), headers=self.headers, stream=True)
                        else:
                            r = requests.get(url="https://" + url, verify=False, timeout=(10, 15), headers=self.headers, stream=True, cookies=self.cookies)
                    except requests.exceptions.Timeout:
                        pass
                    except requests.exceptions.ConnectionError:
                        pass
                    except requests.exceptions.ChunkedEncodingError:
                        pass
            if r.status_code == 200:
                try:
                    content = r.text
                except requests.exceptions.ConnectionError:
                    continue
                except AttributeError:
                    continue
                except requests.exceptions.ChunkedEncodingError:
                    continue
            else:
                continue
            if r.headers.get('Set-Cookie'):
                cookies = r.headers['Set-Cookie']
                self.setcookies(cookies)
            href = re.findall(self.rule, content)
            href2 = re.findall('href="(.*?)"', content)
            if href.__len__() > 0:
                for url in href:
                    if self.black(url):
                        if url.__len__() > 0:
                            if url[0] == '/':
                                url = url.replace('//', '')
                            url = url.replace('&amp;', '&')
                        if self.black2(url):
                            if not self.bloomfilter.add(url):
                                self.queue.put(url)
            if href2.__len__() > 0:
                for url in href2:
                    if '//' not in url:
                        if self.black(url):
                            if url.__len__() > 0:
                                url = url.replace('&amp;', '&')
                                if url[0] != '/':
                                    url = '/' + url
                                if self.black2(self.realdomain + url):
                                    if not self.bloomfilter.add(self.realdomain + url):
                                        self.queue.put(self.realdomain + url)
            if self.count > 10000:
                break
        minilock.release()

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
            self.urlqueue.put(url[0:url.__len__() - 1])
            print url[0:url.__len__() - 1]

crawler = Crawler("https://tieba.baidu.com", 20, '''''')
crawler.stepone()
