from socket_communicate.socket_comm import worker_init, Msg
from model.Job import Job
from util.utils import json2obj
import Queue
import threading as tr
import random

master = None
jobs = Queue.Queue()
jobs_lock = False


def on_receive(s, msg):
    if Msg.get_msg(msg).msg_type == Msg.MSG_HELLO:
        s.send(Msg(Msg.MSG_CONNECTED, 'connected').get_json_msg())
    if Msg.get_msg(msg).msg_type == Msg.MSG_JOB:
        try:
            jobs.put(json2obj(msg.content,hook=Job.json_job_hook))
            tr.Thread(target=do_job, name=str(random.randint(0, 1000))).start()
        except Exception as e:
            print e
        s.send(Msg(Msg.MSG_JOB_REPLY, 'job received').get_json_msg())
    print "slave receive msg: %s" % msg


def do_job():
    job = jobs.get()
    print 'executing task %s, offset is %s count is %s' % (job.sql, job.offset, job.size)
    master.send(Msg(Msg.MSG_RESULT, 'job finished').get_json_msg())


def on_conn(s, address):
    global master
    print "server connected %s" % address[0]
    master = s


if __name__ == '__main__':
    worker_init(on_receive, "127.0.0.1", 9999, on_conn)
