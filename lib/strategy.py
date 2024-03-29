#coding=utf-8

import gevent
from gevent import socket, monkey, pool
monkey.patch_all()
from lib.point import Point
from lib.stock import StockList, Stock
from lib.stock_history import StockHistory
from lib.point import Point
from lib.notify_tpl import NotifyTpl
from lib.config import Config
from lib.etf import ETF
from agileutil.memcache import MemStringCache
import agileutil.wrap as awrap
import lib.notify as notify
import time
import demjson
import sys
import multiprocessing
from agileutil.log import Log


class BaseStrategy:

    logger = None

    def __init__(self):
        pass

    @classmethod
    def logError(cls, string):
        if cls.logger != None: cls.logger.error("[strategy] " + string)

    @classmethod
    def logInfo(cls, string):
        if cls.logger != None: cls.logger.info("[strategy] " + string)

    @classmethod
    def logWarning(cls, string):
        if cls.logger != None: cls.logger.warning("[strategy] " + string)

    @classmethod
    def getBeginEndDate(cls, days=10):
        now = time.time()
        endDate = time.strftime('%Y%m%d', time.localtime(now))
        begin = now - (days * 24 * 3600)
        beginDate = time.strftime("%Y%m%d", time.localtime(begin))
        return str(beginDate), str(endDate)


class HighProbRoseStrategy(BaseStrategy):
    '''
	策略说明：
	当一支股票当前价格到达了最近n个交易日的最低点，且在最近n个交易日中,
	此股票价格不断波动（即最近n个交易日此股价格不是一直上涨，也不是一只下跌）
	那么有很大概率近期仍会反弹(但不保证绝对反弹，任何人都无法预估市场，
	这里只参考此股最近n个交易日的表现，由于波动较大推测
	此时根据策略判断符合买入条件，发出买入信号
	'''
    @classmethod
    def analyseOneStock(cls,
                        stock,
                        beforeDayNum,
                        allowDynicPe=40,
                        allowStaticPe=40,
                        allowPb=20,
                        allowLowPrice=2,
                        allowHighPrice=40):
        gevent.sleep(0.001)
        #如果是ST类型的股票，不分析
        if 'ST' in stock.name or 'st' in stock.name: return
        startDate, endDate = cls.getBeginEndDate(beforeDayNum)
        print(startDate, endDate)
        sh = StockHistory(code=stock.code,
                          startDate=startDate,
                          endDate=endDate)
        pointList, err = sh.getPointList()
        if err != None:
            cls.logError("code:%s, name:%s, get history failed:%s" %
                         (stock.code, stock.name, err))
            return
        pointList = pointList[-10:]
        for p in pointList:
            print(p.time)
        if len(pointList) <= 0: return
        #判断是否到达最近几天的最低点
        now = Point.getNow(stock.code)
        line = stock.name + ' now:' + str(now.now)
        for p in pointList:
            line = line + "|%s %s %s|" % (p.dayBegin, p.dayEnd, p.time)
        print(line, beforeDayNum, startDate, endDate, len(pointList), now.now)
        isLatestMin = True
        for point in pointList:
            #按照日期升序2020-07-13 ~ 2020-07-14
            #for test
            #print('code:', point.code, 'time:', point.time, 'dayBegin:', point.dayBegin, 'dayEnd:', point.dayEnd, 'dayMax:', point.dayMax, 'dayMin:', point.dayMin)
            if float(now.now) >= float(point.dayMin):
                isLatestMin = False
                break
        #判断最近几天是否有振荡 (判断是否有涨有跌)
        if isLatestMin == False: return
        roseNum = 0
        fallNum = 0
        for point in pointList:
            if point.dayBegin < point.dayEnd:
                roseNum = roseNum + 1
            else:
                fallNum = fallNum + 1
        sumNum = roseNum + fallNum
        roseRate = float(roseNum) / float(sumNum)
        if roseRate <= 0.25: return
        dyPe, staPe, pb, err = stock.getPePb()
        print(dyPe, staPe, pb, err)
        cls.logInfo("pb pe :%s,%s,%s,%s" % (dyPe, staPe, pb, err))
        if err != None:
            cls.logError('get pe pb info failed:' + str(err))
            return
        if dyPe < 0 or staPe < 0: return
        if dyPe > allowDynicPe: return
        if staPe > allowStaticPe: return
        if pb > allowPb: return
        if not (now.now >= allowLowPrice and now.now <= allowHighPrice): return
        if not cls.isAllowSend(stock.code): return
        try:
            cls.logInfo(
                "[buy event] code:%s, name:%s, dyPe:%s, staPe:%s, pb:%s, now:%s"
                % (stock.code, stock.name, dyPe, staPe, pb, now.now))
            msg = NotifyTpl.genHighProbStrategyNotify('关注信号', stock.name,
                                                      stock.code, now.now,
                                                      len(pointList), dyPe,
                                                      staPe, pb,
                                                      str(roseRate)[0:4])
            notify.asyncSendMsg(msg)
            cls.markSend(stock.code)
        except Exception as ex:
            cls.logError("send msg exception:" + str(ex))
            return
        cls.logInfo("send once")

    @classmethod
    def test(cls):
        startDate, endDate = cls.getBeginEndDate(20)
        print(startDate, endDate)
        sh = StockHistory(code='sz002078',
                          startDate=startDate,
                          endDate=endDate)
        pointList, err = sh.getPointList()
        if err != None:
            print(err)
            return
        for p in pointList:
            print(p.dayMin, p.time)
        now = Point.getNow('sz002078')
        print('now:', now.now)
        isLatestMin = True
        for point in pointList:
            #按照日期升序2020-07-13 ~ 2020-07-14
            #for test
            #print('code:', point.code, 'time:', point.time, 'dayBegin:', point.dayBegin, 'dayEnd:', point.dayEnd, 'dayMax:', point.dayMax, 'dayMin:', point.dayMin)
            if float(now.now) >= float(point.dayMin):
                isLatestMin = False
                break
        print('isLatestMin:', isLatestMin)

    @classmethod
    def isAllowSend(cls, code):
        key = "HighProbRoseStrategy:" + code
        v = notify.straMemCache.get(key)
        if v == None:
            return True
        return False

    @classmethod
    def markSend(cls, code):
        key = "HighProbRoseStrategy:" + code
        notify.straMemCache.set(key, '1', 3600 * 3)

    @classmethod
    def safeAnaOneStock(cls, stock, beforeDayNum):
        try:
            cls.analyseOneStock(stock, beforeDayNum)
        except Exception as ex:
            print('analyse exception:' + str(ex))

    @classmethod
    def scanOnce(cls, beforeDayNum, concurrentNum):
        cls.logInfo('ready scan')
        if not Point.isStcokTime(): return
        #for test
        #if not Point.isStcokTime() and False: return
        begin = time.time()
        concurrentPool = pool.Pool(concurrentNum)
        stockList = StockList.getAllStock()
        index = 0
        for stock in stockList:
            concurrentPool.spawn(cls.safeAnaOneStock, stock, beforeDayNum)
            index = index + 1
            cls.logInfo("name:%s,index:%s" % (stock.name, index))
        concurrentPool.join()
        end = time.time()
        cost = end - begin
        cls.logInfo('scan once finish, stock num:' + str(len(stockList)) +
                    ' cost:' + str(int(cost)) + ' seconds')

    @classmethod
    def safeScan(cls, beforeDayNum, concurrentNum):
        try:
            cls.scanOnce(beforeDayNum, concurrentNum)
        except Exception as ex:
            cls.logError("safeScan catch exception:" + str(ex))

    @classmethod
    def run(cls,
            beforeDayNum=20,
            sleepIntval=120,
            concurrentNum=multiprocessing.cpu_count()):
        while 1:
            cls.safeScan(beforeDayNum, concurrentNum)
            time.sleep(sleepIntval)


