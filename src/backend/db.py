import sqlite3

from respond import *

# aux
def sql_decorator(x):
    if not x:
        return "NULL"
    if type(x) is str:
        return '"%s"' % (x.replace('"', '""'),)
    return '%s' % str(x)


class DB:
    def __init__(self):
        self.db_path = None
        self.__ready = False
        self.con = None
        self.cur = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.con:
            self.con.close()

    def __create_tables(self):
        req = """
        CREATE TABLE IF NOT EXISTS Groups (
            gid         INTEGER PRIMARY KEY AUTOINCREMENT);

        CREATE TABLE IF NOT EXISTS Users (
            uid         INTEGER PRIMARY KEY AUTOINCREMENT,
            gid         INTEGER REFERENCES Groups(gid),
            name        TEXT UNIQUE NOT NULL);

        CREATE TABLE IF NOT EXISTS Transactions (
            tr_id       INTEGER PRIMARY KEY AUTOINCREMENT,
            source      INTEGER NOT NULL REFERENCES Users(uid),
            comment     TEXT);

        CREATE TABLE IF NOT EXISTS Counts (
            tr_id       INTEGER NOT NULL REFERENCES Transactions(tr_id),
            user        INTEGER NOT NULL REFERENCES Users(uid),
            value       REAL);
        """
        self.cur.executescript(req)

    def __add_user(self, name):
        req = """
        INSERT INTO Users VALUES (NULL, NULL, %s)
        """ % sql_decorator(name)
        self.cur.execute(req)

    def __get_user_uid(self, name):
        req = """
        SELECT uid FROM Users WHERE name = %s
        """ % sql_decorator(name)
        uid = self.cur.execute(req).fetchone()
        return uid[0] if uid else None

    def open(self, db_path):
        if self.__ready == True:
            raise Exception(STATUS.RUNTIME_ERROR, f'db: try opening "{db_path}" while "{self.db_path}" already opened')
        self.db_path = db_path
        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()
        self.__ready = True
        self.__create_tables()
        return Ok()

    def close(self):
        if self.con:
            self.con.commit()
            self.con.close()
        self.db_path = None
        self.__ready = False
        self.con = None
        self.cur = None

    def ready(self):
        return self.__ready == True

    def has_user(self, user_id):
        if not self.ready():
            raise Exception(STATUS.DB_NOT_READY)
        return self.__get_user_uid(user_id) is not None

    def register(self, user_id):
        if not self.ready():
            raise Exception(STATUS.DB_NOT_READY)

        self.__add_user(user_id)
        self.con.commit()
        return Ok()
