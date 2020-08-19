import requests
import ujson
#http://144.34.213.205:9876/get_now?code=sz002307
#r = requests.get('http://192.168.37.138:9876/get_now?code=sz002307')
r = requests.get('http://192.168.37.138:9876/get_now?code=SH600778')
print(r.text)
data = ujson.loads(r.text)
print(data)
'''
from lib.stock import StockList

name = StockList.getNameByCode('SH600778')

print(name)
'''
