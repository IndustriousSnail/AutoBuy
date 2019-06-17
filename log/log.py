import time


def debug(msg):
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("%s: %s" % (curr_time, msg))
