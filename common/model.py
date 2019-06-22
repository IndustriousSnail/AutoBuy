class Address(object):
    name = None
    address = None
    phone = None

    def __str__(self):
        return '%s %s %s' % (self.name, self.address, self.phone)


class Goods(object):
    # 商品ID
    id = None
    name = None
    price = None
    in_stock = None
    # 配送地点
    delivery_place = None
    # 是否有一键购买按钮
    one_click_buy = False

    def __str__(self):
        return "id=%s, name=%s, price=%s, in_stock=%s, deliveryPlace=%s, oneClickBuy=%s" % (self.id, self.name, self.price,
                                                                               self.in_stock,
                                                                               self.delivery_place, self.one_click_buy)