def run_high_prob_role_strategy(logger = None):
    if logger == None:
        logger = Log('./logs/' + sys._getframe().f_code.co_name + '.log')
    HighProbRoseStrategy.logger = logger
    HighProbRoseStrategy.run()


def run_his_buy_profit_strategy(logger):
    HisBuyProfitStrategy.logger = logger
    HisBuyProfitStrategy.run()


def run_still_rose_strategy(logger):
    FindStillRoseStrategy.logger = logger
    FindStillRoseStrategy.run()


def run_etf_rise_strategy(logger):
    ETFRiseStrategy.logger = logger
    ETFRiseStrategy.run()


class HisBuyProfitStrategy(BaseStrategy):
    @classmethod
    def checkOnce(cls):
        gevent.sleep(0.001)
        f = open('./data/his_buy_profit.json', 'r')
        content = f.read()
        f.close()
        data = demjson.decode(content)
        for code, buyProfitList in data.items():
            buyProfitList.sort()
            print(code, buyProfitList)
            point = Point.getNow(code)
            print(point)
            isLessThanHis = False
            comparePrice = 0
            for price in buyProfitList:
                if point.now <= price:
                    isLessThanHis = True
                    comparePrice = price
                    break
            print(isLessThanHis, point.now)
            if not isLessThanHis: continue
            print('allow send：', cls.isAllowSend(code))
            if not cls.isAllowSend(code): return
            msg = NotifyTpl.genHisBuyProfitNotify('买入信号', point.name, code,
                                                  point.now, comparePrice)
            print('msg:', msg)
            notify.defaultSendDDMsg(msg)
            cls.markSend(code)

    hisBuyMemCache = None

    @classmethod
    def init(cls):
        if cls.hisBuyMemCache == None:
            cls.hisBuyMemCache = MemStringCache()

    @classmethod
    def isAllowSend(cls, code):
        cls.init()
        key = "HisBuyProfitStrategy:" + code
        v = cls.hisBuyMemCache.get(key)
        if v == None: return True
        return False

    @classmethod
    def markSend(cls, code):
        cls.init()
        key = "HisBuyProfitStrategy:" + code
        cls.hisBuyMemCache.set(key, '1', 3600 * 3)

    @classmethod
    def safeCheckOnce(cls):
        try:
            cls.checkOnce()
        except Exception as ex:
            cls.logError("HisBugProfileStrategy exception:" + str(ex))

    @classmethod
    def run(cls):
        while 1:
            #for test
            gevent.sleep(60)
            if not Point.isStcokTime(): continue
            cls.safeCheckOnce()


