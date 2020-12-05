#coding=utf-8

import init
import time
from business import business

logger = init.get_logger('app')

def main():
    while 1:
        try:
            business()
        except Exception as ex:
            logger.error('global exception:', ex)
            time.sleep(2)

if __name__ == '__main__':
    main()