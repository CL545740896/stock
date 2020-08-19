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


if __name__ == '__main__':
    app = JapApp(worker_num=1, port=9876, log='./access.log')
    app.route('/get_now', GetNowController)
    app.run()
