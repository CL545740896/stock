#coding=utf-8
import gevent
import gevent.monkey
gevent.monkey.patch_all()
from lib.config import Config
from lib.watcher import Watcher
from lib.point import Point
import lib.notify
import sys
import multiprocessing
import time
import os
from agileutil.queue import UniMemQueue
from agileutil.log import Log
from lib.stock_history import StockHistory
import agileutil.wrap as awrap
os.environ['TZ'] = 'Asia/Shanghai'
commonLogger = Log('./common.log')

def run(stock, notifyUrl):
    watcher = Watcher(stock['code'], buyPriceList=stock['buyPriceList'], salePriceList=stock['salePriceList'], notifyUrl=notifyUrl)
    watcher.setCommonLogger(commonLogger)
    watcher.start()

def push_msg():
    while 1:
        time.sleep(30)
        msg = UniMemQueue.getInstance().pop()
        if msg == None:
            continue
        lib.notify.safeSendDDMsg(conf.reload().data['notifyUrl'], msg)

def gen_report():
    while 1:
        for stock in conf.reload().data['stockList']:
            sh = StockHistory(stock['code'], '20200601', '20200623')
            pointList = sh.getPointList()
            print(pointList)
            time.sleep(1)

def dump_queue():
    while 1:
        time.sleep(5)
        commonLogger.info('queue rest:' + str( UniMemQueue.getInstance().count() ))

if __name__ == '__main__':
    conf = Config("./config.json")
    if not conf.isOK():
        print('conf has syntax error')
        sys.exit()
    taskList = []
    for stock in conf.reload().data['stockList']:
        t = gevent.spawn(run, stock, conf.reload().data['notifyUrl'])
        taskList.append(t)

    #推送买入、卖出消息
    t = gevent.spawn(push_msg)
    taskList.append(t)

    #生成最近15个交易日的这线图
    #t = gevent.spawn(gen_report)
    #taskList.append(t)

    #打印消息队列积压
    t = gevent.spawn(dump_queue)
    taskList.append(t)


    gevent.joinall(taskList)