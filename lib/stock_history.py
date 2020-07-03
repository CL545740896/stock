#coding=utf-8

'''
获取股票的历史数据
'''

from lib.point import Point
import requests
import demjson

class StockHistory:

    def __init__(self, code, startDate, endDate):
        self.code = code
        self.startDate = startDate
        self.endDate = endDate
        self.baseurl = 'https://q.stock.sohu.com'
        self.timeout = 30

    def transCode(self, code):
        code = str(code).lower().replace('sz', '').replace('sh', '')
        code = 'cn_' + code
        return code

    def makeUrl(self):
        url =  self.baseurl + '/hisHq?code=%s&start=%s&end=%s&stat=1&order=A&period=d&callback=historySearchHandler&rt=json' % (
            self.transCode(self.code), self.startDate, self.endDate
        )
        return url
    
    def fetchRaw(self):
        '''
        成功返回响应内容和None, 否则返回响应内容和错误信息
        '''
        url = self.makeUrl()
        resp = ''
        err = None
        try:
            r = requests.get(url, timeout = self.timeout, verify = False)
            code, resp = r.status_code, r.text
            if code == 200:
                return resp, None
            else:
                return resp, "http code:%s" % code
        except Exception as ex:
            return resp, str(ex)

    def getPointList(self):
        '''
        成功返回list和None, 否则返回list和错误信息
        '''
        pointList = []
        err = None
        raw, err = self.fetchRaw()
        raw = raw.strip()
        if err != None:
            return pointList, err
        try:
            data = demjson.decode(raw)
            data = data[0]['hq']
            for dayData in data:
                p = Point()
                # 0    1    2    3    4    5    6    7       8    9
                #日期，开盘，收盘，涨跌，涨幅，最低，最高，成交量，成交额，换手
                p.time = dayData[0]
                p.dayBegin = dayData[1]
                p.dayEnd = dayData[2]
                p.dayMin = dayData[5]
                p.dayMax = dayData[6]
                pointList.append(p)
        except Exception as ex:
            err = str(ex)
        return pointList, err