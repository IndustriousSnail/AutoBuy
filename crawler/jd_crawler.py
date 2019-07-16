import json
import re

import requests
from pyquery import PyQuery as pq

from common.model import Address, Goods
from log import log


def get_user_name(html_text):
    doc = pq(html_text)
    user_name = doc(".user_show>p>a")
    if user_name and len(user_name) > 0:
        log.info("用户：" + user_name[0].text)
        return user_name[0].text
    else:
        log.warning("获取用户名失败")


def check_login_result(html_text):
    """
    检查登录结果，如果上面包含请登录三个字，说明登录失效，需要重新登录
    :param html_text:
    :return:
    """
    doc = pq(html_text)
    if len(doc('.link-regist')) > 0:
        return False
    else:
        return True


def get_address(html_text):
    doc = pq(html_text)
    address_divs = doc(".item-lcol")
    address_list = []
    for address_item in address_divs.items():
        address = Address()
        for item in address_item(".item").items():
            label = item(".label").text()
            text = item(".fl").text()
            if '收货人' in label:
                address.name = text
            if '地址' in label:
                address.address = text
            if '手机' in label:
                address.phone = text
        log.debug("获取地址成功：%s" % str(address))
        address_list.append(address)
    return address_list


def get_goods_info(goods_url, html_text):
    goods = Goods()

    url = goods_url.strip()
    goods_id = re.search("\\d+(?=.htm)", url)
    if goods_id:
        goods.id = goods_id.group()  # 获取商品ID
        log.debug("商品ID: %s" % goods.id)
    else:
        log.error("获取商品ID失败，请输入正确商品地址，如“https://item.jd.com/29355959679.html”")
    doc = pq(html_text)
    goods_name = doc(".sku-name")

    if goods_name:
        goods.name = goods_name.text().strip()
        log.debug("商品名称: %s" % goods.name)
    else:
        log.error("获取商品%s名称失败" % goods.id)

    for item in doc(".p-price").items():
        price = item(".J-p-%s" % goods.id)
        if price:
            goods.price = price.text()
            break

    if goods.price is None:
        log.error("获取商品%s价格失败" % goods.id)

    in_stock = doc("#store-prompt>strong")
    if in_stock:
        goods.in_stock = in_stock.text()
    else:
        log.error("获取商品%s库存信息失败" % goods.id)

    delivery_place = doc(".ui-area-text")
    if delivery_place:
        goods.delivery_place = delivery_place.text()
    else:
        log.error("获取商品%s配送地址失败" % goods.id)

    one_click_buy = doc("#btn-onkeybuy")
    if one_click_buy:
        if "display:none" in one_click_buy.attr("style").replace(" ", ""):
            goods.one_click_buy = False
        else:
            goods.one_click_buy = True
    else:
        goods.one_click_buy = False

    return goods


def get_goods_info_from_cart(html_text):
    """从购物车页面获取商品详情"""
    doc = pq(html_text)
    item_length = len(doc(".item-form"))
    if item_length > 1:
        log.error("清空购物车失败，购物车存在两个以上商品")
        return
    elif item_length <= 0:
        log.error("加入购物车失败，购物车为空")
        return

    goods = Goods()
    goods.price = float(doc(".plus-switch strong").text().replace("¥", ""))
    goods.in_stock = doc(".quantity-txt")[0].text == "有货"
    goods.name = doc(".p-name")("a").text().strip()
    return goods


def get_goods_info_by_requests(goods_id):
    resp = requests.get("https://c0.3.cn/stock", {
        "skuId": goods_id,
        "cat": "123,456,789",
        "area": "1_2345_67890_1",
        "buyNum": "1",
        "extraParam": '{"originid":"1"}',
        "ch": "1",
        "fqsp": "0",
        "callback": "jQuery1454717"
    })
    goods_dict = json.loads(resp.text.replace("jQuery1454717(", "")[:-1])

    goods = Goods()
    if "有货" in goods_dict["stock"]["stockDesc"]:
        goods.in_stock = True
    else:
        goods.in_stock = False

    goods.price = float(goods_dict["stock"]["jdPrice"]["p"])
    return goods
