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
from xmlParse import parser

f = open("../jobs.xml")
s = f.readline()
print s
f.close();
a = parser.parse_worker("../workers.xml")
print a
