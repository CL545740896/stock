#coding=utf-8

class UniQueue:

    def __init__(self, asyncTag = True):
        self.queue = set()
        self.asyncTag = asyncTag

    instance = None
    @classmethod
    def getInstance(cls):
        if cls.instance == None:
            cls.instance = UniQueue()
        return cls.instance

    def push(self, elem):
        self.queue.add(elem)

    def pop(self):
        if self.asyncTag:
            try:
                elem = self.queue.pop()
            except:
                return None
            return elem
        return self.queue.pop()