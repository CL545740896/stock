import demjson

f = open('../data/all_etf.json', 'r')
content = f.read()
f.close()
etfList = demjson.decode(content)
cnETFList = []
for etf in etfList:
    code = etf['code']
    if len(code) < 8: continue
    prefix = code[0] + code[1]
    if prefix in ['SH', 'SZ', 'sh', 'sz']:
        cnETFList.append(etf)
f = open('../data/cn_etf_list.json', 'w')
content = demjson.encode(cnETFList)
f.write(content)