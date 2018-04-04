import re
from urllib import request
from urllib import error


class DouBanSpider(object):
    """
    本类主要用于抓取豆瓣中的电影
    Attributes:
        page:       表示当前所处理的页面
        cur_url:    表示当前准备抓取页面的url
        datas：     存储处理好的电影名称
        _top_num:   用于记录当前的top号码
    """

    def __init__(self):
        self.page = 1
        self.cur_url = 'http://movie.douban.com/top250?start={page}&filter='
        self.datas = []
        self._top_num = 1
        print('正在请求资源，请稍等......')

    def get_page(self, cur_page):
        """
        param cur_page: 表示当前处理页
        return: 返回抓取到的整个页面的HTML（unicode编码）
        """
        url = self.cur_url
        try:
            # 因为一个页面有25部电影，所以这里 “* 25”
            page = request.urlopen(url.format(page=(cur_page - 1) * 25)).read().decode("utf-8")
        except error.URLError as e:
            if hasattr(e, 'code'):
                print("HTTPError: the server couldn`t deal with the request")
                print("Error code: %s" % e.code)
            elif hasattr(e, 'reason'):
                print("URLError: failed to reach the server")
                print("Reason : %s" % e.reason)
        return page

    def find_title(self, page):
        tmp_data = []
        average_data = []
        result_data = []
        movie_items = re.findall(r'<span.*?class="title">(.*?)</span>', page, re.S)
        movie_average = re.findall(r'property="v:average">(.*?)</span>', page, re.S)
        for index, item in enumerate(movie_average):
            average_data.append('豆瓣评分: ' + item)
        for index, item in enumerate(movie_items):
            if item.find('&nbsp'):
                tmp_data.append("Top" + str(self._top_num) + " " + '《' + item + '》')
                self._top_num += 1
        for i, item in enumerate(tmp_data):
            result_data.append(tmp_data[i] + '-----' + average_data[i])
        self.datas.extend(result_data)

    def start_spider(self):
        while self.page <= 10:
            page = self.get_page(self.page)
            self.find_title(page)
            self.page += 1


def main():
    spider = DouBanSpider()
    spider.start_spider()
    for item in spider.datas:
        print(item)


if __name__ == '__main__':
    main()