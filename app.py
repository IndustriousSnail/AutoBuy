import os
import time

from flask import Flask, Response, json, request, make_response

from common.model import Model
from shop.jd import JD
from utils import sqlite_utils, wait_utils

app = Flask(__name__)

jd = JD()


def resp_format(resp_data=None, return_code=0, return_message=""):
    if isinstance(resp_data, Model):
        resp_data = resp_data.to_dict()

    resp = {
        "returnCode": return_code,
        "returnMessage": return_message,
        "beans": resp_data
    }
    return Response(json.dumps(resp), content_type='application/json')


@app.route("/auto_buy/init", methods=['POST'])
def init():
    jd.init()
    return resp_format()


@app.route("/auto_buy/get_qr_img", methods=['GET'])
def get_qr_img():
    image_data = open(os.path.join("./qr_imgs", 'qr.png'), "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response


@app.route("/auto_buy/login_qr", methods=['POST'])
def login():
    jd.login_qr()
    # jd.get_user_name()
    # jd.save_cookies()
    return resp_format()


@app.route("/auto_buy/finish_scan_qr", methods=['POST'])
def finish_scan_qr():
    if not wait_utils.until_url_contains(jd.driver, "//www.jd.com", retry_interval=0.01, timeout=3):
        # 扫码成功后，应该返回京东页面，如果3s内，没返回，报错
        return resp_format(None, 1, "登录失败，请重新登录")
    username = jd.get_user_name()
    jd.save_cookies()  # 把session信息保存下来，以便于以后使用
    return resp_format(username, return_message="您好，%s!" % username)


@app.route("/auto_buy/get_logined_user", methods=['POST'])
def get_logined_user():
    return resp_format(sqlite_utils.get_logined_users())


@app.route("/auto_buy/set_logined_user", methods=['POST'])
def set_logined_user():
    username = request.form['username']
    cookies = sqlite_utils.get_cookies_by_username(username)
    jd.set_cookie(cookies)
    return resp_format(jd.check_login_result())


@app.route("/auto_buy/get_goods_info", methods=['POST'])
def get_goods_info():
    goods_url = request.json.get("goodsUrl")
    return resp_format(jd.get_goods_info(goods_url))


@app.route("/auto_buy/get_logined_username", methods=['POST'])
def get_logined_username():
    if jd.check_login_result():
        # 已经登录
        username = jd.get_user_name()
        return resp_format(username, return_message="您好，%s!" % username)
    else:
        return resp_format(return_code=404)


if __name__ == '__main__':
    os.system("taskkill /im chrome.exe /f")
    os.system("taskkill /im chromedriver75.exe /f")
    time.sleep(2)
    jd.init()
    app.run()
