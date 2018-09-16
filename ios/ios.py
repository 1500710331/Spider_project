import requests
from lxml import etree
import json


def get_app():
	for num in range(113597, 300000):
		#188661

		url = "https://www.i4.cn/app_detail_{}.html".format(str(num))
		html = requests.get(url)
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
	save_json(app)

def save_json(app):
	content = json.dumps(app, ensure_ascii = False) + ',\n'
	with open('app.json', 'ab') as f:
		f.write(content.encode('utf-8'))
    



def main():
	get_app()

if __name__ == '__main__':
	main()