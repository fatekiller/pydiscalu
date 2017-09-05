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
from util.utils import json2obj, obj2json
from model.Job import *
from xmlParse.parser import *


def get_msg(d):
    return Msg(int(d["msg_type"]), d["content"], int(d["status"]))


class DictObj(object):
    def __init__(self,map):
        self.map = map

    def __setattr__(self, name, value):
        if name == 'map':
            object.__setattr__(self, name, value)
            return;
        print 'set attr called ',name,value
        self.map[name] = value

    def __getattr__(self,name):
        v = self.map[name]
        if isinstance(v,(dict)):
            return DictObj(v)
        if isinstance(v, (list)):
            r = []
            for i in v:
                r.append(DictObj(i))
            return r
        else:
            return self.map[name];

    def __getitem__(self,name):
        return self.map[name]

if __name__ == '__main__':
    msg = Msg(Msg.MSG_HELLO, "hello", Msg.STATUS_SUCCESS)
    s = obj2json(msg)
    mm = json2obj(s, get_msg)
    jobs = parse_job('../conf/jobs.xml')
    jobs_json_str=obj2json(jobs)
    print jobs_json_str
    jobs_copy = json2obj(jobs_json_str)
    print jobs_copy
