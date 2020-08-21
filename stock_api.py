from agileutil.sanic import SanicApp, SanicController
from lib.point import Point


class BaseController(SanicController):
    ...


class GetNowController(BaseController):
    async def handle(self):
        try:
            code = self.param('code')
            remote = self.remoteAddr()
            self.logInfo(f'code:{code}, remote:{remote}')
            now = Point.getNow(code)
            return now.toString()
        except Exception as ex:
            return str(ex)


class GetStockListController(BaseController):
    async def handle(self):
        content = ''
        with open('./data/stock_list.json', 'r') as f:
            content = f.read()
        return content


class MyController(BaseController):
    async def handle(self):
        remote = self.remoteAddr()
        return 'Your IP:' + remote


def main():
    app = SanicApp(worker_num=1, port=9876, log='./access.log')
    app.route('/get_now', GetNowController)
    app.route('/get_stock_list', GetStockListController)
    app.route('/my', MyController)
    app.run()


if __name__ == '__main__':
    while 1:
        try:
            main()
        except Exception as ex:
            print(ex)
