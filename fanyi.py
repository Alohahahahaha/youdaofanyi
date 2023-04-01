# -*- encoding: utf-8 -*-
# coding=utf-8
"""
@Author: Aloha
@Time: 2023/3/26 16:01
@ProjectName: Practice
@FileName: fanyi.py
@Software: PyCharm
"""
import requests
import execjs
import json
from urllib.parse import quote
import tkinter as tk
from tkinter import *
import threading


class YouDao(object):
    def __init__(self, master):
        self.root = master
        self.root_width = self.root.winfo_screenwidth()
        self.root_height = self.root.winfo_screenheight()
        # 界面大小
        root.geometry(
            '1000x550+' + str(int(self.root_width / 2 - 1000 / 2)) + '+' + str(int(self.root_height / 2 - 550 / 2)))
        # 界面标题
        root.title('翻译')
        # 界面背景颜色
        root.configure(bg='White')
        # 页面
        self.page = tk.Frame(window)
        self.page.configure(bg='White')
        self.page.grid()

        # 创建Canvas对象
        self.canvas = tk.Canvas(root, width=1000, height=550, bg="white")
        self.canvas.pack()

        # 绘制第一个四个角都有弧度的长方形
        self.x1, self.y1, self.x2, self.y2 = 50, 50, 450, 500
        r = 20  # 设置圆角半径
        self.canvas.create_arc(self.x1, self.y1, self.x1 + r, self.y1 + r, start=90, extent=90, fill="white", outline="black")
        self.canvas.create_arc(self.x2 - r, self.y1, self.x2, self.y1 + r, start=0, extent=90, fill="white", outline="black")
        self.canvas.create_arc(self.x1, self.y2 - r, self.x1 + r, self.y2, start=180, extent=90, fill="white", outline="black")
        self.canvas.create_arc(self.x2 - r, self.y2 - r, self.x2, self.y2, start=270, extent=90, fill="white", outline="black")
        self.canvas.create_line(self.x1 + r, self.y1, self.x2 - r, self.y1, fill="black")
        self.canvas.create_line(self.x1 + r, self.y2, self.x2 - r, self.y2, fill="black")
        self.canvas.create_line(self.x1, self.y1 + r, self.x1, self.y2 - r, fill="black")
        self.canvas.create_line(self.x2, self.y1 + r, self.x2, self.y2 - r, fill="black", dash=(4, 4))  # dash时虚线

        # 添加第一个文本框
        self.text_box1 = tk.Text(root, width=40, height=30, bd=0, highlightthickness=0, state='normal')
        self.text_box1.place(x=self.x1 + 50, y=self.y1 + 50)

        # 清空图标
        button = Button(root, text='Clear', command=self.thread_clear)
        button.place(x=473, y=210)

        # 创建一个按钮并绑定事件处理函数
        tran = tk.Button(root, text="Translate", command=self.thread_translate)
        tran.place(x=463, y=260)

        # 绘制第二个四个角都有弧度的长方形
        self.x1, self.y1, self.x2, self.y2 = 550, 50, 950, 500
        r = 20  # 设置圆角半径
        self.canvas.create_arc(self.x1, self.y1, self.x1 + r, self.y1 + r, start=90, extent=90, fill="white", outline="black")
        self.canvas.create_arc(self.x2 - r, self.y1, self.x2, self.y1 + r, start=0, extent=90, fill="white", outline="black")
        self.canvas.create_arc(self.x1, self.y2 - r, self.x1 + r, self.y2, start=180, extent=90, fill="white", outline="black")
        self.canvas.create_arc(self.x2 - r, self.y2 - r, self.x2, self.y2, start=270, extent=90, fill="white", outline="black")
        self.canvas.create_line(self.x1 + r, self.y1, self.x2 - r, self.y1, fill="black")
        self.canvas.create_line(self.x1 + r, self.y2, self.x2 - r, self.y2, fill="black")
        self.canvas.create_line(self.x1, self.y1 + r, self.x1, self.y2 - r, fill="black", dash=(4, 4))
        self.canvas.create_line(self.x2, self.y1 + r, self.x2, self.y2 - r, fill="black")

        # 添加第二个文本框
        self.text_box2 = tk.Text(root, width=40, height=30, bd=0, highlightthickness=0, state='normal')
        self.text_box2.place(x=self.x1 + 50, y=self.y1 + 50)

        # 在两个文本框中间绘制箭头
        self.canvas.create_line(460, 250, 540, 250, width=1, arrow='last', tags='arrow', dash=(4, 4))

        self.url = "https://dict.youdao.com/webtranslate"
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=749413681@10.108.162.135; OUTFOX_SEARCH_USER_ID_NCOO=730233449.255903; P_INFO=15218329192|1673262013|1|dict_logon|00&99|null&null&null#gud&440900#10#0|&0|null|15218329192; UM_distinctid=185965a1ed5b92-0fc83a9930bd3f-26021c51-144000-185965a1ed6dc3; __yadk_uid=HYDYsQclT8Y6m0Xj9fhbHNiGhmS6k8Y4',
            'Origin': 'https://fanyi.youdao.com',
            'Referer': 'https://fanyi.youdao.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }

    def thread_translate(self):
        """将函数打包进线程"""
        # 创建
        t = threading.Thread(target=self.translate)
        # 守护 !!!
        t.setDaemon(True)
        # 启动
        t.start()

    def userInput(self):
        text = self.text_box1.get('1.0', 'end-1c')
        return text

    def thread_clear(self):
        """将函数打包进线程"""
        # 创建
        t = threading.Thread(target=self.clear_input)
        # 守护 !!!
        t.setDaemon(True)
        # 启动
        t.start()

    def clear_input(self):
        self.text_box1.delete('1.0', 'end')
        self.text_box2.delete('1.0', 'end')

    def translate(self):
        text = self.userInput()
        # 参数解密，获取加密数据
        params = execjs.compile(open('translate.js', 'r', encoding='utf-8').read()).call('f', 'fsdsogkndfokasodnaso')
        sign = params['sign']
        my_time = params['t']
        payload = f'i={quote(text)}&from=auto&to=&dictResult=true&keyid=webfanyi&sign={sign}&client=fanyideskweb&product=webfanyi&appVersion=1.0.0&vendor=web&pointParam=client%2CmysticTime%2Cproduct&mysticTime={my_time}&keyfrom=fanyi.web'
        response = requests.post(self.url, headers=self.headers, data=payload).text
        resp = execjs.compile(open('translate.js', 'r', encoding='utf-8').read()).call('data', response)
        res = json.loads(resp)['translateResult']
        user_input = ''
        translate = ''
        for t in res:
            for h in t:
                data = h['src']  # 原文
                translates = h['tgt']  # 翻译
                user_input += data
                translate += translates
        self.thread_show_translate(translate)

    def thread_show_translate(self, data):
        """将函数打包进线程"""
        # 创建
        t = threading.Thread(target=self.show_translate, args=(data,))
        # 守护 !!!
        t.setDaemon(True)
        # 启动
        t.start()

    def show_translate(self, data):
        show = f'{data}\n\n'
        self.text_box2.insert("insert", show)
        # gui界面滑动条自动下拉
        self.text_box2.see('insert')


if __name__ == '__main__':
    root = tk.Tk()
    window = Frame(root)
    window.configure(bg='White')
    window.pack()
    YouDao(window)
    root.mainloop()
