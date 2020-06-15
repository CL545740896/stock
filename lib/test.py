from point import Point
import time
import asyncio

'''
notifyUrl = 'https://oapi.dingtalk.com/robot/send?access_token=d29bc5f270e97303817f9a0e3df8ccfa3e31efc04b04c8c2854765affb5b3fd9'
watcher = Watcher(
    code = 'sz159919', 
    buyPriceList = [3.98, 3.97], 
    salePriceList = [4.05, 4.11], 
    notifyUrl = notifyUrl
)
watcher.start()
'''

from point import Point
p = Point().getNow('sz159919')
p.print()