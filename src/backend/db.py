import sqlite3

from respond import *

class DB:
    def __init__(self):
        self.db_path = None
        self.ready == False
        self.con = None
        self.cur = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.con:
            self.con.close()

    def open(self, db_path):
        if self.ready == True:
            raise Exception(STATUS.RUNTIME_ERROR, f'db: try opening "{db_path}" while "{self.db_path}" already opened')
        self.db_path = db_path
        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()
        self.ready = True
        return Ok()

    def close(self):
        if self.con:
            self.con.close()
        self.db_path = None
        self.ready = False
        self.con = None
        self.cur = None

    def ready(self):
        return self.ready == True

    def has_user(self, user_id):
        if not self.ready():
            raise Exception(STATUS.DB_NOT_READY)
        return False

    def register(self, user_id):
        if not self.ready():
            raise Exception(STATUS.DB_NOT_READY)

        return Error(STATUS.UNIMPLEMENTED)

