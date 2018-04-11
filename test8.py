from urllib.request import urlretrieve

import requests
# html = requests.get('http://pc.33egg.com:9101/?u=31899&k=xx')
# print(html.text)
from bs4 import BeautifulSoup


def back(a, b, c):
    per = 100*a*b/c
    if per > 100:
        per = 100
        print('下载完成！')
    print('%.2f%%' % per)


html = requests.get('http://pc.33egg.com:9101/play.php?id=57')
soup = BeautifulSoup(html.text, 'html.parser')
url = soup.select('.playbox-l')[0].select('.playContent source')[0]['src']
urlretrieve(url, 'xxx.mp4', back)