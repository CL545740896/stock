import requests
import demjson

def fetch_by_page(page: int, size: int):
	headers = {
		'Host' : 'xueqiu.com',
		'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
		'Cookie' : 's=d811jej3wn; device_id=7a4981ca5bec19d55e5b932ebdd7a3b4; remember=1; xq_a_token=44660516faae1917b9bde3f022208047fc0c3b0a; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjQ5NTA4NzY3OTUsImlzcyI6InVjIiwiZXhwIjoxNTk4NDIyMzg1LCJjdG0iOjE1OTU4MzAzODU1OTYsImNpZCI6ImQ5ZDBuNEFadXAifQ.Yv9WLDDLZBgSW1nNt99vlsRO5Y5CjuRlya1yaTs5_jjKoEENqI1z6-Dgvsbq-em4ihhpvVWlrUY5Xed0HlaRRBND0mG4CBLvtW-zLKEdzGbEVn1MbwQoGTfJdjPFDVDM3m-x6x8-oIm6iwMZjvR_k817BrudJeMGvtFcEEqeR3mJ9_bFC90F8EFqxc99_IdEdi2Fgbe6GUkzVzVz2nsy8sfqL7-eiZ_sx33eNazkVboupnXYx7Mj_4QGcV2GXUSYBBU5C2GPTwE7i8t4l9m_7THtD0yHeK4vkseKeS9E6SbJ1HUFN-qD41-U3MWXvHislKsDuGuI026xn9y-DyHPjQ; xqat=44660516faae1917b9bde3f022208047fc0c3b0a; xq_r_token=e3fa7d697e27d4f81a96060ff8fcf1c4fd711555; xq_is_login=1; u=4950876795; bid=65ccfc7cf5c638f60edd7e3ff1c99c46_kd49ts2w; aliyungf_tc=AQAAAIDsHQECpAsAJ6F5arUJYkDK/qOT; acw_tc=2760822615965268435183869e902946a8f384ae8a3c2ce6675b144ff4ed57; Hm_lvt_1db88642e346389874251b5a1eded6e3=1595839626,1595840055,1596446311,1596526846; __utma=1.285592886.1596526970.1596526970.1596526970.1; __utmc=1; __utmz=1.1596526970.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=1.1.10.1596526970; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1596527234',
		'ragma': 'no-cache',
		'Sec-Fetch-Dest' : 'document',
		'Sec-Fetch-Mode' : 'navigate',
		'Sec-Fetch-Site' : 'none',
		'Sec-Fetch-User' : '?1',
		'Upgrade-Insecure-Requests' : '1',
	}
	url = 'https://xueqiu.com/stock/search.json?code=ETF&size=%s&page=%s' % (size, page)
	print(url)
	r = requests.get(url, headers = headers, timeout = 5)
	print('status_code:', r.status_code)
	if r.status_code != 200: return []
	res = demjson.decode(r.content)
	stocks = res['stocks']
	print(len(stocks))
	return stocks

all_stocks = []
for i in range(60):
	stocks = fetch_by_page(i+1, 50 )
	for etf in stocks:
		all_stocks.append({
			'code' : etf['code'],
			'name' : etf['name'],
		})

content = demjson.encode(all_stocks)
f = open('./etf.json', 'w')
f.write(content)
f.close()