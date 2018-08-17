import requests
from bs4 import BeautifulSoup
import re 

url = "http://www.biqukan.com/0_790/"
html = requests.get(url)
html.encoding = html.apparent_encoding

soup = BeautifulSoup(html.text, "html.parser")
#print(soup.prettify())

dd_tag = soup.find_all("dd")
dd = str(dd_tag)
patten = re.compile(r'<dd>.*?href="(.*?)"')
urls = re.findall(patten, dd)[:30]
#print(urls)

for final_urls in urls:
	url2 = "http://www.biqukan.com"+final_urls
	html2 = requests.get(url2)
	html2.encoding = html2.apparent_encoding
	soup2 = BeautifulSoup(html2.text, "html.parser")
	#print(title)
	#print(soup2.prettify())
	

	title = soup2.find_all("h1")
	pattern2 = re.compile(r'<h1>(.*?)</h1>', re.S)
	tt = str(title[0])
	title_final = re.findall(pattern2, tt)
	titles =  title_final[0]
	


	text = soup2.find_all("div", {"id": "content"})
	pattern3 = re.compile(r'<div.*?>(.*?)</div>', re.S)
	text1 = str(text[0])
	text_final = re.findall(pattern3, text1)
	texts = text_final[0]
	



	n = urls.index(final_urls)+1


	with open('novel%d'%n, 'w') as f:
		f.write(str(titles))
		f.write(str(texts))


