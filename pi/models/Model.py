#!/usr/bin/env python3
import sqlite3

class Model(object):

    def __init__(self):
        self.conn = sqlite3.connect('edaq530.sql')
        self.create_tables()

    def create_tables(self):
        if self.conn is not None:
            cur = self.conn.cursor()