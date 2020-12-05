#coding=utf-8

import ujson
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Stock:
    def __init__(self, code='', name='', peTtm=0):
        self.code = code
        self.name = name
        self.peTtm = peTtm

    def dump(self):
        print("code:%s,name:%s,pe_ttm:%s" % (self.code, self.name, self.peTtm))

    def fetchRawInfo(self):
        url = 'https://xueqiu.com/stock/f10/compinfo.json?symbol=%s' % self.code
        headers = {
            'Cookie':
            's=d811jej3wn; device_id=7a4981ca5bec19d55e5b932ebdd7a3b4; aliyungf_tc=AQAAAPXlQiwi2AAAEOT7ciyRymMNb7Id; xq_a_token=ad923af9f68bb6a13ada0962232589cea11925c4; xqat=ad923af9f68bb6a13ada0962232589cea11925c4; xq_r_token=cf0e6f767c2318f1f1779fcee9323365f02e1b4b; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTU5NjE2MjgxNSwiY3RtIjoxNTk1MzMxNjUyMDUzLCJjaWQiOiJkOWQwbjRBWnVwIn0.FgAkF-boF_MquIfBejwPAj3Xq1yehunyuAdQsrcSm9OPcO_AIEM77haw2cuhGBHgzZOuZR5zcU_t68G-vAp7U5WyQeMJxK1r3Ddpr8U-svMIZi---6Vj1PkIKMU_JMjlRKREnTZ2zrEpqCwlbtx4VPQr3yTmAFSfbtg38_9sJ2-tN-gJ3KUwvNbRYlHs473JGIdlRBYzF8fjr5WCABZiqC8nnprrAUXmAsMGpoVMOndKtFUnsFh-BW4xa36AQk2Wto75TVTtWIgqYRgDIkucd9wPFuKAi26I5EaG19KT7XtGwGTnkM4KxSGFTtJCzM_N6yUdmGUxxPJFv6fL9_TmvA; u=211595331675076; acw_tc=2760825415954062862922319e4cf4a1e515a6e1bb203be12f6a70642cda77; Hm_lvt_1db88642e346389874251b5a1eded6e3=1593573481,1593781252,1595331676,1595406288; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1595406288',
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        }
        r = None
        try:
            r = requests.get(url, verify=False, headers=headers)
        except Exception as ex:
            return '', str(ex)
        if r.status_code != 200:
            return '', "http status code:%s" % r.status_code
        return r.text, None

    def getInfo(self):
        raw, err = self.fetchRawInfo()
        if err != None:
            return [], err
        data = []
        try:
            data = ujson.loads(raw)
        except Exception as ex:
            return [], str(ex)
        return data, None

    @classmethod
    def getByName(cls, name):
        stockList = StockList.getAllStock()
        nameStockMap = {}
        for stock in stockList:
            nameStockMap[stock.name] = stock
        if name in nameStockMap:
            return nameStockMap[name]
        return None

    def fetchPe(self):
        url = 'https://stock.xueqiu.com/v5/stock/quote.json?symbol=%s&extend=detail' % self.code.upper(
        )
        headers = {
            'Cookie':
            's=d811jej3wn; device_id=7a4981ca5bec19d55e5b932ebdd7a3b4; xq_a_token=69a6c81b73f854a856169c9aab6cd45348ae1299; xqat=69a6c81b73f854a856169c9aab6cd45348ae1299; xq_r_token=08a169936f6c0c1b6ee5078ea407bb28f28efecf; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTU5ODMyMzAwNCwiY3RtIjoxNTk1NzM5NDI3NDY0LCJjaWQiOiJkOWQwbjRBWnVwIn0.Y992GPjMMv1wIO9-pzikMuFQeb4vqZPohLqz_7l3A7ScKjW24ZyK3vmHGhR7XTO2a6xe7EUvcUSjOUnFnH4yKVm8I9ebmqnDb-pqzCi4hRPLLditb_56NPhgykLlGk577wkHWVDKMVvMutkdtolEWxAjcfQhsTrrtJkvHtgI2uRX9ksRws8BXt0juRGE07a_pjlITrT9-koWVsKXJ8-MJaH-lUlia7g80WCnO827mNnFLullOxrIa0PlHl5pQNmVmd4y5k0qQJ_rHCCx6ZDjJFrNG-SZQruqLifCDmHFdAeUsZvCnR3YM3a2WNO8MIoEXmO23vHY_E9ha0bGJV3pVw; u=751595739466597; Hm_lvt_1db88642e346389874251b5a1eded6e3=1595510636,1595564296,1595665596,1595739469; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1595739475',
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "Referer": "https://xueqiu.com/S/SZ002389",
        }
        r = None
        try:
            r = requests.get(url, verify=False, headers=headers)
            print(url, r.status_code)
        except Exception as ex:
            return '', str(ex)
        if r.status_code != 200:
            return '', 'http status code:%s' % r.status_code
        return r.text, None

    def getPe(self):
        '''
		返回动态市盈率和静态市盈率
		'''
        dyPe, staticPe = -1, -1
        raw, err = self.fetchPe()
        if err != None:
            return dyPe, staticPe, err
        try:
            data = ujson.loads(raw)
            dyPe = data['data']['quote']['pe_forecast']
            staticPe = data['data']['quote']['pe_lyr']
        except Exception as ex:
            return dyPe, staticPe, err
        return dyPe, staticPe, None

    def getPePb(self):
        '''
		返回动态市盈率和静态市盈率
		'''
        dyPe, staticPe, pb = 0, 0, 0
        raw, err = self.fetchPe()
        if err != None:
            return dyPe, staticPe, pb, err
        try:
            data = ujson.loads(raw)
            dyPe = data['data']['quote']['pe_forecast']
            staticPe = data['data']['quote']['pe_lyr']
            pb = data['data']['quote']['pb']
        except Exception as ex:
            return dyPe, staticPe, pb, err
        return dyPe, staticPe, pb, None


class StockList:

    stockList = None
    instance = None

    def __init__(self):
        pass

    @classmethod
    def getInstance(cls):
        if cls.instance == None:
            cls.instance = StockList()
        return cls.instance

    @classmethod
    def getAllStock(cls):
        if cls.stockList == None:
            f = open('./data/stock_list.json', 'r')
            content = f.read()
            f.close()
            tmpStockList = ujson.loads(content)
            stockList = []
            for stockItem in tmpStockList:
                stock = Stock(code=stockItem['symbol'].lower(),
                              name=stockItem['name'],
                              peTtm=stockItem['pe_ttm'])
                stockList.append(stock)
            cls.stockList = stockList
        #for test
        #return  [ cls.stockList[20] ]
        return cls.stockList

    @classmethod
    def filterByWord(cls, word):
        stockList = cls.getAllStock()
        retList = []
        for stock in stockList:
            if word in stock.name:
                retList.append(stock)
        return retList

    @classmethod
    def getBankStockList(cls):
        return cls.filterByWord('银行')

    @classmethod
    def getCarStockList(cls):
        return cls.filterByWord('车')

    @classmethod
    def getNameByCode(cls, code):
        code = code.upper()
        stockList = StockList.getInstance().getAllStock()
        for stock in stockList:
            if stock.code.upper() == code:
                return stock.name
        return ''