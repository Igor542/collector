import atexit

import sqlite3

from backend.respond import *

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
        self.__con = None
        self.__cur = None
        atexit.register(self.close)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.__con:
            self.__con.close()

    @property
    def cur(self):
        if not self.ready():
            raise Exception(STATUS.DB_NOT_READY)
        return self.__cur

    def __create_tables(self):
        req = """
        CREATE TABLE IF NOT EXISTS Groups (
            gid         INTEGER PRIMARY KEY AUTOINCREMENT);

        CREATE TABLE IF NOT EXISTS Users (
            uid         INTEGER PRIMARY KEY,
            gid         INTEGER REFERENCES Groups(gid));

        CREATE TABLE IF NOT EXISTS Transactions (
            tr_id       INTEGER PRIMARY KEY AUTOINCREMENT,
            time        DATETIME NOT NULL,
            source      INTEGER NOT NULL REFERENCES Users(uid),
            comment     TEXT);

        CREATE TABLE IF NOT EXISTS Counts (
            tr_id       INTEGER NOT NULL REFERENCES Transactions(tr_id),
            user        INTEGER NOT NULL REFERENCES Users(uid),
            value       REAL);
        """
        self.cur.executescript(req)

    def __add_user(self, uid):
        req = f"""
        INSERT INTO Users VALUES ({uid}, NULL)
        """
        self.cur.execute(req)

    def __has_user(self, uid):
        req = f"""
        SELECT 1 FROM Users WHERE uid = {uid}
        """
        _ = self.cur.execute(req).fetchone()
        return _ is not None

    # generic public API

    def open(self, db_path):
        if self.__ready == True:
            raise Exception(STATUS.RUNTIME_ERROR, f'db: try opening "{db_path}" while "{self.db_path}" already opened')
        self.db_path = db_path
        self.__con = sqlite3.connect(db_path)
        self.__cur = self.__con.cursor()
        self.__ready = True
        self.__create_tables()
        return Ok()

    def close(self):
        if self.__con:
            self.__con.commit()
            self.__con.close()
        self.__con = None
        self.__ready = False
        self.db_path = None

    def ready(self):
        return self.__ready == True

    # public API

    def has_user(self, uid):
        return self.__has_user(uid)

    def get_all_users(self):
        req = f"""
        SELECT uid FROM Users ORDER BY uid ASC
        """
        ret = self.cur.execute(req).fetchall()
        ret = [elem[0] for elem in ret]
        return Ok(ret)

    def add_user(self, uid):
        self.__add_user(uid)
        return Ok()

    def add_transaction(self, source_id, comment=None):
        req = """
        INSERT INTO Transactions VALUES (NULL, CURRENT_TIMESTAMP, %d, %s)
        """ % (source_id, sql_decorator(comment))
        self.cur.execute(req)
        return Ok(self.cur.lastrowid)

    def get_last_transactions(self, num_tx, user_id=None):
        order_by = 'tr_id' # time ?
        maybe_constrain = f'WHERE source = {user_id}' if user_id else ''
        req = f"""
        SELECT tr_id FROM Transactions {maybe_constrain}
        ORDER BY {order_by} DESC LIMIT {num_tx}
        """
        ret = self.cur.execute(req).fetchall()
        ret = [elem[0] for elem in ret]
        return Ok(ret)

    def add_count(self, tr_id, user, value):
        req = f"""
        INSERT INTO Counts VALUES ({tr_id}, {user}, {value})
        """
        self.cur.execute(req)
        return Ok()
