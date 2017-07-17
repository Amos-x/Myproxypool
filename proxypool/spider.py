from proxypool.settings import BASE_HEADERS
import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq

class ProxyMetaclass(type):
    """ 定义元类，在类中加入表示爬虫个数和爬虫函数的两个参数
        __crawlfunc__ 和 __crawlfunccount """

    def __new__(cls,name,bases,dct):
        count = 0
        dct['__crawlfunc__'] = []
        for k in dct.keys():
            if 'crawl_' in k:
                dct['__crawlfunc__'].append(k)
                count += 1
        dct['__crawlfunccount__'] = count
        return type.__new__(cls,name,bases,dct)


class ProxyCrawl(object,metaclass=ProxyMetaclass):

    @staticmethod
    def get_page(url, **options):
        """页面请求"""
        headers = dict(BASE_HEADERS, **options)
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
        except:
            print(' 请求网页失败 ', url)
            return None

    def get_proxy_list(self,callback):
        """得到抓取的代理列表"""
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            proxies.append(proxy)
        return proxies

    ## 以下为爬虫函数，可自行修改添加，返回一个proxy生成器。

    def crawl_daili66(self, page_count=4):
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling ', url)
            html = ProxyCrawl.get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_proxy360(self):
        start_url = 'http://www.proxy360.cn/Region/China'
        print('Crawling', start_url)
        html = ProxyCrawl.get_page(start_url)
        if html:
            doc = pq(html)
            lines = doc('div[name="list_proxy_ip"]').items()
            for line in lines:
                ip = line.find('.tbBottomLine:nth-child(1)').text()
                port = line.find('.tbBottomLine:nth-child(2)').text()
                yield ':'.join([ip, port])
    #
    # def crawl_goubanjia(self):
    #     start_url = 'http://www.goubanjia.com/free/gngn/index{page}.shtml'
    #     urls = [start_url.format(page=x) for x in range(1,31)]
    #     for url in urls:
    #         print('crawling ',url)
    #         html = ProxyCrawl.get_page(url)
    #         if html:
    #             doc = pq(html)
    #             tds = doc('td.ip').items()
    #             for td in tds:
    #                 td.find('p').remove()
    #                 yield td.text().replace(' ', '')

    def crawl_xichi(self):
        start_url = 'http://www.xicidaili.com/wt/{page}'
        urls = [start_url.format(page=x) for x in range(1,11)]
        for url in urls:
            print('crawling ', url)
            html = ProxyCrawl.get_page(url)
            if html:
                soup = BeautifulSoup(html,'lxml')
                ip_list = soup.select('#ip_list tr')
                for x in range(1,len(ip_list)):
                    ip = ip_list[x].select('td')[1].get_text()
                    port = ip_list[x].select('td')[2].get_text()
                    yield ':'.join([ip,port])

    def crawl_kuaidaili(self):
        start_url = 'http://www.kuaidaili.com/free/inha/{page}/'
        urls = [start_url.format(page=x) for x in range(1,5)]
        for url in urls:
            print('crawling ',url)
            html = ProxyCrawl.get_page(url)
            if html:
                soup = BeautifulSoup(html,'lxml')
                ip_list = soup.select('tbody tr')
                for x in ip_list:
                    ip = x.select('td[data-title="IP"]')[0].get_text()
                    port = x.select('td[data-title="PORT"]')[0].get_text()
                    yield ':'.join([ip,port])

    def crawl_nianshao(self):
        start_url = 'http://www.nianshao.me/?stype=1&page={page}'
        urls = [start_url.format(page=x) for x in range(1, 21)]
        for url in urls:
            print('crawling', url)
            html = ProxyCrawl.get_page(url)
            if html:
                soup = BeautifulSoup(html, 'lxml')
                ip_list = soup.select('tbody tr')
                for group in ip_list:
                    ip = group.select('td[style="WIDTH:110PX"]')[0].get_text()
                    port = group.select('td[style="WIDTH:40PX"]')[0].get_text()
                    yield ':'.join([ip, port])

if __name__ == '__main__':
    spider = ProxyCrawl()
    a = spider.crawl_nianshao()
    for x in a:
        print(x)
