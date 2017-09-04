import mysql.connector as my_conn
import re
import Queue

conns = Queue.Queue()
CONN_SiZE = 10

'''
ds datasource object
only support mysql now
'''


def init_conn(ds):
    if ds.ds_type == 'mysql':
        user = ''
        password = ''
        db = ''
        for prop in ds.props:
            if prop.name == 'username':
                user = prop.value
            if prop.name == 'password':
                password = prop.value
            if prop.name == 'url':
                db = re.search('database=(.*)&?', prop.value).group(1)
        for i in range(0, CONN_SiZE):
            conns.put(my_conn.connect(user=user, password=password, database=db))


def insert_data():
    conn = conns.get()
    cursor = conn.cursor()
    for i in range(1, 1000):
        cursor.execute("insert into sale (sale_id, trade_sum, date) values (%s, %s, %s)", [i, i, "2016-01-01"])
    for i in range(1000, 2001):
        cursor.execute("insert into sale (sale_id, trade_sum, date) values (%s, %s, %s)", [i, i, "2017-07-01"])
    conn.commit()
    conns.put(conn)


def get_count(sql=""):
    conn = conns.get()
    m = re.search('from\s+(\w+)\s+(where.*)', sql)
    table = m.group(1)
    where = m.group(2)
    cursor = conn.cursor()
    cursor.execute("select count(*) from %s %s" % (table, where))
    return cursor.fetchone()[0]
