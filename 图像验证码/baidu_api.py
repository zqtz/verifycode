import urllib.request
import re
import base64
import requests

host = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=oa6VVGS7ldI5GG1e3fHrgvB6&client_secret=xdaZFWKnqt2Hsxvnpd2GDo2QNpfGrHLQ&"
response = requests.get(host)
if response:
    access_token = re.findall(r'"access_token":"(.*?)"', response.text)[0]

'''
通用文字识别（高精度版）
'''
request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
# 二进制方式打开图片文件
f = open('fetch.jpg', 'rb')
img = base64.b64encode(f.read())
params = {"image": img}
access_token = access_token
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print(response.json()['words_result'][0]['words'])