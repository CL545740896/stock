from agileutil.japronto import JapApp, JapController
from lib.point import Point


class BaseController(JapController):
    ...


class GetNowController(BaseController):
    def handle(self):
        try:
            code = self.param('code')
            remote = self.remoteAddr()
            self.logInfo(f'code:{code}, remote:{remote}')
            now = Point.getNow(code)
            return now.toString()
        except Exception as ex:
            return str(ex)


class GetStockListController(BaseController):
    def handle(self):
        f = open('./data/stock_list.json', 'r')
        content = f.read()
        f.close()
        return content

def main():
    app = JapApp(worker_num=1, port=9876, log='./access.log')
    app.route('/get_now', GetNowController)
    app.route('/get_stock_list', GetStockListController)
    app.run()


if __name__ == '__main__':
    while 1:
        try:
            main()
        except Exception as ex:
            print(ex)
