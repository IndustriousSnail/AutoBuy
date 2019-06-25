import sqlite3

conn = sqlite3.connect("auto_buy.db")

cursor = conn.cursor()

cursor.execute("""create table if not exists cookies(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain varchar(128) not null,
                expiry varchar(64),
                name varchar(256) not null,
                path varchar(256),
                secure varchar(256),
                value varchar(2048) not null,
                httpOnly varchar(10) not null
);""")

cursor.close()

conn.commit()


def insert_cookies(cookies):
    c = conn.cursor()
    for item in cookies:
        sql = "insert into cookies(domain,expiry,httpOnly,name,path,secure,value) values('%s', '%s', '%s', '%s', " \
              "'%s', '%s', '%s')" % (
            item.domain,
            item.expiry,
            item.httpOnly,
            item.name,
            item.path,
            item.secure,
            item.value
        )
        c.execute(sql)

    cursor.close()
    conn.commit()




