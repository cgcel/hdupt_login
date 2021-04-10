# -*- coding: utf-8 -*-
# author: elvin

import requests
from bs4 import BeautifulSoup as bs
import sys
from img import MyImg

url_root = 'https://pt.hdupt.com/'
url_login_get = 'https://pt.hdupt.com/login.php'
url_login_post = 'https://pt.hdupt.com/takelogin.php'
url_index = 'https://pt.hdupt.com/index.php'
url_signin = 'https://pt.hdupt.com/added.php'


class HduLogin(object):
    def __init__(self, *args):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            # 'content-length': '98',
            # 'content-type': 'application/x-www-form-urlencoded',
            # 'origin': 'https://pt.hdupt.com',
            'referer': 'https://pt.hdupt.com/login.php',
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

        if len(sys.argv) > 1:
            self.username = sys.argv[1]
            self.password = sys.argv[2]
        else:
            self.username = args[0]
            self.password = args[1]

        self.retry_time = 0

    # 登录函数
    def login(self):
        r = self.session.get(url_login_get)
        soup = bs(r.content, "lxml")

        image_hash = soup.find(
            "input", {"type": "hidden", "name": "imagehash"})['value']
        image_src = soup.find("img", {"border": "0", "alt": "CAPTCHA"})['src']
        url_image = url_root + image_src

        with open("image.png", "wb") as img:
            img.write(requests.get(url_image).content)
        captcha_str = MyImg("image.png").get_str()
        print(captcha_str)
        # captcha_str = input("输入验证码: ")

        form_data = {
            'username': self.username,
            'password': self.password,
            'imagestring': captcha_str,
            'imagehash': image_hash
        }
        self.session.post(url_login_post, data=form_data)
        r = self.session.get(url_index)
        soup = bs(r.content, "lxml")
        # print(soup.find("a", {"class":"User_Name"}))
        # print(soup.find("a", {"onclick":"javascript:qiandao('qiandao')"}))

        try:
            if soup.find("a", {"class": "User_Name"}).get_text() == self.username:
                print("登录成功")
        except:
            self.retry_time += 1
            if self.retry_time < 6:
                print("登录失败, 重试{}次...".format(self.retry_time))
                self.login()
            else:
                print("多次尝试登录失败, 退出程序")
                return

    # 签到函数
    def signin(self):
        r = self.session.get(url_index)
        soup = bs(r.content, "lxml")
        if not soup.find("a", {"onclick": "javascript:qiandao('qiandao')"}):
            print("无需重复签到")
            return
        form_data = {"action": "qiandao"}
        self.session.post(url_signin, data=form_data)
        r = self.session.get(url_index)
        soup = bs(r.content, "lxml")
        # print(soup.find("a", {"onclick":"javascript:qiandao('qiandao')"}))
        if not soup.find("a", {"onclick": "javascript:qiandao('qiandao')"}):
            print("签到成功")


if __name__ == '__main__':
    # hdu = HduLogin('username', 'password')
    hdu = HduLogin()
    hdu.login()
    hdu.signin()
