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


class Cookie(object):

    domain = None
    # int
    expiry = None
    # bool
    httpOnly = None
    name = None
    path = None
    # False
    secure = None
    value = None

    def __str__(self):
        return "domain=%s, expiry=%s, httpOnly=%s, name=%s, path=%s, secure=%s, value=%s" % (self.domain,
                                                                                             self.expiry,
                                                                                             self.httpOnly,
                                                                                             self.name,
                                                                                             self.path,
                                                                                             self.secure,
                                                                                             self.value)

    def to_dict(self):
        result = {}
        if self.domain:
            result['domain'] = self.domain
        if self.expiry:
            result['expiry'] = int(self.expiry)
        if self.httpOnly:
            result['httpOnly'] = self.httpOnly
        if self.name:
            result['name'] = self.name
        if self.path:
            result['path'] = self.path
        if self.secure:
            result['secure'] = self.secure
        if self.value:
            result['value'] = self.value

        return result

    @staticmethod
    def from_dict(cookies):
        cookies_list = []
        for cookie_dict in cookies:
            cookie = Cookie()
            if 'domain' in cookie_dict:
                cookie.domain = cookie_dict['domain']
            if 'expiry' in cookie_dict:
                cookie.expiry = cookie_dict['expiry']
            if 'httpOnly' in cookie_dict:
                cookie.httpOnly = cookie_dict['httpOnly']
            if 'name' in cookie_dict:
                cookie.name = cookie_dict['name']
            if 'path' in cookie_dict:
                cookie.path = cookie_dict['path']
            if 'secure' in cookie_dict:
                cookie.secure = cookie_dict['secure']
            if 'value' in cookie_dict:
                cookie.value = cookie_dict['value']

            cookies_list.append(cookie)

        return cookies_list













