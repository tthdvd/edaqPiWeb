#!/usr/bin/env python3
import threading
from Edaq530 import Edaq530
import time
import json
import datetime
from models.Task import Task
import dateutil.parser
import pytz
import math
import Edaq530


class EdaqDaemon(threading.Thread):

    def __init__(self, task_id, redis, pubsub):
        threading.Thread.__init__(self)
        self.task_id = task_id
        self.redis = redis
        self.pubsub = pubsub
        self.running = True

    def run(self):
        tz = pytz.timezone('Europe/Budapest')
        self.task = Task(self.task_id)
        end_date = dateutil.parser.parse(self.task.end_date)
        first_channel = int(self.task.first_channel)
        second_channel = int(self.task.second_channel)
        third_channel = int(self.task.third_channel)
        with Edaq530([first_channel, second_channel, third_channel]) as edaq530:
            #mérést megvalósító kód
            while self.running:
                time.sleep(self.task.delay)
                #measurement = edaq530.getMesurementInCelsius()
                measurements = edaq530.getMesurements()
                calculatedMeasurements = []
                print(calculatedMeasurements)

                for i in range(0,3):
                    # ADC to Voltage
                    x = Edaq530Converters.adcCodeToVoltage(measurements[i])
                    calculatedMeasurements.append(eval(self.task.first_equation))

                print(calculatedMeasurements)
                self.task.insertMeasurements(calculatedMeasurements)
                self.redis.publish('edaq530', json.dumps({'event': 'new_value', 'data': calculatedMeasurements}))
                now = datetime.datetime.now()
                if(now > end_date):
                    self.stop()

    def stop(self):
        self.running = False