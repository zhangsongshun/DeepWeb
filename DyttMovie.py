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
        result['下载链接'] = get_download_link(result['详情链接'])
        movie_list.append(result)
    for i in movie_list[0:1]:
        soup = get_soup(i['详情链接'])
        print(soup)

    # for table in tables:
    #     print(table)
    #     nameA = table.find('a', text=re.compile("《"))
    #     lsit.append(nameA)
    #     # print(nameA)
    #     td = table.find('td', text=re.compile("IMD"))
    #     if td is not None:
    #         scoreStr = re.findall(r"评分 (.+?)/10", td.text)
    #         if(len(scoreStr) > 0):
    #             try:
    #                 score = float(scoreStr[0])
    #                 if(score > 8):
    #                     name = nameA.text
    #                     url = site + nameA['href']
    #                     # print('url:', url)
    #                     # print('title:', name)
    #                     # print('score:', score)
    #                     downloadLink = getDownloadLink(url)
    #                     movie = Movie(name, url, score, downloadLink)
    #                     resultList.append(movie)
    #             except:
    #                 print('error !!')
    # return resultList


def get_download_link(url):
    soup = get_soup(url)
    return soup.find('td', attrs={"style": "WORD-WRAP: break-word"}).find('a')['href']


def get_score(soup):
    pass


def saveInfo(movieList):
    fileObj = open('data.txt', 'a')
    for movie in movieList:
        movie_str = str(movie)
        print('movie info:', movie_str)
        global lineNo
        fileObj.write('(' + str(lineNo) + ') ' + movie_str)
        fileObj.write('\n')
        fileObj.write(
            '————————————————————————————————————————————————————————————————————————————————————————————————')
        fileObj.write('\n')
        lineNo += 1
    fileObj.close()


def getPageResource(url):
    get_movie_detail(url)

    # if len(resultList) > 0:
    #     saveInfo(resultList)


if __name__ == '__main__':
    for index in range(1, 2):
        url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_' + \
            str(index) + '.html'
        getPageResource(url)
        time.sleep(5)