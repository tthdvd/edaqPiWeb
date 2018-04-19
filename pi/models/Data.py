#!/usr/bin/env python3
from models.Model import Model


class Data(Model):

    def __init__(self, id, task_id=None,
                 first_measurement=None,
                 second_measurement=None,
                 third_measurement=None,
        datetime = None):
        super(Data, self).__init__()
        self.id = id
        with self.conn:
            if task_id is not None:
                self.taskId = task_id
            else:
                cur = self.conn.cursor()
                self.taskId = cur.execute("SELECT task_id FROM data WHERE id=?", (self.id,))

            if first_measurement is not None:
                self.first_measurement = first_measurement
            else:
                cur = self.conn.cursor()
                self.first_measurement = cur.execute("SELECT first_measurement FROM data WHERE id=?", (self.id,))

            if second_measurement is not None:
                self.second_measurement = second_measurement
            else:
                cur = self.conn.cursor()
                self.second_measurement = cur.execute("SELECT second_measurement FROM data WHERE id=?", (self.id,))

            if third_measurement is not None:
                self.third_measurement = third_measurement
            else:
                cur = self.conn.cursor()
                self.third_measurement = cur.execute("SELECT third_measurement FROM data WHERE id=?", (self.id,))

            if datetime is not None:
                self.datetime = datetime
            else:
                cur = self.conn.cursor()
                self.datetime = cur.execute("SELECT created_at FROM data WHERE id=?", (self.id,))
