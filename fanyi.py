# -*- encoding: utf-8 -*-
# coding=utf-8
import time
import random
import requests
from hashlib import md5


class YdTranslate(object):
    def __init__(self):
        # self.keyword = input('请输入你要翻译的词汇:')
        self.url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.headers = {
        }

    def get(self, keyword):
        lts = str(int(time.time() * 1000))
        salt = lts + str(int(10 * random.random()))
        s = md5()
        string = "fanyideskweb" + keyword + salt + "Ygy_4c=r#e#4EX^NUGUc5"
        s.update(string.encode())
        sign = s.hexdigest()
        return lts, salt, sign

    def get_data(self, keyword):
        lts, salt, sign = self.get(keyword)
        data = {
            'i': keyword,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salt,
            'sign': sign,
            'lts': lts,
            'bv': '56d33e2aec4ec073ebedbf996d0cba4f',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME',
        }
        res = requests.post(self.url, headers=self.headers, data=data).json()
        print(res)


if __name__ == '__main__':
    YdTranslate().get_data('where are you now')
