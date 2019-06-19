import time

from common.gui import gui_log

@gui_log
def info(msg):
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_msg = "%s: %s" % (curr_time, msg)
    print(log_msg)
    return log_msg + "\n"


@gui_log
def debug(msg):
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_msg = "%s: %s" % (curr_time, msg)
    print(log_msg)
    return log_msg + "\n"


@gui_log
def error(msg):
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_msg = "%s: %s" % (curr_time, msg)
    print(log_msg)
    return log_msg + "\n"
