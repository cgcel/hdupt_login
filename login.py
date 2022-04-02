# !/usr/env/python3
# -*- coding: utf-8 -*-
# author: elvin

import re
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs

from img import MyImg

url_root = 'https://pt.hdupt.com/'
url_login_get = 'https://pt.hdupt.com/login.php'
url_login_post = 'https://pt.hdupt.com/takelogin.php'
url_index = 'https://pt.hdupt.com/index.php'
url_signin = 'https://pt.hdupt.com/added.php'
url_img = 'https://pt.hdupt.com/image.php?action=regimage&imagehash={}'


class HduLogin(object):

    def __init__(self, *args):

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'referer': 'https://pt.hdupt.com/index.php',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
        }

        self.session = requests.Session()
        self.session.headers.update(headers)
        self.retry_time = 0
        self.flag = False

        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # 打印时间

        if len(sys.argv) == 3:  # 获取命令行参数
            self.username = sys.argv[1]
            self.password = sys.argv[2]
            self.login()
            if self.flag:
                self.signin()
        elif len(sys.argv) > 1 and len(sys.argv) != 3:
            print("参数格式错误, 请按照 python login.py username password 来输入")
            return
        else:
            self.username = args[0]
            self.password = args[1]
            self.login()
            if self.flag:
                self.signin()

    def login(self):
        """登录函数
        """
        r = self.session.get(url_login_get)

        pattern = re.compile(r'imagehash=(.*?)"')
        image_hash = pattern.findall(r.text)[0]

        url_image = url_img.format(image_hash)

        with open("image.png", "wb") as img:
            img.write(requests.get(url_image).content)

        captcha_str = MyImg("image.png").get_str()
        print("OCR识别验证码: {}".format(captcha_str))

        form_data = {
            'username': self.username,
            'password': self.password,
            'imagestring': captcha_str,
            'imagehash': image_hash
        }

        self.session.post(url_login_post, data=form_data)
        r = self.session.get(url_index)
        try:
            if len(re.findall('欢迎回来', r.text)) == 1:
                self.flag = True
                return
            else:
                self.retry_time += 1
                if self.retry_time < 6:
                    print("登录失败, 重试{}次...".format(self.retry_time))
                    self.login()
                else:
                    print("多次尝试登录失败, 退出程序")
                    return
        except:
            pass

    def signin(self):
        """签到函数
        """
        r = self.session.get(url_index)
        soup = bs(r.content, "html.parser")
        if not soup.find("a", {"onclick": "javascript:qiandao('qiandao')"}):
            print("无需重复签到")
            return
        form_data = {"action": "qiandao"}
        self.session.post(url_signin, data=form_data)
        r = self.session.get(url_index)
        soup = bs(r.content, "html.parser")
        if not soup.find("a", {"onclick": "javascript:qiandao('qiandao')"}):
            print("签到成功")


if __name__ == '__main__':
    # HduLogin('username', 'password')
    HduLogin()
