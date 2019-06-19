import time


def info(msg):
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("%s: %s" % (curr_time, msg))


def debug(msg):
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("%s: %s" % (curr_time, msg))


def error(msg):
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("%s: %s" % (curr_time, msg))
