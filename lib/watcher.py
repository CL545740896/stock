from point import Point
from kline_sqlite import KLineSqlite
import requests

'''
监控一只股票
在满足买入阀值时，发送买入通知
在满足卖出阀值时，发送卖出通知
'''

class Watcher:

    STATUS_RUN = 1
    STATUS_STOP = 2

    def __init__(self, code, bugPriceList = [], salePriceList[], notifyUrl = ''):
        self.code = code
        self.bugPriceList = bugPriceList
        self.salePriceList = salePriceList
        self.notifyUrl = notifyUrl
        self.status = Watcher.STATUS_STOP 

    def start(self):
        self.status = Watcher.STATUS_RUN
        while 1:
            if self.status == Watcher.STATUS_STOP:
                print('watcher stopped')
                return
            self.watchOnce()

    def stop(self):
        self.status = Watcher.STATUS_STOP

    def watchOnce(self):
        if not Point.isStockTime(): return
        point = Point.getNow(self.code)