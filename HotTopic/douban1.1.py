import requests
import re
import pymysql

def SearchData(i,j):
	url = "https://www.douban.com/group/explore?start="
	urls = [url + str(num*30) for num in range(i,j)]
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


		d = list(zip(topics, urls, like))

		#last = dict(zip(like, d))
		#last_sort = max(last.items())
        
		for item in d:
			#print(item)
			#print(type(item[1]))
			write(item)
			#print(item)
		

def write(a_set):
# 打开数据库连接
    db = pymysql.connect("localhost","root","123456","test" )
     
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    try:    
        sql1 = """create table data(
                topics varchar(100),
                urls varchar(100),
                likes int 
                )"""
        cursor.execute(sql1)
    except:
    	pass


    sql2 = 'insert into data(topics, urls, likes)values("{0}","{1}",{2})'.format(a_set[0],a_set[1],a_set[2])
    # 使用 execute()  方法执行 SQL 查询 
    cursor.execute(sql2)
    db.commit()


    # 关闭数据库连接
    db.close()	


if __name__ == '__main__':
	SearchData(101,292)
