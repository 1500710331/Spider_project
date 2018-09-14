import re
import requests
from lxml import etree
import pymongo
import random
import pymysql


def get_app_url():
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
        pages = range(1, 14643)
        url = 'http://www.anzhi.com/search.php?keyword=&page='
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        for page in pages:
            print('第%d页'%page)
            html = requests.get(url + str(page), headers=header, proxies=proxies)
            html.encoding = html.apparent_encoding
            pattern = re.compile(r'<span class="app_name"><a href="(.*?)">.*?</a></span>', re.S)
            app_url = re.findall(pattern, html.text)
            for app in app_url:
                get_detail(app)
    except Exception as err:
        print("1"+err)
        get_app_url()


def get_detail(url):
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
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        app_url = 'http://www.anzhi.com' + url
        html = requests.get(app_url, proxies=proxies, headers=header)
        html.encoding = html.apparent_encoding
        html_text = html.text
        html_final = etree.HTML(html_text)

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
        save_mysql(app_data)
    except Exception as err:
        print("data:"+err)


def save_mysql(app_data):
    try:
        db = pymysql.connect('localhost', 'root', '123456', 'st')
        cursor = db.cursor()
        # sql1 = '''CREATE TABLE APP (
        #         NAME CHAR(10),
        #         CLASSIFY CHAR(20),
        #         TIME CHAR(30),
        #         SYS CHAR(20),
        #         CREATOR CHAR(50),
        #         DOWNLOAD_NUM CHAR(20),
        #         SIZE CHAR(20),
        #         CHARGE CHAR(20),
        #         LANGUAGE CHAR(20) )'''
        # cursor.execute(sql1)
        sql2 = '''INSERT INTO APP(NAME, CLASSIFY, TIME, SYS, CREATOR, DOWNLOAD_NUM, SIZE, CHARGE, LANGUAGE)
                VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')'''.format(
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
    except Exception as err:
        print("save"+err)
        db.rollback()
    finally:
        db.close()


def main():
    get_app_url()


if __name__ == '__main__':
    main()
