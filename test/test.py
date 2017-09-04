# -*- coding:utf-8 -*-
# 引用在初始化了新的对象的时候就设置了新的地址
# from model import Job
# a = []
# b = Job.Job()
# b.set_sql("bbb")
# a.append(b)
# print a[0].sql
# b = Job.Job()
# print a[0].sql
# print b.sql

# test parse
# from xmlParse import parser
#
# f = open("../jobs.xml")
# s = f.readline()
# print s
# f.close();
# a = parser.parse_worker("../workers.xml")
# print a

# from data_conn.read_data import get_count,init_conn
# init_conn()
# print get_count()

# from util.utils import json2obj, obj2json
#
#
# class TestClass(object):
#     def __init__(self, a=None):
#         self.a = a
#
#
# print json2obj(obj2json(TestClass()))
from socket_communicate.socket_comm import Msg
from util.utils import json2obj,obj2json


def get_msg(d):
    return Msg(int(d["msg_type"]), d["content"], int(d["status"]))


msg = Msg(Msg.MSG_HELLO, "hello", Msg.STATUS_SUCCESS)
s = obj2json(msg)
mm = json2obj(s, get_msg)
