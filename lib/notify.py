import requests
import demjson

def sendDDMsg(ddrotUrl = '', msg = '', timeout = 10):
    print('send msg:', msg, ddrotUrl)
    headers = {'Content-Type' : 'application/json'}
    params = {
        'msgtype' : 'text', 
        'text' : {'content' : msg },
    }
    data = demjson.encode(params)
    r = requests.post(url = ddrotUrl, headers=headers, data=data, timeout = timeout, verify=False)
    return r.status_code, r.text