import atexit

import sqlite3

from backend.respond import *


# aux
def sql_decorator(x):
    if not x:
        return "NULL"
    if type(x) is str:
        return '"%s"' % (x.replace('"', '""'), )
    return '%s' % str(x)


class Transaction:
    def __init__(self, tx_id, time, user, comment):
        self.tx_id = tx_id
        self.time = time
        self.user = user
        self.comment = comment


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
            tx_id       INTEGER PRIMARY KEY AUTOINCREMENT,
            time        DATETIME NOT NULL,
            source      INTEGER NOT NULL REFERENCES Users(uid),
            comment     TEXT);

        CREATE TABLE IF NOT EXISTS Counts (
            tx_id       INTEGER NOT NULL REFERENCES Transactions(tx_id),
            user        INTEGER NOT NULL REFERENCES Users(uid),
            value       REAL);
        """
        self.cur.executescript(req)

    # generic public API

    def open(self, db_path):
        if self.__ready == True:
            raise Exception(
                STATUS.RUNTIME_ERROR,
                f'db: try opening "{db_path}" while "{self.db_path}" already opened'
            )
        self.db_path = db_path
        self.__con = sqlite3.connect(db_path, check_same_thread=False)
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

    # Users

    def has_user(self, uid):
        req = f"""
        SELECT 1 FROM Users WHERE uid = {uid}
        """
        _ = self.cur.execute(req).fetchone()
        return _ is not None

    def get_all_users(self):
        req = f"""
        SELECT uid FROM Users ORDER BY uid ASC
        """
        ret = self.cur.execute(req).fetchall()
        ret = [elem[0] for elem in ret]
        return Ok(ret)

    def add_user(self, uid):
        req = f"""
        INSERT INTO Users VALUES ({uid}, NULL)
        """
        self.cur.execute(req)
        return Ok()

    # Transactions

    def get_transaction(self, tx_id):
        req = f"""
        SELECT time, source, comment FROM Transactions WHERE tx_id = {tx_id}
        """
        _ = self.cur.execute(req).fetchone()
        return Transaction(tx_id, _[0], _[1], _[2]) if _ else None

    def has_transaction(self, tx_id):
        return self.get_transaction(tx_id) is not None

    def add_transaction(self, source_id, comment=None):
        req = """
        INSERT INTO Transactions VALUES (NULL, CURRENT_TIMESTAMP, %d, %s)
        """ % (source_id, sql_decorator(comment))
        self.cur.execute(req)
        return Ok(self.cur.lastrowid)

    def get_last_transactions(self, num_tx, user_id=None):
        order_by = 'tx_id'  # time ?
        maybe_constrain = f'WHERE source = {user_id}' if user_id else ''
        req = f"""
        SELECT tx_id FROM Transactions {maybe_constrain}
        ORDER BY {order_by} DESC LIMIT {num_tx}
        """
        ret = self.cur.execute(req).fetchall()
        ret = [elem[0] for elem in ret]
        return Ok(ret)

    def get_transaction_users(self, tx_id):
        req = f"""
        SELECT user FROM Counts WHERE tx_id = {tx_id}
        """
        ret = self.cur.execute(req).fetchall()
        ret = [elem[0] for elem in ret]
        return Ok(ret)

    # Counts

    def add_count(self, tx_id, user_id, value):
        req = f"""
        INSERT INTO Counts VALUES ({tx_id}, {user_id}, {value})
        """
        self.cur.execute(req)
        return Ok()

    def get_user_count_value(self, user_id):
        req = f"""
        SELECT SUM(value) FROM Counts WHERE user={user_id}
        """
        _ = self.cur.execute(req).fetchone()
        if _: return Ok(_[0])
        return Error(STATUS.OTHER_ERROR,
                     error=f'db:get_user_count_value(user_id={user_id})')

    def add_counts_with_inverse_values(self, cancel_tx, new_tx):
        req = f"""
        SELECT user, value FROM Counts WHERE tx_id = {cancel_tx}
        """
        counts = self.cur.execute(req).fetchall()
        for count in counts:
            user = count[0]
            value = -count[1]
            req = f"""
            INSERT INTO Counts VALUES ({new_tx}, {user}, {value})
            """
            self.cur.execute(req)
        return Ok()
