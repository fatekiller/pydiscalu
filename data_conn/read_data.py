import mysql.connector as my_conn


def init_conn(user_name, password, database):
    conn = my_conn.connect(user=user_name, password=password, database=database)
    return conn


def insert_data():
    conn = init_conn("root", "cloudsea123", "pydistcalu")
    cursor = conn.cursor()
    for i in range(1, 1000):
        cursor.execute("insert into sale (sale_id, trade_sum, date) values (%s, %s, %s)", [i, i, "2016-01-01"])
    for i in range(1000, 2001):
        cursor.execute("insert into sale (sale_id, trade_sum, date) values (%s, %s, %s)", [i, i, "2017-07-01"])
    conn.commit()
    conn.close()
# insert_data()
