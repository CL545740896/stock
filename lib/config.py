#coding=utf-8

import demjson

class Config:

    def __init__(self, confPath):
        self.confPath = confPath
        self.data = {}
        self.reload()

    def reload(self):
        f = open(self.confPath, 'r')
        content = f.read()
        f.close()
        try:
            data = demjson.decode(content)
            self.data = data
        except:
            pass
        return self

    def isOK(self):
        f = open(self.confPath, 'r')
        content = f.read()
        f.close()
        try:
            data = demjson.decode(content)
        except:
            return False
        return True