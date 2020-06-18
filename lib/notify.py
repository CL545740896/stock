#coding=utf-8

import requests
import demjson
import lib.util as util

def sendDDMsg(ddrotUrl = '', msg = '', timeout = 10):
    util.disable_requests_warn()
    print('send msg:', msg, ddrotUrl)
    headers = {'Content-Type' : 'application/json'}
    params = {
        'msgtype' : 'text', 
        'text' : {'content' : msg },
    }
    data = demjson.encode(params)
    r = requests.post(url = ddrotUrl, headers=headers, data=data, timeout = timeout, verify=False)
    import sys;sys.exit(0)
    return r.status_code, r.text

def safeSendDDMsg(ddrotUrl = '', msg = '', timeout = 10):
    code = output = None
    try:
        code, output = sendDDMsg(ddrotUrl, msg, timeout)
    except Exception as ex:
        print('safeSendDDMsg exception:' + str(ex))
        pass
    return code, output