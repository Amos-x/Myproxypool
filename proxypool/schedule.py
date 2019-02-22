from proxypool.settings import TEST_WEB,TEST_TIMEOUT,PROXIES_MAX,TEST_PERIOD,PROXIES_LEN_CHECK_PERIOD,PROXIES_MIN
from proxypool.Redis import RedisClient
from proxypool.spider import ProxyCrawl
from multiprocessing import Process
import asyncio
import aiohttp
import time


class ProxyTest(object):
    """
    代理检测
    """
    def __init__(self):
        self.test_proxies_list = None
        self.usable_proxies = []

    def set_test_proxies(self,proxies):
        self.test_proxies_list = proxies
        self.conn = RedisClient()

    async def test_single_proxy(self,proxy):
        """一个异步检测函数"""
        async with aiohttp.ClientSession() as session:
            try:
                real_proxy = 'http://' + proxy
                async with session.get(TEST_WEB, proxy=real_proxy, timeout=TEST_TIMEOUT) as response:
                    if response.status == 200:
                        self.conn.put(proxy)
            except:
                pass

    def test(self):
        """异步检测启动函数"""
        try:
            if self.test_proxies_list:
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in self.test_proxies_list]
                loop.run_until_complete(asyncio.wait(tasks))
        except:
            print('异步检测错误')


class ProxyPoolAdder(object):
    """
    向代理池中添加代理
    """
    def __init__(self):
        self.conn = RedisClient()
        self.crawler = ProxyCrawl()
        self.proxies_max = PROXIES_MAX
        self.test = ProxyTest()

    def isover_max(self):
        """判断是否超出设置的代理池最大容量"""
        if self.conn.queue_len >= self.proxies_max:
            return True
        else:
            return False

    def add_to_queue(self):
        """添加代理入代理池"""
        proxies_count = 0
        while not self.isover_max():
            for spider in self.crawler.__crawlfunc__:
                proxies_list = self.crawler.get_proxy_list(spider)
                if proxies_list:
                    self.test.set_test_proxies(proxies_list)
                    self.test.test()
                proxies_count += len(proxies_list)
                if self.isover_max():
                    break
            if proxies_count == 0:
                print('爬取代理出错，请检查')


class Schedule(object):

    @staticmethod
    def test():
        conn = RedisClient()
        tester = ProxyTest()
        # 不断循环测试
        while True:
            count = int(0.5*conn.queue_len)
            if count==0:
                time.sleep(TEST_PERIOD)
                continue
            print('开始检测...')
            proxies_list = conn.get(count=count)
            tester.set_test_proxies(proxies_list)
            tester.test()
            print('检测结束，睡眠一个周期...')
            time.sleep(TEST_PERIOD)

    @staticmethod
    def crawl():
        conn = RedisClient()
        adder = ProxyPoolAdder()
        # 不断进行代理添加
        while True:
            if conn.queue_len <= PROXIES_MIN:
                print('开始爬取代理...')
                adder.add_to_queue()
                print('代理池容量达到上限，爬取结束，睡眠...')
            time.sleep(PROXIES_LEN_CHECK_PERIOD)

    def run(self):
        print('代理池启动')
        test_pro = Process(target=Schedule.test)
        crawl_pro = Process(target=Schedule.crawl)
        test_pro.start()
        crawl_pro.start()


if __name__ == '__main__':
    r = ProxyTest()
