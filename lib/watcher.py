#coding=utf-8

from lib.point import Point
from lib.notify_tpl import NotifyTpl
import lib.notify as notify
import requests
import time
from agileutil.log import Log

'''
监控一只股票
在满足买入阀值时，发送买入通知
在满足卖出阀值时，发送卖出通知
'''

class Watcher:

    STATUS_RUN = 1
    STATUS_STOP = 2

    def __init__(self, code, buyPriceList = [], salePriceList = [], notifyUrl = ''):
        self.code = code
        self.buyPriceList = buyPriceList
        self.salePriceList = salePriceList
        self.notifyUrl = notifyUrl
        self.status = Watcher.STATUS_STOP 
        self.logger = Log('./watcher.log')

    def start(self):
        self.status = Watcher.STATUS_RUN
        while 1:
            time.sleep(1)
            if self.status == Watcher.STATUS_STOP:
                print('watcher stopped')
                return
            self.watchOnce()

    def stop(self):
        self.status = Watcher.STATUS_STOP

    def watchOnce(self):
        if not Point.isStcokTime(): return
        try:
            point = Point.getNow(self.code)
        except:
            return
        self.onNewPoint(point)

    def onBuyEvent(self, nowPrice, buyPrice, point):
        print('on buy event', 'now:', nowPrice, 'buy:', buyPrice)
        msg = NotifyTpl.genNotify(point.name, nowPrice, NotifyTpl.ACTION_BUY, '(<=%s)' % buyPrice)
        notify.sendDDMsg(self.notifyUrl, msg)

    def onSaleEvent(self, nowPrice, salePrice, point):
        print('on sale event', 'now:', nowPrice, 'sale:', salePrice)
        msg = NotifyTpl.genNotify(point.name, nowPrice, NotifyTpl.ACTION_SALE, '(>=%s)' % salePrice)
        notify.sendDDMsg(self.notifyUrl, msg)

    def onNewPoint(self, point):
        self.logger.info("code:%s, name:%s, now:%s" % (point.code, point.name, point.now))
        now = point.now
        for p in self.buyPriceList:
            if now <= p:
                self.onBuyEvent(now, p, point)
        for p in self.salePriceList:
            if now >= p:
                self.onSaleEvent(now, p, point)