import urllib.request
import re


top_num = 1

url = 'https://movie.douban.com/top250?start='
urls = [url + str(num*25)for num in range(4)]

for url in urls:    

    html = urllib.request.urlopen(url).read().decode('utf-8')

        
    top_tag = re.compile(r'<span class="title">(.*)</span>')

    title = re.findall(top_tag,html)

    for  i in title:
        if i.find('/') == -1:          
            print('Top'+str(top_num) + ' ' + i)
            top_num += 1
             
