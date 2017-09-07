import mysql.connector as my_conn
import re
import Queue

conns = Queue.Queue()
CONN_SiZE = 10

'''
ds datasource object
only support mysql now
'''


class Table(object):
    def __init__(self, sql):
        m = re.search('select\s+(.*)\s+from\s+(\w+)\s+where(.*)', sql)
        self.select_target = m.group(1)
        self.table_name = m.group(2)
        self.where_rules = m.group(3)


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


def execute_with_result_and_count(sql, offset, count):
    conn = conns.get()
    cursor = conn.cursor()
    table = Table(sql)
    _view = "(select * from %s WHERE %s limit %s,%s) as %s" % \
            (table.table_name, table.where_rules, str(offset), str(count), table.table_name)
    sql = "select %s from  %s" % (table.select_target, _view)
    print sql
    cursor.execute(sql)
    return cursor.fetchone()


def get_count(sql=""):
    conn = conns.get()
    table = Table(sql)
    cursor = conn.cursor()
    cursor.execute("select count(*) from %s where %s" % (table.table_name, table.where_rules))
    conns.put(conn)
    return cursor.fetchone()[0]
