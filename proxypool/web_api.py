from proxypool.Redis import RedisClient
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'welcome to ProxyPool System'

@app.route('/get')
def get():
    conn = RedisClient()
    return conn.pop()

if __name__ == '__main__':
    app.run()