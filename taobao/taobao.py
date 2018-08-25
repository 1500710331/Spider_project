from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from config import *
import pymongo
import re

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

#初始化浏览器
option = webdriver.ChromeOptions()
option.add_argument('headless')
browser = webdriver.Chrome(chrome_options=option)
wait = WebDriverWait(browser, 10)


#搜索页面
def search():
	try:
		browser.get('https://www.taobao.com')
		#指定输入框的css选择器
		input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
		#提交按钮的选择器
		submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
		input.send_keys(KEYWORD)
		submit.click()
		total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total")))
		get_products()
		return total.text
	except:
		return search()


#翻页功能
def next_page(page_number):
	try:
		input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
		submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
		input.clear()
		input.send_keys(page_number)
		submit.click()
		wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
		get_products()
	except:
		next_page(page_number)


#爬下产品信息
def get_products():
	wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
	html = browser.page_source
	doc = pq(html)
	items = doc('#mainsrp-itemlist .items .item').items()
	for item in items:
		product = {
		'image': 'http:' + item.find('.pic .img').attr('data-src'),
		'price': item.find('.price').text(),
		'deal': item.find('.deal-cnt').text()[:-3],
		'title': item.find('.title').text(),
		'shop': item.find('.shop').text(),
		'location': item.find('.location').text()
		}
		
		save_to_mongo(product)
		#print(product)


#存入mongodb
def save_to_mongo(result):
	try:	
		if db[MONGO_TABLE].insert(result):
			print('存储到MONGODB成功', result)
	except Exception:
		print('存储到MONGODB失败', result)



def main():
	total = search()
	total = int(re.compile('(\d+)').search(total).group())
	for i in range(2, total + 1):
		next_page(i)
	browser.close()


if __name__ == '__main__':
	main()