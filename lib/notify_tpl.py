class NotifyTpl:

    def __init__(self):
        pass

    ACTION_BUY = '买入'
    ACTION_SALE = '卖出'

    commonTpl = '您关注的股票 [%s] 当前价格 [%s] 满足 [%s] 条件 %s'

    @classmethod
    def genNotify(cls, name, now, action, args = ''):
        string = cls.commonTpl % (name, now, action, args)
        return string