import time


def until_url_contains(driver, pattern, retry_interval=0.5, timeout=180):
    """
    当url包含某个值时，等待结束
    :param driver: webdriver
    :param pattern: 包含的值
    :param retry_interval: 重新检测的间隔事件
    :param timeout: 超时时间
    """
    duration = 0
    while True:
        if pattern in driver.current_url:
            return True
        time.sleep(retry_interval)
        duration += retry_interval  # 记录时长
        if duration >= timeout:
            # 如果超时，结束
            return False


def open_page(driver, url):
    if url in driver.current_url:
        return True

    driver.get(url)
    until_url_contains(driver, url, retry_interval=0.01, timeout=10)

