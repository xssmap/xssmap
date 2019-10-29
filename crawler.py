import requests
import re
import urllib3


class Crawler:
    def __init__(self, domain):
        self.domain = domain
        self.urls = []

    def stepone(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        r = requests.get(url=self.domain, verify=False)
        content = r.text
        href = re.findall('href="(.*?)"', content)
        for url in href:
            if self.domain in url:
                print url


crawler = Crawler("https://www.qq.com")
crawler.stepone()
