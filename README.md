Myproxypool

仅用于学习交流，By Amos  
使用redis数据库维护的一个免费代理池  
可作为安装库使用，下载后将项目复制到你的python库搜索路径下 如：~\Python36\Lib\site-packages  


使用方法：  
ps:使用前，请先根据自己的电脑进行设置。   
import Myproxypool  #导入库   
Myproxypool.run() #启动并维护代理池   


设置（在使用之前进行）：   
目前没有提供外部调用的设置接口。   
打开原文件，修改设置即可，文件地址：Myproxypool\proxypool\settings.py   
内容如下：   
是否开启网页api，若开启，请求本地5000端口，返回一个代理IP。请求地址为：localhost:5000/get   
WEBAPI_ENABLED = False   

redis数据库连接信息   
REDIS_HOST = 'localhost'  # redis数据库连接地址   
REDIS_PORT = 6379   # redis数据库端口   
REDIS_PASSWORD = 'xxxxxxx'  # redis数据库密码   

代理测试站点   
TEST_WEB = 'http://www.baidu.com/'  # 用于测试代理是否可用的站点，可更具需求自定义   
代理测试网页超时时间设置   
TEST_TIMEOUT = 10   
检查周期 单位：秒   
TEST_PERIOD = 60   

代理池容量上下限设置   
PROXIES_MAX = 100  # 代理池容量上限   
PROXIES_MIN = 10  # 代理池容量下限   
代理池大小检测周期 单位：秒   
PROXIES_LEN_CHECK_PERIOD = 30   

设置默认请求handers   
BASE_HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}