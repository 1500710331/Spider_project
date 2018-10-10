import requests
from lxml import etree 
import re


def get_main_url():
	header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
	start_url = ['http://bus.mapbar.com/guilin/poi_']*24
	a = ['1', '4', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'W', 'X', 'Y', 'Z']
	urls = [start_url[i]+a[i] for i in range(24)]
	for url in urls:
		get_station_url(url)


def get_station_url(url):
	html = requests.get(url)
	if html.status_code == 200:
		html.encoding = html.apparent_encoding
		page = html.text
		pattern = re.compile(r'<dd>(.*?)</dd>', re.S)
		station_detail = re.findall(pattern, page)
		s = station_detail[:-2]
		for station_url in s:
			pattern2 = re.compile(r'<a href="(.*?)"', re.S)
			station_url_list = re.findall(pattern2, station_url)
			for station_url in station_url_list:
				get_station_detail(station_url)
				# print(station_url)


def get_station_detail(station_url):
	html = requests.get(station_url)
	if html.status_code == 200:
		html.encoding = html.apparent_encoding
		page = html.text
		pattern = re.compile(r'<h1 class="topH1">(.*?)</h1>', re.S)
		station_name = re.findall(pattern, page)[0]
		html_final = etree.HTML(page)
		zhoubian = html_final.xpath('//*[@id="bodyid"]/div[3]/div[1]/div[1]/div/div[2]/a/text()')
		if zhoubian == []:
			zhoubian = "null"
		else:
			zhoubian = zhoubian[0]
		bus = html_final.xpath('//*[@id="bodyid"]/div[3]/div[1]/div[1]/div/div[2]/p/a/text()')
		station = {'station': station_name, 'zhoubian': zhoubian, 'bus': bus}
		print(station)


if __name__ == '__main__':
	get_main_url()


