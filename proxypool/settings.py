# 是否开启网页api
WEBAPI_ENABLED = True

# redis数据库连接信息
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = 'wyx379833553'


# 代理测试站点
TEST_WEB = 'http://www.baidu.com/'
# 代理测试网页超时时间设置
TEST_TIMEOUT = 10
# 检查周期 单位：秒
TEST_PERIOD = 180


# 代理池容量上下限设置
PROXIES_MAX = 100
PROXIES_MIN = 10
# 代理池大小检测周期 单位：秒
PROXIES_LEN_CHECK_PERIOD = 60


# 设置请求handers
BASE_HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


