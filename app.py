from shop.jd import JD

if __name__ == '__main__':
    jd = JD()
    jd.init()  # 初始化
    jd.login_qr()  # 扫码登录
    jd.get_user_name()
    address = jd.get_address()  # 获取收货地址
    for address_item in address:
        print(str(address_item))
    print(jd.get_goods_info("https://item.jd.com/7629508.html"))
    print(jd.check_conditions_of_purchase(12000))
    jd.order()