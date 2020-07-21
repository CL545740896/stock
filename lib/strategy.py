#coding=utf-8

class BaseStrategy:
	def __init__(self):
		pass


class HighProbRoseStrategy:
	'''
	策略说明：
	当一支股票当前价格到达了最近n个交易日的最低点，且在最近n个交易日中,
	此股票价格不断波动（即最近n个交易日此股价格不是一直上涨，也不是一只下跌）
	那么有很大概率近期仍会反弹(但不保证绝对反弹，任何人都无法预估市场，
	这里只参考此股最近n个交易日的表现，由于波动较大推测
	此时根据策略判断符合买入条件，发出买入信号
	'''

	def __init__(self, code='', name='',stockDayNum = 10, amplitude=0.1, waveTimes = 30):
		'''
		param code:股票代码
		param name:股票名称
		param stockDayNum: 多少个交易日
		param amplitude: 股票连续上涨或下跌的幅度，超过此幅度时认定为波动一次
		param waveTimes: 波动的次数，若最近n个交易日的波动次数小于此值，则不会发出买入信号
		'''
		self,code = code
		self.name = name
		self.stockDayNum = stockDayNum
		self.amplitude = amplitude
		self.waveTimes = waveTimes