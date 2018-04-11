"""
电影天堂电影名和下载链接爬取
"""
import requests
import time
from bs4 import BeautifulSoup
import re

from requests import HTTPError

site = 'http://www.ygdy8.net'
lineNo = 1
movie_list = []
headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/64.0.3282.140 Safari/537.36'
    }


def get_soup(url):
    try:
        r = requests.get(url, headers=headers)
        r.encoding = 'gb18030'
        return BeautifulSoup(r.text, "html.parser")
    except HTTPError as e:
        print(e)


def get_movie_detail(table):
    try:
        result = {}
        result['电影译名'] = table.text
        result['详情链接'] = site + table.get('href')
        soup = get_soup(result['详情链接'])
        result['下载链接'] = get_download_link(soup)
        result['豆瓣评分'] = get_score(soup)
        movie_list.append(result)
    except Exception as e:
        print(e)


def get_download_link(soup):
    return soup.find('td', attrs={"style": "WORD-WRAP: break-word"}).find('a')['href']


def get_score(soup):
    score = re.findall(r"豆瓣评分　(.+?)/10", soup.text)
    if len(score) > 0:
        return str(score[0]) + '/10'
    else:
        return None


def save_info():
    file = open('data.txt', 'a')
    for movie in movie_list:
        movie_str = str(movie)
        print('movie info:', movie_str)
        global lineNo
        file.write('(' + str(lineNo) + ') ' + movie_str)
        file.write('\n')
        file.write('——————————————————————————————————')
        file.write('\n')
        lineNo += 1
    file.close()


def get_page_resource(url):
    soup = get_soup(url)
    tables = soup.select('.ulink')
    print('为了防止反爬虫，设置间隔访问时间，请耐心等待...')
    for table in tables:
        get_movie_detail(table)
        time.sleep(1)


if __name__ == '__main__':
    for index in range(1, 3):
        url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_' + \
            str(index) + '.html'
        get_page_resource(url)
        time.sleep(5)
    for i in movie_list:
        print(i)
    # if len(movie_list) > 0:
    #     save_info()