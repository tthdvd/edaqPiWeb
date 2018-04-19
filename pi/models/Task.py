#!/usr/bin/env python3
from models.Model import Model
from models.Data import Data
import sqlite3
import datetime
import pytz


class Task(Model):

    def __init__(self, id):
        super(Task, self).__init__()
        self.id = id
        with self.conn:
            cur = self.conn.cursor()
            getName = cur.execute("SELECT name FROM tasks WHERE id=?", (self.id,))
            self.name = getName.fetchone()[0]

            getEndDate = cur.execute("SELECT datetime(end_date) FROM tasks WHERE id=?", (self.id,))
            self.end_date = getEndDate.fetchone()[0]

            getThirdEquation = cur.execute("SELECT first_equation FROM tasks WHERE id=?", (self.id,))
            self.first_equation = getThirdEquation.fetchone()[0]

            getSecondEquation = cur.execute("SELECT second_equation FROM tasks WHERE id=?", (self.id,))
            self.second_equation = getSecondEquation.fetchone()[0]

            getThirdEquation = cur.execute("SELECT third_equation FROM tasks WHERE id=?", (self.id,))
            self.third_equation = getThirdEquation.fetchone()[0]

            getFirstChannel = cur.execute("SELECT first_channel FROM tasks WHERE id=?", (self.id,))
            self.first_channel = getFirstChannel.fetchone()[0]

            getSecondChannel = cur.execute("SELECT second_channel FROM tasks WHERE id=?", (self.id,))
            self.second_channel = getSecondChannel.fetchone()[0]

            getThirdChannel = cur.execute("SELECT third_channel FROM tasks WHERE id=?", (self.id,))
            self.third_channel = getThirdChannel.fetchone()[0]

            getDelay = cur.execute("SELECT delay FROM tasks WHERE id=?", (self.id,))
            self.delay = getDelay.fetchone()[0]

    def insertMeasurements(self, measurements):
        tz = pytz.timezone('Europe/Budapest')
        with self.conn:
            sql = """INSERT INTO data(
            task_id,
            first_measurement,
            second_measurement,
            third_measurement,
            created_at) VALUES(?,?,?,?,?) """
            values = (self.id,
                      measurements[0],
                      measurements[1],
                      measurements[2],
                      datetime.datetime.now())
            cur = self.conn.cursor()
            cur.execute(sql, values)

        return Data(cur.lastrowid)

    @staticmethod
    def createTask(name,
                   first_channel,
                   first_equation,
                   second_channel,
                   second_equation,
                   third_channel,
                   third_equation,
                   delay,
                   end_date):
        conn = sqlite3.connect('edaq530.sql')
        with conn:
            sql_instert_task = """
            INSERT INTO tasks(
                name,
                first_equation,
                second_equation,
                third_equation,
                first_channel,
                second_channel,
                third_channel,
                delay,
                end_date) VALUES(?,?,?,?,?,?,?,?,?) """
            values = (name,
                      first_equation,
                      second_equation,
                      third_equation,
                      first_channel,
                      second_channel,
                      third_channel,
                      delay,
                      end_date)
            cur = conn.cursor()
            cur.execute(sql_instert_task, values)

        return Task(cur.lastrowid)
