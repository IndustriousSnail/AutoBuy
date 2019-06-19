import uuid
from urllib.request import urlretrieve

from PIL import Image


def download_qr_img(img_url):
    """
    下载二维码图片
    :param img_url: 二维码地址
    :return: 图片的名称
    """
    img_filename = str(uuid.uuid1()).replace('-', '') + '.png'
    result = urlretrieve(img_url, './qr_imgs/%s' % img_filename)
    if result:
        return img_filename


def open_qr_img(img_filename):
    img = Image.open("./qr_imgs/%s" % img_filename)
    img.show()
