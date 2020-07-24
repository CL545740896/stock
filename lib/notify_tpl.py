#coding=utf-8

class NotifyTpl:

    def __init__(self):
        pass

    ACTION_BUY = '买入'
    ACTION_SALE = '卖出'

    commonTpl = '您关注的股票 [%s] 当前价格 [%s] 满足 [%s] 条件 %s'
    highProbStraTpl = '%s：股票[%s],代码[%s],当前价格[%s],为最近%s天振荡的最低价格，满足策略[HIGH_PROB_ROSE_STRA]'

    @classmethod
    def genNotify(cls, name, now, action, args = ''):
        string = cls.commonTpl % (name, now, action, args)
        return string

    @classmethod
    def genHighProbStrategyNotify(cls, action, name, code, now, ndays):
    	string = cls.highProbStraTpl % (action, name, code, now, ndays,)
    	return string