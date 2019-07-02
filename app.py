import os

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


@app.route("/auto_buy/check_finish_scan_qr", methods=['POST'])
def check_finish_scan_qr():
    """检测是否完成扫码登录"""
    if not wait_utils.until_url_contains(jd.driver, "//www.jd.com", retry_interval=0.01, timeout=0.5):
        # 还没扫码
        return resp_format(False)
    else:
        # 扫过码了
        return finish_scan_qr()


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


@app.route("/auto_buy/start_rush_buy", methods=['POST'])
def start_rush_buy():
    """开始抢购"""
    price = request.json.get("price")
    in_stock = request.json.get("inStock")
    buy_time = request.json.get("buyTime")
    if price is None and in_stock is False and buy_time is None:
        return resp_format(return_code=400, return_message="至少选择一项抢购条件")

    result = jd.start_rush_buy(price, in_stock, buy_time)
    if result:
        return resp_format()
    else:
        return resp_format(return_code=403, return_message="抢购已经开始")


@app.route("/auto_buy/cancel_rush_buy", methods=['POST'])
def cancel_rush_buy():
    jd.jd_thread.stop()
    jd.jd_thread = None
    return resp_format()


@app.route("/auto_buy/check_buying", methods=['POST'])
def check_buying():
    """检测是否正在抢购"""
    return resp_format(not jd.jd_thread is None)


@app.route("/auto_buy/check_order_success", methods=['POST'])
def check_order_success():
    """检测是否下单成功"""
    return resp_format(jd.jd_thread.success)


if __name__ == '__main__':
    os.system("taskkill /im chrome.exe /f")
    os.system("taskkill /im chromedriver75.exe /f")
    jd.init()
    app.run()
