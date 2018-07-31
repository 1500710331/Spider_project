import urllib.request
import urllib.parse
import json
import os



'''
爬虫有道翻译
'''
content = input('（Enter开始）——即将开始翻译——（q退出）')

while(content != 'q' ):
    content = input('请输入要翻译的内容：')
    if(content != 'q'):      
        url='http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&sessionFrom='
        data = {}

        data['i']= content
        data['from'] = 'AUTO'
        data['to'] = 'AUTO'
        data['smartresult'] = 'dict'
        data['client'] = 'fanyideskweb'
        data['salt'] = '1532219375982'
        data['sign'] = '2e9a1136ef4f6580003f8c6d0b0f4795'
        data['doctype'] = 'json'
        data['version'] = '2.1'
        data['keyfrom'] = 'fanyi.web'
        data['action'] = 'FY_BY_CLICKBUTTION'
        data['typoResult'] = 'false'
        data = urllib.parse.urlencode(data).encode('utf-8')

        response = urllib.request.urlopen(url,data)
        html = response.read().decode('utf-8')


        target = json.loads(html)

        print("翻译结果:%s" % target['translateResult'][0][0]['tgt'])
        continue
    else:
        break
os.system('pause')
