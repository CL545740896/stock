#coding=utf-8

from lib.point import Point
from lib.notify_tpl import NotifyTpl
import lib.notify as notify
import requests
import time
from agileutil.log import Log
from agileutil.queue import UniMemQueue
import agileutil.date as dt

'''
监控一只股票
在满足买入阀值时，发送买入通知
在满足卖出阀值时，发送卖出通知
'''

class Watcher:

    STATUS_RUN = 1
    STATUS_STOP = 2

    def __init__(self, code, buyPriceList = [], salePriceList = [], notifyUrl = '', conf = None):
        self.code = code
        self.buyPriceList = buyPriceList
        self.salePriceList = salePriceList
        self.notifyUrl = notifyUrl
        self.status = Watcher.STATUS_STOP 
        self.logger = Log('./' + self.code + '.log')
        self.commonLogger = None
        self.globalConf = conf

    def isDisable(self):
        if self.globalConf == None:
            return False
        findStock = None
        for stock in self.globalConf.reload().data['stockList']:
            if stock['code'] == self.code:
                findStock = stock
                break
        if findStock == None:
            return True
        if 'enable' in findStock and findStock['enable'] == False:
            return True
        else:
            return False

    def setCommonLogger(self, logger):
        self.commonLogger = logger

    def start(self):
        self.status = Watcher.STATUS_RUN
        while 1:
            time.sleep(1)
            if self.status == Watcher.STATUS_STOP:
                print('watcher stopped')
                return
            if self.isDisable():
                print('%s warcher disable' % self.code )
                continue
            self.watchOnce()

    def stop(self):
        self.status = Watcher.STATUS_STOP

    def watchOnce(self):
        if not Point.isStcokTime(): 
            print('is not stock time, current time:' + str(dt.current_time()))
            return
        try:
            point = Point.getNow(self.code)
        except:
            return
        self.onNewPoint(point)

    def onBuyEvent(self, nowPrice, buyPrice, point):
        print('on buy event', 'now:', nowPrice, 'buy:', buyPrice)
        msg = NotifyTpl.genNotify(point.name, nowPrice, NotifyTpl.ACTION_BUY, '(<=%s)' % buyPrice)
        UniMemQueue.getInstance().push(msg)

    def onSaleEvent(self, nowPrice, salePrice, point):
        print('on sale event', 'now:', nowPrice, 'sale:', salePrice)
        msg = NotifyTpl.genNotify(point.name, nowPrice, NotifyTpl.ACTION_SALE, '(>=%s)' % salePrice)
        UniMemQueue.getInstance().push(msg)

    def onNewPoint(self, point):
        self.logger.info("code:%s, name:%s, now:%s, time:%s" % (point.code, point.name, point.now, point.time))
        if self.commonLogger:
            self.commonLogger.info("code:%s, name:%s, now:%s, time:%s" % (point.code, point.name, point.now, point.time))
        now = point.now
        for p in self.buyPriceList:
            if now <= p:
                self.onBuyEvent(now, p, point)
        for p in self.salePriceList:
            if now >= p:
                self.onSaleEvent(now, p, point)