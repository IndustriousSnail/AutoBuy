import time


def info(msg):
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_msg = "%s: %s" % (curr_time, msg)
    print(log_msg)
    return log_msg + "\n"


def debug(msg):
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_msg = "%s: %s" % (curr_time, msg)
    print(log_msg)
    return log_msg + "\n"

def warning(msg):
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_msg = "%s: %s" % (curr_time, msg)
    print(log_msg)
    return log_msg + "\n"

def error(msg):
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_msg = "%s: %s" % (curr_time, msg)
    print(log_msg)
    return log_msg + "\n"
