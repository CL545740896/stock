from lib.config import Config
from lib.watcher import Watcher
import sys
import multiprocessing
import time

conf = Config("./config.json")
if not conf.isOK():
    print('conf has syntax error')
    sys.exit()

watcherList = []
for stock in conf.reload().data['stockList']:
    watcher = Watcher(stock['code'], buyPriceList=stock['buyPriceList'], salePriceList=stock['salePriceList'])
    watcherList.append(watcher)

for watcher in  watcherList:
    p = multiprocessing.Process(target=watcher.start(), args=())
    p.start()

while 1: time.sleep(3600)