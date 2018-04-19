#!/usr/bin/env python3
import DBCommands
import sqlite3
from sqlite3 import Error

class EdaqDB(object):

    def __init__(self):
        self.conn = sqlite3.connect('edaq530.sql')
        self.create_tables()

    def create_tables(self):
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(DBCommands.sql_create_tasks_table)
            cur.execute(DBCommands.sql_create_datas_table)

    def create_task(self, name, begin_date, end_date=None):
        task = (name, begin_date, end_date)
        cur = self.conn.cursor()
        cur.execute(DBCommands.sql_instert_task, task)
        return cur.lastrowid

    def insert_measurment(self, task_id, measurment):
        measurment = (task_id, measurment, 'now')
        cur = self.conn.cursor()
        cur.execute(DBCommands.sql_instert_data, measurment)
        return cur.lastrowid