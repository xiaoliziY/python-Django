import requests
import json
from mysql.sql import mysql

con, cursor = mysql().connect_sql()


class movie_spider():
    def __init__(self, page=4):
        """
        爬取movies title url cover    直接存入mysql
        :param page: 要爬取的页数
        """
        self.page = page

    def run(self):
        for a in range(1, self.page):
            url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start={}"
            url2 = url.format(a * 20)
            data = requests.get(url2).text
            list = json.loads(data)
            movoeList = list.get("subjects")
            for x in movoeList:
                sql = "insert into movies(title,url,cover) values ('%s','%s','%s')"
                data = (x.get("title"), x.get("url"), x.get("cover"))
                cursor.execute(sql % data)
                con.commit()
