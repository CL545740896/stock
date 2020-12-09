#coding=utf-8

from high_prob_rose_strategy import HighProbRoseStrategy
import init

def business():
    for i in [15, 16, 17, 18, 19, 20]:
        HighProbRoseStrategy.logger = init.get_logger('app')
        HighProbRoseStrategy.run(beforeDayNum = 15)