import requests
from bs4 import BeautifulSoup

url = "http://www.ip38.com/ip.php?ip="
ip = input("请输入需查询的IP地址：")
html1 = requests.get(url+ip)
html = html1.text
soup = BeautifulSoup(html, 'html.parser')
Font = soup.find_all("font")
#print(soup.prettify())
addr = Font[3].string
print("IP详细地址为：" + addr)