import requests
import re 
from bs4 import BeautifulSoup

url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2018.html'

html = requests.get(url)
html.encoding = html.apparent_encoding
pattern = re.compile(r'<div.*?align="left">(.*?)</div></td><td>(.*?)</td><td>(.*?)</td><td.*?>(.*?)</td>', re.S)
schooldatas = re.findall(pattern, str(html.text))

for schooldata in schooldatas:
	print(list(schooldata))

