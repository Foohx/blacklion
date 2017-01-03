# coding: utf-8
import sys
import time
import random
import shutil
import requests
from lxml import html

n = 1
while n:
    s = requests.session()
    r = s.get('http://www.google.com/recaptcha/api/noscript?k=6Lf5ztsSAAAAADHGj627J-3EUXNXlmfGa_q501JK')

    captcha = html.fromstring(r.content)
    captcha = captcha.xpath('//img/@src')
    captcha = "https://www.google.com/recaptcha/api/" +captcha[0]

    # print(captcha)
    r = requests.get(captcha, stream=True)
    with open('captchas/'+str(n)+'.png', 'wb') as o:
        shutil.copyfileobj(r.raw, o)
    del r
    del s
    n = n+1
