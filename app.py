import time

from common.model import Cookie
from shop.jd import JD

if __name__ == '__main__':
    jd = JD()
    jd.init()  # 初始化
    # jd.login_qr()  # 扫码登录
    # jd.get_user_name()
    # jd.get_cookies()
    # address = jd.get_address()  # 获取收货地址
    # for address_item in address:
    #     print(str(address_item))
    # print(jd.get_goods_info("https://item.jd.com/7629508.html"))
    # print(jd.check_conditions_of_purchase(12000))
    # jd.order()

    # cookies = [{'domain': 'jd.com', 'expiry': 1561447733, 'httpOnly': False, 'name': '__jdb', 'path': '/', 'secure': False, 'value': '122270672.4.15614459076381833832199|1.1561445908'}, {'domain': 'jd.com', 'expiry': 1564037933.658375, 'httpOnly': False, 'name': '_tp', 'path': '/', 'secure': False, 'value': 'PpnKqjTU2RdbUiHmvPsMRnt1QQMV7vlXmtjEfobacvAviQL7TBlGxgPuBD4nJwh1'}, {'domain': 'jd.com', 'httpOnly': True, 'name': 'thor', 'path': '/', 'secure': False, 'value': '7D8BD431ABFC2BC0F51DF4FC5E1B0AB466FD98BEAB43383E3CF68032156D533E5BF927ABD14C1F99F95C74AC5099E540B33F793F242FE8016AA857428795F8EBA6615877DAFDE8558F29FB2345F96BA3F6D5BF7E941D3DA937E8B65C7796032CC6E864BAECD5BF6F7A566EA9B18B5FA37CBB96EE2700E05D6498CA5E984959B794145EAC6D7F50AF2436E7A44653AB4A'}, {'domain': 'jd.com', 'expiry': 1564037933.658428, 'httpOnly': True, 'name': '_pst', 'path': '/', 'secure': False, 'value': '%E5%94%B1%E8%B7%B3Rap_%E7%AF%AE%E7%90%83'}, {'domain': 'jd.com', 'expiry': 1564037933.658311, 'httpOnly': True, 'name': 'unick', 'path': '/', 'secure': False, 'value': '%E5%94%B1%E8%B7%B3Rap_%E7%AF%AE%E7%90%83iVT'}, {'domain': 'jd.com', 'expiry': 1719125933.658163, 'httpOnly': False, 'name': 'TrackID', 'path': '/', 'secure': False, 'value': '12Cy9kj_LdXBmEMZvPfJEvgfzoqv8DZ9QuEwcHGVBQZzSMWrUcVZrfaDaD5puXiMh-oARPpCxKKsW41oRHPEuPaLWDLNICjYFwRIAZU_u3E4'}, {'domain': 'jd.com', 'expiry': 1564037933.658272, 'httpOnly': False, 'name': 'pin', 'path': '/', 'secure': False, 'value': '%E5%94%B1%E8%B7%B3Rap_%E7%AF%AE%E7%90%83'}, {'domain': 'jd.com', 'expiry': 1924905600, 'httpOnly': False, 'name': '3AB9D23F7A4B3C9B', 'path': '/', 'secure': False, 'value': 'YGF4MAGCJNZIL5SVT7W6VMSTS6H5AM7IXJBAECMGV3YSKCAXKCEVLOGNB5C2BPYV6L6WUUPMUX4RIXR5HSGDGCNNNM'}, {'domain': 'jd.com', 'httpOnly': False, 'name': 'wlfstk_smdl', 'path': '/', 'secure': False, 'value': 'lvdsh2b78z4beaj881mii6us7c5jk035'}, {'domain': 'jd.com', 'expiry': 2425445935, 'httpOnly': False, 'name': 'shshshfpb', 'path': '/', 'secure': False, 'value': 'a%2BKp59p5rZ7JXVbhRfDnlkA%3D%3D'}, {'domain': 'jd.com', 'expiry': 2425445935, 'httpOnly': False, 'name': 'shshshfp', 'path': '/', 'secure': False, 'value': 'e225328cc30f91f0b2673706164af556'}, {'domain': 'jd.com', 'expiry': 1562309909.171762, 'httpOnly': False, 'name': 'PCSYCityID', 'path': '/', 'secure': False, 'value': '412'}, {'domain': 'jd.com', 'expiry': 1592981933.658239, 'httpOnly': False, 'name': 'pinId', 'path': '/', 'secure': False, 'value': '7INv0Pxt1u8zoRi9hndgQbV9-x-f3wj7'}, {'domain': 'jd.com', 'expiry': 1562309907, 'httpOnly': False, 'name': 'ipLoc-djd', 'path': '/', 'secure': False, 'value': '7-412-3548'}, {'domain': 'jd.com', 'httpOnly': False, 'name': 'ceshi3.com', 'path': '/', 'secure': False, 'value': '000'}, {'domain': 'jd.com', 'expiry': 2425445908, 'httpOnly': False, 'name': 'shshshfpa', 'path': '/', 'secure': False, 'value': '6085a108-cac3-79e1-f2c8-c331bba012d8-1561445908'}, {'domain': 'jd.com', 'expiry': 1562741907, 'httpOnly': False, 'name': '__jdv', 'path': '/', 'secure': False, 'value': '122270672|direct|-|none|-|1561445907639'}, {'domain': 'jd.com', 'expiry': 1576997935.115395, 'httpOnly': False, 'name': '__jdu', 'path': '/', 'secure': False, 'value': '15614459076381833832199'}, {'domain': 'jd.com', 'expiry': 1576997933, 'httpOnly': False, 'name': '__jda', 'path': '/', 'secure': False, 'value': '122270672.15614459076381833832199.1561445908.1561445908.1561445908.1'}, {'domain': 'jd.com', 'expiry': 1562309907, 'httpOnly': False, 'name': 'areaId', 'path': '/', 'secure': False, 'value': '7'}, {'domain': 'jd.com', 'httpOnly': False, 'name': '__jdc', 'path': '/', 'secure': False, 'value': '122270672'}, {'domain': 'jd.com', 'expiry': 1561447735, 'httpOnly': False, 'name': 'shshshsID', 'path': '/', 'secure': False, 'value': 'afa161469d11e9d0928a3996cda745c9_2_1561445935069'}, {'domain': 'www.jd.com', 'expiry': 1592981933, 'httpOnly': False, 'name': 'o2Control', 'path': '/', 'secure': False, 'value': 'webp'}]
    # cookie_list = []
    # for item in cookies:
    #     cookie = Cookie()
    #     cookie.domain = item['domain'] if 'domain' in item else None
    #     cookie.expiry = item['expiry'] if 'expiry' in item else None
    #     cookie.httpOnly = item['httpOnly'] if 'httpOnly' in item else None
    #     cookie.name = item['name'] if 'name' in item else None
    #     cookie.path = item['path'] if 'path' in item else None
    #     cookie.secure = item['secure'] if 'secure' in item else None
    #     cookie.value = item['value'] if 'value' in item else None
    #     cookie_list.append(cookie)
    #
    # jd.set_cookie(cookie_list)

    jd.get_cookies()

    time.sleep(180)
