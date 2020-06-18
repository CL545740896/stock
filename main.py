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
os.environ['TZ'] = 'Asia/Shanghai'


def run(stock, notifyUrl):
    watcher = Watcher(stock['code'], buyPriceList=stock['buyPriceList'], salePriceList=stock['salePriceList'], notifyUrl=notifyUrl)
    watcher.start()

def push_msg():
    while 1:
        time.sleep(1)
        msg = UniMemQueue.getInstance().pop()
        if msg == None:
            continue
        lib.notify.safeSendDDMsg(conf.reload().data['notifyUrl'], msg)

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

    gevent.joinall(taskList)
