"""
电影天堂电影名和下载链接爬取
"""
import requests
import time
from bs4 import BeautifulSoup
import re

site = 'http://www.ygdy8.net'
lineNo = 1
movie_list = []


class Movie:
    def __init__(self, name, url, score, link):
        self.name = name
        self.url = url
        self.score = score
        self.link = link

    def __str__(self):
        return '%s,\t%s分,\t%s' % (self.name, self.score, self.link)
    __repr__ = __str__


def get_soup(url):
    r = requests.get(url)
    r.encoding = 'gb18030'
    return BeautifulSoup(r.text, "html.parser")


def get_movie_detail(url):
    soup = get_soup(url)
    tables = soup.select('.ulink')
    for table in tables:
        result = {}
        result['电影译名'] = table.text
        result['详情链接'] = site + table.get('href')
        soup = get_soup(result['详情链接'])
        result['下载链接'] = get_download_link(soup)
        result['豆瓣评分'] = get_score(soup)
        movie_list.append(result)


def get_download_link(soup):
    return soup.find('td', attrs={"style": "WORD-WRAP: break-word"}).find('a')['href']


def get_score(soup):
    score = re.findall(r"豆瓣评分　(.+?)/10", soup.text)
    if len(score) > 0:
        return str(score[0]) + '/10'
    else:
        return None


def save_info():
    fileObj = open('data.txt', 'a')
    for movie in movie_list:
        movie_str = str(movie)
        print('movie info:', movie_str)
        global lineNo
        fileObj.write('(' + str(lineNo) + ') ' + movie_str)
        fileObj.write('\n')
        fileObj.write('——————————————————————————————————')
        fileObj.write('\n')
        lineNo += 1
    fileObj.close()


def get_page_resource(url):
    get_movie_detail(url)
    # if len(movie_list) > 0:
    #     save_info()


if __name__ == '__main__':
    for index in range(1, 2):
        url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_' + \
            str(index) + '.html'
        get_page_resource(url)
        time.sleep(5)