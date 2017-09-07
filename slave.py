from socket_communicate.socket_comm import worker_init, Msg
from model.Job import Result
from util.utils import json2obj
from data_conn.read_data import execute_with_result_and_count, init_conn
import Queue
import threading as tr
import random
import time

master = None
jobs = Queue.Queue()
jobs_lock = False
is_socket_alive = True

slave_ip = "127.0.0.1"
slave_port = 9999


def on_receive(s, msg):
    msg = Msg.get_msg(msg)
    print 'msg is %s' % msg
    if msg.msg_type == Msg.MSG_HELLO:
        s.send(Msg(Msg.MSG_CONNECTED, 'connected').get_json_msg())
    if msg.msg_type == Msg.MSG_JOB:
        try:
            jobs.put(msg.content)
            print "slave received job: %s" % msg.content.sql
            master.send(Msg(Msg.MSG_RESULT, "slave %s received job: %s" % (slave_ip, msg.content.sql)).get_json_msg())
            tr.Thread(target=do_job, name=str(random.randint(0, 1000))).start()
        except Exception as e:
            print e


def do_job():
    job = jobs.get()
    print 'slave executing task %s, offset is %s count is %s' % (job.sql, job.offset, job.size)
    time.sleep(2)
    init_conn(job.ds)
    result = execute_with_result_and_count(job.sql, job.offset, job.size)
    print 'slave finished job %s' % job.sql
    master.send(Msg(Msg.MSG_RESULT, Result('slave %s finished job %s' % (slave_ip, job.sql), result)).get_json_msg())


def on_conn(s, address):
    global master
    print "server connected %s" % address[0]
    master = s


def is_alive():
    return is_socket_alive

if __name__ == '__main__':
    worker_init(on_receive, slave_ip, slave_port, on_conn, is_alive=is_alive)
