# -*- coding:utf-8 -*-
from socket_communicate.socket_comm import init_socket, Msg
from xmlParse.parser import parse_job, parse_worker
from data_conn.read_data import get_count, init_conn
import threading as tr

import math


def reply_gen(exe_job):
    def on_reply(s, msg):
        print 'master receive message :%s' % msg
        msg = Msg.get_msg(msg)
        if msg.status == Msg.STATUS_SUCCESS:
            if msg.msg_type == Msg.MSG_CONNECTED:
                s.send(Msg(Msg.MSG_JOB, exe_job).get_json_msg())
            if msg.msg_type == Msg.MSG_RESULT:
                print msg.content
                # s.send(Msg(Msg.MSG_JOB, exe_job).get_json_msg())
    return on_reply


# 闭包函数，每个worker开启一个新的thread
def init_socket_conn(ip, port, exec_job):
    def job_thread():
        init_socket(Msg(Msg.MSG_HELLO, "hello").get_json_msg(), ip, port, reply_gen(exec_job))
    return job_thread

if __name__ == "__main__":
    # 解析workers
    workers = parse_worker("conf/workers.xml")
    # 解析jobs
    jobs = parse_job("conf/jobs.xml")
    for job in jobs:
        init_conn(job.ds)
        count = get_count(job.sql)
        # 计算每个worker应该负责的记录条数
        amount = math.ceil(float(count)/len(workers))
        offset = 0
        for worker in workers:
            count -= amount
            if count >= 0:
                size = amount
            else:
                size = amount + count
            # 设置当前worker需要执行的job涉及的记录条数和起始记录id
            job.size = size
            job.offset = offset
            offset += size
            tr.Thread(target=init_socket_conn(worker.address, worker.port, job), name=worker.address).start()
