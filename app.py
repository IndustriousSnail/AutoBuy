from flask import Flask, Response, json, request

from shop.jd import JD
from utils import sqlite_utils

app = Flask(__name__)

jd = JD()


def resp_format(resp_data=None):
    resp = {
        "returnCode": 0,
        "returnMessage": "",
        "beans": resp_data
    }
    return Response(json.dumps(resp), content_type='application/json')


@app.route("/init", methods=['POST'])
def init():
    jd.init()
    return resp_format()


@app.route("/login_qr", methods=['POST'])
def login():
    jd.login_qr()
    jd.get_user_name()
    jd.save_cookies()
    return resp_format(jd.user_name)


@app.route("/get_logined_user", methods=['POST'])
def get_logined_user():
    return resp_format(sqlite_utils.get_logined_users())


@app.route("/set_logined_user", methods=['POST'])
def set_logined_user():
    username = request.form['username']
    cookies = sqlite_utils.get_cookies_by_username(username)
    jd.set_cookie(cookies)
    return resp_format(jd.check_login_result())


if __name__ == '__main__':
    app.run()
