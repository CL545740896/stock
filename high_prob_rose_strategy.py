#coding=utf-8

from base_strategy import BaseStrategy
from lib.stock_history import StockHistory
from lib.point import Point
from lib.notify_tpl import NotifyTpl
from lib.notify import defaultSendDDMsg
from lib.stock import StockList, Stock
import traceback

import time

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
                        stock_name,
                        stock_code,
                        beforeDayNum,
                        allowDynicPe=40,
                        allowStaticPe=40,
                        allowPb=20,
                        allowLowPrice=0.5,
                        allowHighPrice=30,
                        dy_pe = 0,
                        sta_pe = 0,
                        pb = 0):

        #如果是ST类型的股票，不分析
        if 'ST' in stock_name or 'st' in stock_name:
            return

        print(stock_name)

        startDate, endDate = cls.getBeginEndDate(beforeDayNum)

        sh = StockHistory(code=stock_code, startDate=startDate, endDate=endDate)
        pointList, err = sh.getPointList()
        if err != None:
            cls.logError("code:%s, name:%s, get history failed:%s" % (stock_code, stock_name, err) )
            return

        if len(pointList) <= 0:
            cls.logError("get latest n days data return empty list")
            return

        #判断是否到达最近几天的最低点
        now = Point.getNow(stock_code)
        #now.now = 1

        isLatestMin = True
        for point in pointList:
            #print('now:', now.now, 'daymin:', point.dayMin)
            #按照日期升序2020-07-13 ~ 2020-07-14
            if float(now.now) >= float(point.dayMin):
                isLatestMin = False
                break
        if isLatestMin == False:
            return

        #判断最近几天是否有振荡 (判断是否有涨有跌)
        roseNum = 0
        fallNum = 0
        for point in pointList:
            if point.dayBegin < point.dayEnd:
                roseNum += 1
            else:
                fallNum += 1
        sumNum = roseNum + fallNum

        #计算增长率
        roseRate = float(roseNum) / float(sumNum) * 100

        #判断当前价格是否符合购买区间
        if not (now.now >= allowLowPrice and now.now <= allowHighPrice):
            return
        print(dy_pe, sta_pe, pb, err)

        #日志
        cls.logInfo(
            "[buy event] code:%s, name:%s, dyPe:%s, staPe:%s, pb:%s, now:%s" % (
                stock_code, stock_name, dy_pe, sta_pe, pb, now.now
            )
        )

        #生成消息内容
        msg = NotifyTpl.genHighProbStrategyNotify('关注信号', stock_name, stock_code, now.now, len(pointList), dy_pe, sta_pe, pb, str(roseRate)[0:4])
        defaultSendDDMsg(msg)

    @classmethod
    def safeAnaOneStock(cls, stock, beforeDayNum):
        try:
            dy_pe, sta_pe, pb, _ = stock.getPePb()
            cls.analyseOneStock(stock.name, stock.code, beforeDayNum, dy_pe = dy_pe, sta_pe = sta_pe, pb = pb)
        except Exception as ex:
            cls.logError('analyse exception:' + str(ex))

    @classmethod
    def scanOnce(cls, beforeDayNum, concurrentNum):
        cls.logInfo('ready scan')
        if not Point.isStcokTime():
            return

        begin = time.time()

        stockList = StockList.getAllStock()
        index = 0
        for stock in stockList:
            cls.safeAnaOneStock(stock, beforeDayNum)
            index = index + 1
            cls.logInfo("name:%s,index:%s" % (stock.name, index))
        end = time.time()
        cost = end - begin
        cls.logInfo('scan once finish, stock num:' + str(len(stockList)) + ' cost:' + str(int(cost)) + ' seconds')

    @classmethod
    def safeScan(cls, beforeDayNum, concurrentNum):
        try:
            cls.scanOnce(beforeDayNum, concurrentNum)
        except Exception as ex:
            cls.logError("safeScan catch exception:" + str(ex) + traceback.format_exc())

    @classmethod
    def run(cls, beforeDayNum=20, sleepIntval=120, concurrentNum=4):
        while 1:
            cls.safeScan(beforeDayNum, concurrentNum)
            time.sleep(sleepIntval)