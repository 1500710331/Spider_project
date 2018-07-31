'''
抓取博客时间和标题
'''




from urllib.request import urlopen
import re

a = ['','/page/2','/page/3','/page/4','/page/5','/page/6']

for m in a:
    url = 'http://opslinux.com/archives%s'%(m)

    html = urlopen(url).read().decode('utf-8')


    pattern = re.compile(r'<time datetime=".*" itemprop=".*">(.*)</time>')

    date_str = re.findall(pattern, html)

    #print(date_str)


    pattern_title = re.compile(r'<h1 itemprop="name">(.*)</h1>')

    title_str = re.findall(pattern_title,html)

    #print(title_str)


    for i,j in zip(date_str,title_str):
        print(i,j)

    
