#coding=utf-8

from multiprocessing import Process

def spawn_process(func):
    p = Process(target=func)
    p.start()

