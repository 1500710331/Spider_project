import re
import time
import random
import datetime
 
import requests
from lxml import etree
import pymysql

from config import *


def get_app_url(page):
	try:
		ip_list = [
			'122.114.82.64:16819',
			'114.215.140.117:16819',
			'116.62.128.50:16819',
			'114.67.228.126:16819',
			'115.28.102.240:16819',
			'117.48.201.187:16819',
			'121.41.11.179:16819',
			'121.42.140.113:16819',
			'123.57.67.124:16819',
			'43.226.164.156:16819'
		]
		global proxies
		global header
		proxies = {'http': 'http://zhangqm:z23lb6t1@%s' % random.choice(ip_list)}
		url = 'http://www.anzhi.com/search.php?keyword=&page='
		header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
		html = requests.get(url + str(page), headers=header, proxies=proxies, timeout=10)
		html.encoding = html.apparent_encoding
		print('page-status = {}  {}'.format(page,html.status_code))
		pattern = re.compile(r'<span class="app_name"><a href="(.*?)">.*?</a></span>', re.S)
		app_url = re.findall(pattern, html.text)
		if app_url == []:
			print('爬取完成，退出~')
			main(H, M, W)
		for app in app_url:
			get_detail(app)
	except Exception as err:
		print(err)
		get_app_url(page)


def get_detail(url):
	try:
		app_url = 'http://www.anzhi.com' + url
		html2 = requests.get(app_url, headers=header, proxies=proxies, timeout=10)
		if html2.status_code == 200:
			html2.encoding = html2.apparent_encoding
			html_text = html2.text
			html_final = etree.HTML(html_text)
			try:
				global app_data 
				app_data = {
					'name': html_final.xpath('//h3/text()')[3],
					'classify': html_final.xpath('//*[@id="detail_line_ul"]/li[1]/text()')[0][3:],
					'time': html_final.xpath('//*[@id="detail_line_ul"]/li[3]/text()')[0][3:],
					'sys': html_final.xpath('//*[@id="detail_line_ul"]/li[5]/text()')[0][3:],
					'creator': html_final.xpath('//*[@id="detail_line_ul"]/li[7]/text()')[0][3:],
					'download_num': html_final.xpath('//span[@class="spaceleft"]/text()')[0][3:],
					'size': html_final.xpath('//span[@class="spaceleft"]/text()')[1][3:],
					'charge': html_final.xpath('//*[@id="detail_line_ul"]/li[6]/span/text()')[0][3:],
					'language': html_final.xpath('//*[@id="detail_line_ul"]/li[8]/text()')[0][5:]
				}
			except:
				pass
			# print('app_data:{}'.format(app_data))
			time.sleep(0.8)
			save_mysql()
		else:
			print(html2.status_code)
	except Exception as err:
		print(err)
		get_detail(url)


def save_mysql():
	try:
		global db
		db = pymysql.connect('172.17.98.1', 'spider', 'Za123456@', 'anzhi')
		cursor = db.cursor()
		sql1 = ''' show tables like 'android_app' '''
		cursor.execute(sql1)
		row_1 = cursor.fetchone()[0]
		if row_1 != 'android_app':
			sql1 = '''CREATE TABLE android_app(
					NAME CHAR(80),
					CLASSIFY CHAR(80),
					TIME CHAR(80),
					SYS CHAR(80),
					CREATOR CHAR(50),
					DOWNLOAD_NUM CHAR(50),
					SIZE CHAR(50),
					CHARGE CHAR(50),
					LANGUAGE CHAR(50) )'''
			cursor.execute(sql1)
		dbname = update(app_data['name'], app_data['creator'])
		result = (app_data['name'], app_data['creator'],)
		if dbname == result:
			print('{}存在！无需存储'.format(app_data['name']))
		else:
			sql2 = '''INSERT INTO android_app(NAME, CLASSIFY, TIME, SYS, CREATOR, DOWNLOAD_NUM, SIZE, CHARGE, LANGUAGE)
					VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'''.format(
					app_data['name'],
					app_data['classify'],
					app_data['time'],
					app_data['sys'],
					app_data['creator'],
					app_data['download_num'],
					app_data['size'],
					app_data['charge'],
					app_data['language'])
			cursor.execute(sql2)
			db.commit()
			print('存储成功！')
	except Exception as err:
		print(err)
		db.rollback()
	finally:
		db.close()


def update(name, creator):
	cursor = db.cursor()
	sql = ''' select name, creator from android_app where name = "{}" and creator = "{}" '''.format(name, creator)
	cursor.execute(sql)
	row1 = cursor.fetchone()
	return row1

def main(H, M, W):
	while True:
		now = datetime.datetime.now()
		print(now.hour, now.minute, now.isoweekday())
		if now.hour == H and now.minute == M and now.isoweekday() == W:
			break
		time.sleep(60)

	pages = range(FIRST_PAGE, LAST_PAGE)#22095
	for page in pages:
		get_app_url(page)


if __name__ == '__main__':
	main(H, M, W)