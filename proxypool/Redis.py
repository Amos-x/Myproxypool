import redis
from proxypool.settings import REDIS_PORT,REDIS_HOST,REDIS_PASSWORD

class RedisClient(object):

    def __init__(self):
        """初始化连接redis"""
        if REDIS_PASSWORD:
            self.client = redis.Redis(REDIS_HOST,REDIS_PORT,1,REDIS_PASSWORD)
        else:
            self.client = redis.Redis(REDIS_HOST,REDIS_PORT,1)

    def get(self,count=1):
        """从Redis中取出代理"""
        proxies = [proxy.decode('utf-8') for proxy in self.client.lrange('proxies',0,count-1)]
        self.client.ltrim('proxies',count,-1)
        return proxies

    def put(self,proxy):
        """放代理入redis"""
        proxies = [x.decode('utf-8') for x in self.client.lrange('proxies', 0, -1)]
        if proxy not in proxies:
            self.client.rpush('proxies', proxy)

    def pop(self):
        """从右边取第一个代理"""
        try:
            return self.client.rpop('proxies').decode('utf-8')
        except:
            print('代理列表为空')

    @property
    def queue_len(self):
        """队列长度"""
        return self.client.llen('proxies')

    def flush(self):
        """清楚所有数据"""
        self.client.flushdb()

if __name__ == '__main__':
    conn = RedisClient()

