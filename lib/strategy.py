#coding=utf-8

from lib.point import Point
from lib.stock import StockList
from lib.stock_history import StockHistory
from lib.point import Point
import time
import gevent
from gevent import socket,monkey,pool
monkey.patch_all()


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
	def analyseOneStock(cls, stock, beforeDayNum, sleepIntval, concurrentNum):
		startDate, endDate = cls.getBeginEndDate()
		sh = StockHistory(code = stock.code, startDate = startDate, endDate = endDate)
		pointList, err = sh.getPointList()
		if err != None:
			cls.logError("code:%s, name:%s, get history failed:%s" % (stock.code, stock.name, err) )
			return
		cls.logInfo( "code:%s, name:%s, get history succed" % (stock.code, stock.name) )
		print('point count:', len(pointList))
		

	@classmethod
	def scanOnce(cls, beforeDayNum, sleepIntval, concurrentNum):
		if not Point.isStcokTime() and False: return
		concurrentPool = pool.Pool(concurrentNum)
		stockList = StockList.getAllStock()
		for stock in stockList:
			concurrentPool.spawn(cls.analyseOneStock, stock, beforeDayNum, sleepIntval, concurrentNum)

	@classmethod
	def safeScan(cls, beforeDayNum, sleepIntval, concurrentNum):
		try:
			cls.scanOnce(beforeDayNum, sleepIntval, concurrentNum)
		except Exception as ex:
			cls.logError("safeScan catch exception:" + str(ex))
		cls.logInfo("scan once")

	@classmethod
	def run(cls, beforeDayNum = 7, sleepIntval = 20, concurrentNum = 100):
		while 1:
			cls.safeScan(beforeDayNum, sleepIntval, concurrentNum)
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