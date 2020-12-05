#coding=utf-8

from high_prob_rose_strategy import HighProbRoseStrategy
import init

def business():
    HighProbRoseStrategy.logger = init.get_logger('app')
    HighProbRoseStrategy.run(beforeDayNum = 15)