#coding=utf-8

from conf import CONF
from agileutil.log import Log

logger = None

def get_logger(logger_name):
    global logger
    if logger == None:
        logger = {}
    if logger_name in logger:
        return logger.get(logger_name)
    if logger_name not in CONF.get('log'):
        raise Exception('logger_name not found')
    if 'file' not in CONF.get('log').get(logger_name):
        raise Exception('file node not found')
    logger[logger_name] = Log(CONF.get('log').get(logger_name).get('file'))
    return logger.get(logger_name)