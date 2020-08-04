#coding=utf-8

import demjson

class ETF:

    allETFList = None
    cnETFList = None
    codeNameMap = None

    def __init__(self, code):
        self.code = code
        self.name = None

    @classmethod
    def getAllETFList(cls):
        if cls.allETFList == None:
            f = open('./data/all_etf.json', 'r')
            content = f.read()
            f.close()
            cls.allETFList = demjson.decode(content)
        return cls.allETFList

    @classmethod
    def getCnETFList(cls):
        if cls.cnETFList == None:
            f = open('./data/cn_etf_list.json', 'r')
            content = f.read()
            f.close()
            cls.cnETFList = demjson.decode(content)
        return cls.cnETFList

    @classmethod
    def getCodeNameMap(cls):
        if cls.codeNameMap == None:
            cls.codeNameMap = {}
            etfList = cls.getAllETFList()
            if etfList == None: etfList = []
            for etf in etfList:
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