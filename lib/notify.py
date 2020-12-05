#coding=utf-8

import requests
import ujson
import lib.util as util
import time
import sys
from agileutil.queue import UniMemQueue
from lib.config import Config
from agileutil.memcache import MemStringCache
from lib.point import Point

msgQueue = None
straMemCache = None

def get_msg_queue():
    global msgQueue
    if msgQueue == None:
        msgQueue = UniMemQueue()
    return msgQueue


def init():
    global straMemCache
    if straMemCache == None:
        straMemCache = MemStringCache()
    initMsgQueue()


def initMsgQueue():
    global msgQueue
    if msgQueue != None:
        return
    msgQueue = UniMemQueue()


def sendDDMsg(ddrotUrl='', msg='', timeout=10):
    util.disable_requests_warn()
    headers = {'Content-Type': 'application/json'}
    params = {
        'msgtype': 'text',
        'text': {
            'content': msg
        },
    }
    data = ujson.dumps(params)
    r = requests.post(url=ddrotUrl,
                      headers=headers,
                      data=data,
                      timeout=timeout,
                      verify=False)
    print('send msg:', msg, ddrotUrl, r.status_code, r.text)
    straMemCache.set(msg, '1', 3600 * 3)
    return r.status_code, r.text


def defaultSendDDMsg(msg):
    conf = Config("./config.json")
    if not conf.isOK(): return
    return sendDDMsg(conf.reload().data['notifyUrl'], msg, 10)


def safeSendDDMsg(ddrotUrl='', msg='', timeout=10):
    if not Point.isStcokTime(): return
    code = output = None
    try:
        code, output = sendDDMsg(ddrotUrl, msg, timeout)
    except Exception as ex:
        print('safeSendDDMsg exception:' + str(ex))
        pass
    return code, output


def asyncSendMsg(msg):
    if msg == '':
        return
    if not Point.isStcokTime():
        return
    get_msg_queue().push(msg)


def asyncMsgConsume(sleepIntval=60):
    while 1:
        gevent.sleep(sleepIntval)
        totalMsg = ''
        while 1:
            msg = msgQueue.pop()
            if msg == None: break
            totalMsg = totalMsg + msg + "\n\n"
        if totalMsg == '': continue
        defaultSendDDMsg(totalMsg)
