import requests
import urllib.request
import random

# 浏览器头
headers = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36"
    },
    {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201"
    },
    {
        "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)"
    }
]


class TiebaSpider():
    page = 0

    def __init__(self, tiebaName, page=5):
        """
        输入贴吧名,爬取页数，保存爬取的贴吧页面html
        :param tiebaName: 贴吧名 关键字
        """
        self.tiebaName = tiebaName  # 要保存的贴吧的内容
        # 模拟浏览器请求
        self.userAgent = random.choice(headers)
        # 爬取的页面数
        self.page = page
        # 爬虫的url
        self.url = "https://tieba.baidu.com/f?kw=" + tiebaName + "&ie=utf-8&pn={}"

    '''
    获取需要爬虫的url列表
    '''

    def getUrlList(self):
        urlList = []
        for x in range(0, self.page):
            url2 = self.url.format(x * 50)
            urlList.append(url2)
        return urlList

    '''
    保存到本地
    '''

    def saveHtml(self, url3):
        # 爬出html并转换成字符串
        data = requests.get(url3, headers=self.userAgent).content.decode()

        # 拿到页数（列表引用.index(元素)-->拿到该元素的下标）
        pageHtml = self.getUrlList().index(url3) + 1
        filePath = "../LastProject/spider/file/{}第{}页.html".format(self.tiebaName, pageHtml)
        # 保存html
        with open(filePath, "w", encoding="utf-8") as f:
            f.write(data)

    def run(self):
        urlList = self.getUrlList()
        for x in urlList:
            self.saveHtml(x)
