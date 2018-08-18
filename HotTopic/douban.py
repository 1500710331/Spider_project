import requests
import re

	
url = "https://www.douban.com/group/explore?start="
urls = [url + str(num*30) for num in range(10)]
	#print(url)
for url in urls:	
	head = {}
	head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'

	html = requests.get(url,headers=head)
	html.encoding = 'utf-8'

	#匹配出热门度
	pattern = re.compile(r'<div class="likes">(.*?)<br>', re.S)
	like = re.findall(pattern, html.text)
	like = map(int, like)
	#print(like)

	#匹配出热门话题和url
	pattern2 = re.compile(r'<h3><a href="(.*?)">(.*?)</a>', re.S)
	data = re.findall(pattern2, html.text)
	#print(topic)
	urls = []
	topics = []
	for url in data:
		urls.append(url[0])
		topics.append(url[1])


	d = list(zip(topics, urls))
	last = dict(zip(like, d))
	last_sort = max(last.items())


	for item in last_sort:
		print(item)



	

