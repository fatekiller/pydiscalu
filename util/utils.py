# -*-coding:utf-8 -*-
import json

'''
必须判断类型然后确定用什么方法解析
'''


def parse_with_type_check(d):
    if isinstance(d,dict):
        return Dict2obj(d)
    if isinstance(d,list):
        return Dict2list(d)
    else:
        return d


class Dict2obj(object):
    def __init__(self, d):
        self.__d__=d;
        if isinstance(d, dict):
            for key in d:
                object.__setattr__(self, key, parse_with_type_check(d[key]))


class Dict2list(list):
    def __init__(self, d):
        self.__d__ = d;
        if isinstance(d, list):
            for l in d:
                self.append(parse_with_type_check(l))


def obj2json(obj):
    return json.dumps(obj, default=lambda o: o.__dict__)


def json2obj(json_str):
    o = parse_with_type_check(json.loads(json_str))
    return o

