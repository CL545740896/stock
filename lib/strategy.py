#coding=utf-8

import gevent
from gevent import socket,monkey,pool
monkey.patch_all()
from lib.point import Point
from lib.stock import StockList
from lib.stock_history import StockHistory
from lib.point import Point
from lib.notify_tpl import NotifyTpl
from lib.config import Config
import lib.notify as notify
import time


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
	def getBeginEndDate(cls, days = 10):
		now = time.time()
		endDate = time.strftime('%Y%m%d', time.localtime(now) )
		begin = now -  ( days * 24 * 3600 )
		beginDate = time.strftime("%Y%m%d", time.localtime(begin) )
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
	def analyseOneStock(cls, stock, beforeDayNum):
		#如果是ST类型的股票，不分析
		if 'ST' in stock.name or 'st' in stock.name: return
		#for test
		#print('run strategy', stock.code)
		startDate, endDate = cls.getBeginEndDate(beforeDayNum)
		sh = StockHistory(code = stock.code, startDate = startDate, endDate = endDate)
		pointList, err = sh.getPointList()
		if err != None:
			cls.logError("code:%s, name:%s, get history failed:%s" % (stock.code, stock.name, err) )
			return
		pointList = pointList[0:beforeDayNum-2]
		cls.logInfo( "code:%s, name:%s, get history succed" % (stock.code, stock.name) )
		if len(pointList) <= 0: return
		#判断是否到达最近几天的最低点
		now = Point.getNow(stock.code)
		isLatestMin = True
		for point in pointList:
			#按照日期升序2020-07-13 ~ 2020-07-14
			#for test
			#print('code:', point.code, 'time:', point.time, 'dayBegin:', point.dayBegin, 'dayEnd:', point.dayEnd, 'dayMax:', point.dayMax, 'dayMin:', point.dayMin)
			if float(now.now) >= float(point.dayMin):
				isLatestMin = False
				break
		#判断最近几天是否有振荡 (判断是否有涨有跌)
		roseNum = 0
		fallNum = 0
		for point in pointList:
			if point.dayBegin <= point.dayEnd:
				roseNum = roseNum + 1
			else:
				fallNum = fallNum + 1
		if roseNum == 0:
			#最近几天一直下跌, 忽略
			print(stock.name, '最近', len(pointList), '天', '一直下跌')
			return
		if fallNum == 0:
			#最近几天一直上涨, 忽略
			print(stock.name, '最近', len(pointList), '天', '一直上涨')
			return
		if roseNum > 0 and fallNum > 0:
			print(stock.name, '最近', len(pointList), '天', '振荡')
			if not isLatestMin: return
			info, err = stock.getInfo()
			if err != None:
				print('get stock info failed:' + str(err))
				return
			#最近几天有涨有跌，发送买入信号
			dyPe, staPe, err = stock.getPe()
			if err != None:
				print('get pe failed:', err)
				return
			if dyPe < 0 or staPe < 0: return
			if not (dyPe <= 20): return
			print('buy event:', stock.code, stock.name, stock.peTtm, info)
			msg = NotifyTpl.genHighProbStrategyNotify('买入信号', stock.name, stock.code, now.now, len(pointList), dyPe, staPe)
			notify.asyncSendMsg(msg)


	@classmethod
	def scanOnce(cls, beforeDayNum, concurrentNum):
		if not Point.isStcokTime(): return
		#if not Point.isStcokTime() and False: return
		concurrentPool = pool.Pool(concurrentNum)
		stockList = StockList.getAllStock()
		for stock in stockList:
			concurrentPool.spawn(cls.analyseOneStock, stock, beforeDayNum)
			#for test
			#return

	@classmethod
	def safeScan(cls, beforeDayNum, concurrentNum):
		try:
			cls.scanOnce(beforeDayNum, concurrentNum)
		except Exception as ex:
			cls.logError("safeScan catch exception:" + str(ex))
		cls.logInfo("scan once")

	@classmethod
	def run(cls, beforeDayNum = 10, sleepIntval = 20, concurrentNum = 100):
		while 1:
			cls.safeScan(beforeDayNum, concurrentNum)
			time.sleep(sleepIntval)


def run_high_prob_role_strategy(logger):
	HighProbRoseStrategy.logger = logger
	HighProbRoseStrategy.run()


class shareOutBonusStrategy(BaseStrategy):
	'''
	找出最近分紅的股票
	'''
	def __init__(self):
		pass