import redis
import json
import time
import sqlite3
from Edaq530 import Edaq530
from models.Task import Task
from EdaqDaemon import EdaqDaemon
import threading
import sys

def redisConnection():
    r = redis.StrictRedis(host='localhost', port=6379,db=0)
    return r

def listenRedis():
    listening = True
    r = redisConnection()
    p = r.pubsub()
    p.subscribe('edaq530')
    while listening:
        time.sleep(1)
        mStatusSubs = measurementStatusSubscriber(p,r)
""" 
@TODO EdaqDaemon feliratkozása event alapján
"""
def measurementStatusSubscriber(pubsub, redis):
    #print(threading.enumerate())
    getMessage = pubsub.get_message()
    if getMessage != None and getMessage.get('type') == 'message':
        data = json.loads(getMessage.get('data').decode('UTF-8'))
        if data.get('event') == 'schedule_task':
            taskData = data.get('data')
            task = Task.createTask(taskData.get('name'),
                                   taskData.get('first_channel'),
                                   taskData.get('first_equation'),
                                   taskData.get('second_channel'),
                                   taskData.get('second_equation'),
                                   taskData.get('third_channel'),
                                   taskData.get('third_equation'),
                                   taskData.get('delay'),
                                   taskData.get('end_date'))
            startScheduledMeasurment(task.id, redis, pubsub)
        if data.get('event') == 'ask_active_threads':
            redis.publish('edaq530', json.dumps({'event': 'active_threads', 'data': threading.active_count()}))


def statusChecker(pubsub):
    getMessage = pubsub.get_message()
    if getMessage != None and getMessage.get('type') == 'message':
        data = json.loads(getMessage.get('data').decode('UTF-8'))
        print(data.get('event'))
        if data.get('event') == 'mesurement_status' and data.get('data') == 1:
            return True
        elif data.get('event') == 'mesurement_status' and data.get('data') == 0:
            return False
        else:
            return None

def startScheduledMeasurment(task, redis, pubsub):
    edaqDaemon = EdaqDaemon(task, redis,pubsub)
    edaqDaemon.start()

def main():
    listenRedis()


if __name__ == '__main__':
    sql_create_tasks_table = """ CREATE TABLE IF NOT EXISTS tasks (
                                        id integer PRIMARY KEY,
                                        name varchar(255) NOT NULL,
                                        first_channel integer,
                                        first_equation varchar(255),
                                        second_channel integer,
                                        second_equation varchar(255),
                                        third_channel integer,
                                        third_equation varchar(255),
                                        delay integer,
                                        end_date datetime
                                    ); """

    sql_create_datas_table = """ CREATE TABLE IF NOT EXISTS data (
                                        id integer PRIMARY KEY,
                                        task_id integer NOT NULL,
                                        first_measurement varchar(255),
                                        second_measurement varchar(255),
                                        third_measurement varchar(255),
                                        created_at datetime,
                                        FOREIGN KEY (task_id) REFERENCES tasks (id)
                                    ); """
    conn = sqlite3.connect('edaq530.sql')
    with conn:
        cur = conn.cursor()
        #valt = cur.execute("SELECT end_date FROM tasks WHERE id=4")
        #print(datetime.datetime.strptime(valt.fetchone()[0], '%Y-%m-%dT%H:%M:%S%z'))
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks';")
        if not cur.fetchall():
            cur.execute(sql_create_tasks_table)
            cur.execute(sql_create_datas_table)

    main()