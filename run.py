from proxypool.web_api import app
from proxypool.schedule import Schedule
from proxypool.settings import WEBAPI_ENABLED

def main():
    s = Schedule()
    s.run()
    if WEBAPI_ENABLED:
        app.run()

if __name__ == '__main__':
    main()