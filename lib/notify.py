#coding=utf-8

import gevent
from gevent import monkey
monkey.patch_all()
import requests
import demjson
import lib.util as util
import time
import sys
from agileutil.queue import UniMemQueue
from lib.config import Config
from agileutil.memcache import MemStringCache

msgQueue = None
straMemCache = None


def init():
    global straMemCache
    if straMemCache == None:
        straMemCache = MemStringCache()
    initMsgQueue()


def initMsgQueue():
    global msgQueue
    if msgQueue != None: return
    msgQueue = UniMemQueue()
    if msgQueue == None:
        print('init msg queue failed')
        sys.exit(1)


def sendDDMsg(ddrotUrl='', msg='', timeout=10):
    v = straMemCache.get(msg)
    if v != None: return
    util.disable_requests_warn()
    headers = {'Content-Type': 'application/json'}
    params = {
        'msgtype': 'text',
        'text': {
            'content': msg
        },
    }
    data = demjson.encode(params)
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
    code = output = None
    try:
        code, output = sendDDMsg(ddrotUrl, msg, timeout)
    except Exception as ex:
        print('safeSendDDMsg exception:' + str(ex))
        pass
    return code, output


def asyncSendMsg(msg):
    if msg == '': return
    msgQueue.push(msg)


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
