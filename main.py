#coding=utf-8
from lib.config import Config
from lib.watcher import Watcher
from lib.point import Point
import sys
import multiprocessing
import time
import os
import gevent
import gevent.monkey

os.environ['TZ'] = 'Asia/Shanghai'
gevent.monkey.patch_all()

'''
def run(stock, notifyUrl):
    watcher = Watcher(stock['code'], buyPriceList=stock['buyPriceList'], salePriceList=stock['salePriceList'], notifyUrl=notifyUrl)
    watcher.start()

if __name__ == '__main__':
    conf = Config("./config.json")
    if not conf.isOK():
        print('conf has syntax error')
        sys.exit()
    taskList = []
    for stock in conf.reload().data['stockList']:
        t = gevent.spawn(run, stock, conf.reload().data['notifyUrl'])
        taskList.append(t)
    gevent.joinall(taskList)
'''

watcher = Watcher('sh600398', buyPriceList=[5.98], salePriceList=[6.20], notifyUrl='https://oapi.dingtalk.com/robot/send?access_token=d29bc5f270e97303817f9a0e3df8ccfa3e31efc04b04c8c2854765affb5b3fd9')
watcher.start()
