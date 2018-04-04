"""
@张松顺
time:2018-04-02
新浪国内新闻爬虫
"""
import json
import sqlite3
from datetime import datetime

import pandas
import requests
from bs4 import BeautifulSoup


commentURL = 'http://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=gn&newsid=comos-{}&\
                group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread=1'


def getCommentCounts(newsurl):
    """获取评论数"""
    newsid = newsurl.split('/')[-1].lstrip('doc-i').rstrip('.shtml')
    comments = requests.get(commentURL.format(newsid))
    jd = json.loads(comments.text)['result']['count']['total']
    return jd


def getNewsDetail(newsurl):
    """获取新闻的详细信息，存入到字典中"""
    result = {}
    res = requests.get(newsurl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    result['title'] = soup.select('.main-title')[0].text
    time_source = soup.select('.date-source')[0].contents[1].text.strip()
    result['dt'] = datetime.strptime(time_source, '%Y年%m月%d日 %H:%M')
    result['newssource'] = soup.select('.date-source')[0].select('.source')[0].text
    result['article'] = ' '.join([p.text.strip() for p in soup.select('.article p')[:-1]])
    result['editor'] = soup.select('.show_author')[0].text.lstrip('责任编辑：')
    result['comments'] = getCommentCounts(newsurl)
    return result


def paesrListLinks(url):
    """取每个分页中的一页"""
    newsDetails = []
    res = requests.get(url)
    jd = json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');'))
    for news in jd['result']['data']:
        newsDetails.append(getNewsDetail(news['url']))
    return newsDetails


url = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&\
        cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&\
        show_num=22&tag=1&format=json&page={}&callback=newsloadercallback&_=1522653149122' # 分页的URL


def get_news_total(page):
    """定义需要新浪国内新闻中前几页的新闻"""
    news_total = []
    for i in range(1, page):
        newsurl = url.format(i)
        newsary = paesrListLinks(newsurl)
        news_total.extend(newsary)
    return news_total


def save2sql(news_total):
    """将获取的新闻信息保存到数据库中"""
    df = pandas.DataFrame(news_total)
    df.to_excel('news.xlsx')
    with sqlite3.connect('news.sqlite') as db:
        df.to_sql('news', con=db)


def query_sql():
    """显示数据库中的新闻信息"""
    with sqlite3.connect('news.sqlite') as db:
        print(pandas.read_sql_query('select * from news', con =db))


if __name__ == '__main__':
    # get_news_total中的参数决定爬取几页的新闻
    news_total = get_news_total(3)
    for news in news_total:
        print(news)
    # query_sql()

