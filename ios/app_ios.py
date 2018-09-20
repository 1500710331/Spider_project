import requests
from lxml import etree
import json
import pymysql
import random


def get_app(num):	
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
		proxies = {'http': 'http://zhangqm:z23lb6t1@%s' % random.choice(ip_list)}
		#print(proxies)
		header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
		url = "https://www.i4.cn/app_detail_{}.html".format(str(num))
		html = requests.get(url, headers=header, proxies=proxies)
		html.encoding = html.apparent_encoding
		ht = html.text
		if html.status_code == 200:
			print(num)
			html = etree.HTML(ht)
			title = html.xpath('/html/head/title/text()')[0]
			if title == 'ERROR 404 您访问的页面不存在':
				pass
			else:
				get_detail(ht)
				print("有效utl:"+str(num))
	except Exception as e:
		print(e)
		get_app(num)




def get_detail(wb_data):
	html = etree.HTML(wb_data)
	title = html.xpath('/html/head/title/text()')[0]	
	app = {
		'name': html.xpath('//*[@id="app_detail"]/div/div/div[1]/div[1]/div[2]/div[1]/div[1]/text()')[0],
		'version': html.xpath('//*[@id="app_detail"]/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/span/text()')[0],
		'type': html.xpath('//*[@id="app_detail"]/div/div/div[1]/div[1]/div[2]/div[2]/div[5]/span/text()')[0],
		'author': html.xpath('//*[@id="app_detail"]/div/div/div[1]/div[1]/div[2]/div[2]/div[7]/span/text()')[0],
		'sys': html.xpath('//*[@id="app_detail"]/div/div/div[1]/div[1]/div[2]/div[2]/div[8]/span/text()')[0],
		'date': html.xpath('//*[@id="app_detail"]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/span/text()')[0],
		'downcount': html.xpath('//*[@id="app_detail"]/div/div/div[1]/div[1]/div[2]/div[2]/div[4]/span/text()')[0],
		'language': html.xpath('//*[@id="app_detail"]/div/div/div[1]/div[1]/div[2]/div[2]/div[6]/span/text()')[0]
	}
	#print(app)
	save_mysql(app)

	
def save_mysql(app):
	try:
		db = pymysql.connect('172.17.98.1', 'spider', 'Za123456@', 'anzhi')
		cursor = db.cursor()
		sql1 = ''' show tables like 'ios_app' '''
		cursor.execute(sql1)
		row_1 = cursor.fetchone()[0]
		if row_1 != 'ios_app':
			sql2 = '''CREATE TABLE ios_app2(              #建表
					NAME CHAR(50),
					VERSION CHAR(60),
					TYPE CHAR(60),
					AUTHOR CHAR(80),
					SYS CHAR(100),
					DATE CHAR(80),
					DOWNCOUNT CHAR(50),
					LANGUAGE CHAR(80))'''
			cursor.execute(sql2)
		dbname = update(app['name'], app['version'])
		result = (app['name'], app['version'],)
		if result == dbname:
			print('此app存在！')
		else:
			sql3 = '''INSERT INTO ios_app(NAME, VERSION, TYPE, AUTHOR, SYS, DATE, DOWNCOUNT, LANGUAGE) #存储
			VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'''.format(
				app['name'],
				app['version'],
				app['type'],
				app['author'],
				app['sys'],
				app['date'],
				app['downcount'],
				app['language'])
			cursor.execute(sql3)
			db.commit()
			print('入库ok')
	except Exception as e:
		print(e)
		db.rollback()
	finally:
		db.close()


def update(name, version):
	db = pymysql.connect('172.17.98.1', 'spider', 'Za123456@', 'anzhi')
	cursor = db.cursor()
	sql = ''' select name, version from ios_app where name = '{}' and version = '{}' '''.format(name, version)
	# print(sql)
	cursor.execute(sql)
	row1 = cursor.fetchone()
	return row1
		

def main():
	nums = range(1, 300000)#165353 
	for num in nums:
		get_app(num)

if __name__ == '__main__':
	main()