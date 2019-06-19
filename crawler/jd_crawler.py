import re

import requests
from pyquery import PyQuery as pq

from log import log


def get_goods_name_and_id(url):
    """
    根据商品的url，获取商品的名称和id
    :param url:
    :return:
    """
    url = url.strip()
    goods_id = re.search("\d+(?=.htm)", url)
    if goods_id:
        goods_id = goods_id.group()  # 获取商品ID
        log.debug("商品ID: %s" % goods_id)
    else:
        log.error("获取商品ID失败，请输入正确商品地址，如“https://item.jd.com/29355959679.html”")
    resp = requests.get(url)
    html_text = resp.text
    doc = pq(html_text)
    goods_name = doc(".sku-name")

    if goods_name:
        goods_name = goods_name.text().strip()
        log.debug("商品名称: %s" % goods_name)
    else:
        log.error("获取商品名称失败")
    return goods_id, goods_name
