from urllib.request import urlretrieve

import requests
# html = requests.get('http://pc.33egg.com:9101/?u=31899&k=xx')
from bs4 import BeautifulSoup

html = requests.get('http://pc.33egg.com:9101/play.php?id=141')
soup = BeautifulSoup(html.text, 'html.parser')
url = soup.select('.playbox-l')[0].select('.playContent source')[0]['src']
urlretrieve(url, 'xxx.mp4')