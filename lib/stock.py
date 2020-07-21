#coding=utf-8

import demjson

class Stock:

	def __init__(self, code = '', name='', peTtm = 0):
		self.code = code
		self.name = name
		self.peTtm = peTtm

	def dump(self):
		print("code:%s,name:%s,pe_ttm:%s" % (
			self.code,
			self.name,
			self.peTtm
		))

class StockList:

	stockList = None
	instance = None

	def __init__(self):
		pass

	@classmethod
	def getInstance(cls):
		if cls.instance == None:
			cls.instance = StockList()
		return cls.instance

	@classmethod
	def getAllStock(cls):
		if cls.stockList == None:
			f = open('./data/stock_list.json', 'r')
			content = f.read()
			f.close()
			tmpStockList = demjson.decode(content)
			stockList = []
			for stockItem in tmpStockList:
				stock = Stock(
					code = stockItem['symbol'].lower(), 
					name = stockItem['name'], 
					peTtm = stockItem['pe_ttm']
				)
				stockList.append(stock)
			cls.stockList = stockList
		return cls.stockList