class shareBonusStrategy(BaseStrategy):
    '''
	找出最近分紅的股票
	'''
    def __init__(self):
        pass


class FindStillRoseStrategy(BaseStrategy):
    '''
	找出连续n天都在上涨的股票
	'''
    @classmethod
    @awrap.safe
    def scan(cls, stock, beforeDayNum=10):
        gevent.sleep(0.001)
        #如果是ST类型的股票，不分析
        if 'ST' in stock.name or 'st' in stock.name: return
        startDate, endDate = cls.getBeginEndDate(35)
        print(startDate, endDate)
        sh = StockHistory(code=stock.code,
                          startDate=startDate,
                          endDate=endDate)
        pointList, err = sh.getPointList()
        if err != None:
            cls.logError("code:%s, name:%s, get history failed:%s" %
                         (stock.code, stock.name, err))
            return
        index = 0 - beforeDayNum
        pointList = pointList[index:]
        for point in pointList:
            if point.dayBegin >= point.dayEnd:
                return
        #判断价格是否连续上涨
        isStillRose = True
        length = len(pointList)
        for i in range(length - 1):
            if pointList[i].dayEnd >= pointList[i + 1].dayEnd:
                isStillRose = False
        if isStillRose == False: return
        now = Point.getNow(stock.code)
        msg = NotifyTpl.genStillRoseNotify('关注信号', stock.name, stock.code,
                                           length, now.now)
        notify.asyncSendMsg(msg)

    @classmethod
    @awrap.safe
    def scanOnce(cls,
                 beforeDayNum=10,
                 concurrentNum=multiprocessing.cpu_count()):
        #for test
        if not Point.isStcokTime(): return
        begin = time.time()
        concurrentPool = pool.Pool(concurrentNum)
        stockList = StockList.getAllStock()
        index = 0
        for stock in stockList:
            concurrentPool.spawn(cls.scan, stock, beforeDayNum)
            index = index + 1
            cls.logInfo("name:%s,index:%s" % (stock.name, index))
        concurrentPool.join()
        end = time.time()
        cost = end - begin
        cls.logInfo('scan once finish, stock num:' + str(len(stockList)) +
                    ' cost:' + str(int(cost)) + ' seconds')

    @classmethod
    def run(cls):
        while 1:
            gevent.sleep(60)
            cls.scanOnce()

    @classmethod
    def test(cls):
        stock = Stock('sz002405')
        cls.scan(stock)


class ETFRiseStrategy(BaseStrategy):
    '''
	找出ETF类指数基金, 最近连续下跌的, 对于定投来讲，下跌时候是买入的机会
	'''
    @classmethod
    def scanOnce(cls, concurrentNum=multiprocessing.cpu_count()):
        concurrentPool = pool.Pool(concurrentNum)
        cnEtfList = ETF.getCnETFList()
        for etf in cnEtfList:
            concurrentPool.spawn(cls.scanOne, etf)
        concurrentPool.join()
        print('scan once')

    @classmethod
    @awrap.safe
    def scanOne(cls, etf, beforeDayNum=2):
        gevent.sleep(0.001)
        startDate, endDate = cls.getBeginEndDate(20)
        sh = StockHistory(etf.code.lower(), startDate, endDate)
        pointList, err = sh.getPointList()
        if err != None:
            cls.logError("get etf history failed:" + str(err))
            return
        index = 0 - beforeDayNum
        pointList = pointList[index:]
        length = len(pointList)
        #判断价格是否连续下跌
        isStillRise = True
        for i in range(length - 1):
            if pointList[i].dayEnd <= pointList[i + 1].dayEnd:
                isStillRise = False
        if isStillRise == False: return
        #判断是否连续下跌
        for point in pointList:
            if point.dayBegin <= point.dayEnd:
                return
        now = Point.getNow(etf.code)
        #大于30块的不要
        if now.now >= 30: return
        msg = NotifyTpl.genETFRiseTpl('关注信息', etf.name, etf.code, length,
                                      now.now)
        notify.asyncSendMsg(msg)

    @classmethod
    def run(cls):
        while 1:
            gevent.sleep(60)
            cls.scanOnce()
