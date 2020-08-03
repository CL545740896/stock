#coding=utf-8

class NotifyTpl:

    def __init__(self):
        pass

    ACTION_BUY = '买入'
    ACTION_SALE = '卖出'

    commonTpl = '您关注的股票 [%s] 当前价格 [%s] 满足 [%s] 条件 %s'
    #highProbStraTpl = '%s股票[%s],代码[%s],当前价格[%s]为最近[%s]个交易日振荡的最低价,动态市盈率[%s],静态市盈率[%s],满足策略[HIGH_PROB_ROSE_STRA]'
    highProbStraTpl = '%s:股票[%s][%s],当前价格[%s],是最近[%s]个交易日振荡最低价,动态市盈率[%s],静态市盈率[%s],市净率[%s],反弹率[%s],策略[HIGH_PROB_ROSE_STRA]'
    hisBuyProfitTpl = '%s:股票[%s][%s],当前价格[%s],小于历史买入盈利价格[%s],策略[HIS_BUY_PROFIT_STRA]'
    stillRoseTpl = '%s:股票[%s][%s],连续[%s]个交易日上涨，当前价格:[%s], 策略[STILL_ROSE_STRA]'

    @classmethod
    def genNotify(cls, name, now, action, args = ''):
        string = cls.commonTpl % (name, now, action, args)
        return string

    @classmethod
    def genHighProbStrategyNotify(cls, action, name, code, now, ndays, dyPe, staPe, pb, roseRate):
    	string = cls.highProbStraTpl % (action, name, code, now, ndays,dyPe, staPe, pb, roseRate)
    	return string

    @classmethod
    def genHisBuyProfitNotify(cls, action, name, code, now, price):
    	string = cls.hisBuyProfitTpl % (action, name, code, now, price)
    	return string

    @classmethod
    def genStillRoseNotify(cls, action, name, code, ndays, now):
        string = cls.stillRoseTpl % (action, name, code, ndays, now)
        return string