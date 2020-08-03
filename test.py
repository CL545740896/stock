from lib.strategy import HighProbRoseStrategy, HisBuyProfitStrategy, FindStillRoseStrategy
from lib.stock import Stock, StockList

FindStillRoseStrategy.test()

'''
stock = Stock(code = 'sh603488')
if stock != None:
	dyPe, staPe, pb, err = stock.getPePb()
	print(dyPe, staPe, pb, err)
    #HighProbRoseStrategy.analyseOneStock(stock, 10)	
'''
'''
stock = Stock(code = 'sh600967')
raw, err = stock.fetchRawInfo()
print(raw, err)
'''



'''
from lib.stock import StockList
from lib.stock_history import StockHistory
import agileutil.wrap as awrap

stockList = StockList.getCarStockList()
for stock in stockList:
	sh = StockHistory(stock.code, '20200710', '20200722')
	pointList, err = sh.getPointList()
	for point in pointList:
		point.dump()
'''
'''
f = open('./data/stock_detail_list.json', 'r')
content = f.read()
f.close()
data = demjson.decode(content)
stockList = data['data']['list']
stock_list_json = []
for stock in stockList:
	m = {}
	m['name'] = stock['name']
	m['symbol'] = stock['symbol']
	m['pe_ttm'] = stock['pe_ttm']
	stock_list_json.append(m)
json_str = demjson.encode(stock_list_json)
f = open('./data/stock_list.json', 'w')
f.write(json_str)
f.close()
'''

'''
f = open('./data/stock_list.json', 'r')
content = f.read()
f.close()
stockList = demjson.encode(content)
print(stockList)
'''