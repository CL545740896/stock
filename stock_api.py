from agileutil.japronto import JapApp, JapController
from lib.point import Point


class BaseController(JapController):
    ...


class GetNowController(BaseController):
    def handle(self):
        code = self.param('code')
        now = Point.getNow(code)
        return now.toString()


if __name__ == '__main__':
    app = JapApp(worker_num=4, port=9876)
    app.route('/get_now', GetNowController)
    app.run()
