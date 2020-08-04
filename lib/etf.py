#coding=utf-8

import demjson


class ETF:

    allETFList = None
    cnETFList = None
    codeNameMap = None

    def __init__(self, code):
        self.code = code
        self.name = None
        self.name = self.getName()

    @classmethod
    def getAllETFList(cls):
        if cls.allETFList == None:
            f = open('./data/all_etf.json', 'r')
            content = f.read()
            f.close()
            allETFList = demjson.decode(content)
            cls.allETFList = []
            for etf in allETFList:
                etfObj = ETF(etf['code'])
                cls.allETFList.append(etfObj)
        return cls.allETFList

    @classmethod
    def getCnETFList(cls):
        if cls.cnETFList == None:
            f = open('./data/cn_etf_list.json', 'r')
            content = f.read()
            f.close()
            cnETFList = demjson.decode(content)
            cls.cnETFList = []
            for etf in cnETFList:
                etfObj = ETF(etf['code'])
                cls.cnETFList.append(etfObj)
        return cls.cnETFList

    @classmethod
    def getCodeNameMap(cls):
        if cls.codeNameMap == None:
            cls.codeNameMap = {}
            f = open('./data/all_etf.json', 'r')
            content = f.read()
            f.close()
            allETFList = demjson.decode(content)
            if allETFList == None: allETFList = []
            for etf in allETFList:
                cls.codeNameMap[ etf['code'] ] = etf['name']
        return cls.codeNameMap

    def getName(self):
        if self.name == None:
            codeNameMap = self.getCodeNameMap()
            if self.code in codeNameMap:
                self.name = codeNameMap [self.code]
            else:
                self.name = ''
        return self.name

    def dump(self):
        print('code:', self.code, 'name:', self.name)