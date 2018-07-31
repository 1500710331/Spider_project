import urllib.request
import re

a=0
top_num = 1
for i in range(4):
    a = i*25


    url = 'https://movie.douban.com/top250?start=%d&filter='%(a)

    html = urllib.request.urlopen(url).read().decode('utf-8')


    
    top_tag = re.compile(r'<span class="title">(.*)</span>')

    title = re.findall(top_tag,html)

    for  i in title:
        if i.find('/') == -1:          
            print('Top'+str(top_num) + ' ' + i)
            top_num += 1
         
