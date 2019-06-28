import sqlite3

from common.model import Cookie

db_name = "auto_buy.db"


def init():
    conn = sqlite3.connect(db_name)

    cursor = conn.cursor()

    cursor.execute("""create table if not exists cookies(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username varchar(128) not null,
                    domain varchar(128) not null,
                    expiry varchar(64),
                    name varchar(256) not null,
                    path varchar(256),
                    secure varchar(256),
                    value varchar(2048) not null,
                    http_only varchar(10) not null,
                    create_time timestamp not null default (datetime('now','localtime'))
    );""")

    cursor.close()

    conn.commit()
    conn.close()


init()


def delete_cookies_by_username(username):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    sql = "delete from cookies where username='%s'" % username
    c.execute(sql)

    c.close()
    conn.commit()
    conn.close()


def insert_cookies(cookies):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    for item in cookies:
        sql = "insert into cookies(username,domain,expiry,http_only,name,path,secure,value) values('%s', '%s', '%s', " \
              "'%s', '%s', '%s', '%s', '%s')" % (item.username,
                                                 item.domain,
                                                 item.expiry,
                                                 item.httpOnly,
                                                 item.name,
                                                 item.path,
                                                 item.secure,
                                                 item.value
                                                 )
        c.execute(sql)

    c.close()
    conn.commit()
    conn.close()


def get_logined_users():
    logined_users = []
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    cursor = c.execute("select distinct username from cookies order by create_time desc")
    for row in cursor:
        logined_users.append(row[0])
    c.close()
    conn.commit()
    conn.close()
    return logined_users


def get_cookies_by_username(username):
    cookies = []

    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    cursor = c.execute("select username,domain,expiry,http_only,name,path,secure,value from cookies where username='%s'" % username)
    for row in cursor:
        cookie = Cookie()
        cookie.username = row[0]
        cookie.domain = row[1]
        cookie.expiry = row[2]
        cookie.httpOnly = row[3]
        cookie.name = row[4]
        cookie.path = row[5]
        cookie.secure = row[6]
        cookie.value = row[7]
        cookies.append(cookie)
    c.close()
    conn.commit()
    conn.close()
    return cookies
