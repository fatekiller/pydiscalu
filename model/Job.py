# -*-coding:utf-8 -*-
class Job(object):
    def __init__(self, ds=None, sql=None, job_type=None):
        self.ds = ds
        self.sql = sql
        self.job_type = job_type

    def set_ds(self, ds):
        self.ds = ds

    def set_sql(self, sql):
        self.sql = sql

    def set_type(self, job_type):
        self.job_type = job_type

    @staticmethod
    def json_job_hook(d):
        # todo 编写hook函数
        return Job(d[0])


class JobDataSource(object):
    def __init__(self, ds_type=None, props=None):
        self.ds_type = ds_type
        self.props = props

    def set_type(self, ds_type):
        self.ds_type = ds_type

    def set_props(self, props):
        self.props = props


class Prop(object):
    def __init__(self, name=None, prop_type=None, value=None):
        self.name = name
        self.prop_type = prop_type
        self.value = value

    def set_type(self, prop_type):
        self.prop_type = prop_type

    def set_name(self, name):
        self.name = name

    def set_value(self, value):
        self.value = value


class Result(object):
    def __init__(self, msg, value):
        self.msg = msg
        self.value = value

    def __str__(self):
        return "msg: %s, result: %s" % (self.msg, self.value)
