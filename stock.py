#coding=utf-8
import gevent
from gevent import monkey
monkey.patch_all()
from lib.config import Config
from lib.watcher import Watcher
from lib.point import Point
import lib.notify
import sys
import os
from agileutil.queue import UniMemQueue
from agileutil.log import Log
from lib.stock import StockList
import lib.strategy as strategy
import agileutil.wrap as awrap
os.environ['TZ'] = 'Asia/Shanghai'
commonLogger = Log('./common.log')
strategyLogger = Log("./stragegy.log")


def init():
    lib.notify.init()
    StockList.getInstance().getAllStock()


def run(stock, notifyUrl, conf):
    watcher = Watcher(stock['code'],
                      buyPriceList=stock['buyPriceList'],
                      salePriceList=stock['salePriceList'],
                      notifyUrl=notifyUrl,
                      conf=conf)
    watcher.setCommonLogger(commonLogger)
    watcher.start()


def push_msg():
    while 1:
        gevent.sleep(30)
        msg = UniMemQueue.getInstance().pop()
        if msg == None:
            continue
        lib.notify.safeSendDDMsg(conf.reload().data['notifyUrl'], msg)


@awrap.safe
def get_report(code):
    pointList = []
    lastPoint = Point()
    with open('./' + code + '.log', 'r') as f:
        while 1:
            line = f.readline()
            if line:
                fields = line.split(' ')
                code = fields[6].split(':')[1].replace(',', '')
                name = fields[7].split(':')[1].replace(',', '')
                now = fields[8].split(':')[1].replace(',', '')
                time = ':'.join(fields[9].split(':')[1:])
                if now == lastPoint.now:
                    continue
                point = Point()
                point.code, point.name, point.now, point.time = code, name, now, time
                lastPoint = point
                pointList.append(point)
            else:
                break
    lastPoint.time = '15:30:00'
    pointList.append(lastPoint)
    return pointList


def gen_report():
    lastStockTag = False
    while 1:
        gevent.sleep(30)
        currentStockTag = Point.isStcokTime()
        if currentStockTag != lastStockTag and currentStockTag == False and lastStockTag == True:
            for stock in conf.reload().data['stockList']:
                get_report(stock['code'])
        lastStockTag = currentStockTag


def dump_queue():
    while 1:
        gevent.sleep(5)
        commonLogger.info('queue rest:' +
                          str(UniMemQueue.getInstance().count()))
        commonLogger.info('straMemCache count:' +
                          str(lib.notify.straMemCache.count()))


if __name__ == '__main__':
    conf = Config("./config.json")
    if not conf.isOK():
        print('conf has syntax error')
        sys.exit()

    init()

    taskList = []
    for stock in conf.reload().data['stockList']:
        t = gevent.spawn(run, stock, conf.reload().data['notifyUrl'], conf)
        taskList.append(t)

    #推送买入、卖出消息
    t = gevent.spawn(push_msg)
    taskList.append(t)

    #打印消息队列积压
    t = gevent.spawn(dump_queue)
    taskList.append(t)

    #异步消息
    t = gevent.spawn(lib.notify.asyncMsgConsume)
    taskList.append(t)

    #跑策略
    t = gevent.spawn(strategy.run_high_prob_role_strategy, strategyLogger)
    taskList.append(t)
    t = gevent.spawn(strategy.run_his_buy_profit_strategy, strategyLogger)
    taskList.append(t)
    t = gevent.spawn(strategy.run_still_rose_strategy, strategyLogger)
    taskList.append(t)
    t = gevent.spawn(strategy.run_etf_rise_strategy, strategyLogger)
    taskList.append(t)

    while 1:
        gevent.sleep(3600)

    #gevent.joinall(taskList)
