class Model(object):

    def to_dict(self):
        return {}


class Address(Model):
    name = None
    address = None
    phone = None

    def __str__(self):
        return '%s %s %s' % (self.name, self.address, self.phone)


class Goods(Model):
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
        return "id=%s, name=%s, price=%s, in_stock=%s, deliveryPlace=%s, oneClickBuy=%s" % (
            self.id, self.name, self.price,
            self.in_stock,
            self.delivery_place, self.one_click_buy)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "in_stock": self.in_stock,
            "delivery_place": self.delivery_place,
            "one_click_buy": self.one_click_buy,
        }


class Cookie(Model):
    username = None
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
        return "username=%s, domain=%s, expiry=%s, httpOnly=%s, name=%s, path=%s, secure=%s, value=%s" % (self.username,
                                                                                                          self.domain,
                                                                                                          self.expiry,
                                                                                                          self.httpOnly,
                                                                                                          self.name,
                                                                                                          self.path,
                                                                                                          self.secure,
                                                                                                          self.value)

    def to_dict(self):
        result = {}
        if self.username:
            result['username'] = self.username
        if self.domain:
            result['domain'] = self.domain
        if self.expiry and self.expiry != 'None':
            result['expiry'] = int(float(self.expiry))
        if self.httpOnly:
            result['httpOnly'] = False if self.httpOnly == 'False' else True
        if self.name:
            result['name'] = self.name
        if self.path:
            result['path'] = self.path
        if self.secure:
            result['secure'] = False if self.secure == 'False' else True
        if self.value:
            result['value'] = self.value

        return result

    @staticmethod
    def from_dict(username, cookies):
        cookies_list = []
        for cookie_dict in cookies:
            cookie = Cookie()
            cookie.username = username
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
