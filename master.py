# -*- coding:utf-8 -*-
from socket_communicate.socket_comm import send_msg, init_s_conn, Msg, Conn
from xmlParse.parser import parse_job, parse_worker
from data_conn.read_data import get_count, init_conn
import threading as tr
import random
import math

conns = []
workers = []
jobs = []
# 连接校验完成的数量
check_sum = 0
lock = tr.Lock()


def dispatch_job():
    for job in jobs:
        job.job_id = random.randint(0, 1000)
        init_conn(job.ds)
        count = get_count(job.sql)
        # 计算每个worker应该负责的记录条数
        amount = int(math.ceil(float(count)/len(workers)))
        offset = 0
        for _conn in conns:
            count -= amount
            if count >= 0:
                size = amount
            else:
                size = amount + count
            # 设置当前worker需要执行的job涉及的记录条数和起始记录id
            job.size = size
            job.offset = offset
            offset += size
            new_conn = Conn(reply_gen(job), _conn.conn_socket)
            print "send job %s,waiting for confirm message" % job.sql
            send_msg(new_conn, Msg(Msg.MSG_JOB, job).get_json_msg())


def on_connect_confirm(s, msg):
    global check_sum
    lock.acquire()
    check_sum += 1
    lock.release()
    msg = Msg.get_msg(msg)

    if msg.status == Msg.STATUS_SUCCESS:
        if msg.msg_type == Msg.MSG_CONNECTED:
            conns.append(Conn(conn_socket=s))
            if check_sum == len(workers):
                dispatch_job()


def reply_gen(job):

    def on_reply(s, msg):
        msg = Msg.get_msg(msg)
        if msg.status == Msg.STATUS_SUCCESS:
            if msg.msg_type == Msg.MSG_JOB_REPLY:
                print msg.content
            if msg.msg_type == Msg.MSG_RESULT:
                print msg.content
    return on_reply


# 向worker发送连接确认消息
def init_socket_conn(pre_conn_worker):
    init_s_conn(Msg(Msg.MSG_HELLO, "hello").get_json_msg(), pre_conn_worker, on_connect_confirm)


if __name__ == "__main__":
    # 解析workers
    workers = parse_worker("conf/workers.xml")
    # 解析jobs
    jobs = parse_job("conf/jobs.xml")
    # worker 连接
    for worker in workers:
        init_socket_conn(worker)
