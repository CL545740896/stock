from lib.config import Config
import sys

conf = Config("./config.json")
if not conf.isOK():
    print('conf has syntax error')
    sys.exit()

for stock in conf.reload().data['stockList']:
    