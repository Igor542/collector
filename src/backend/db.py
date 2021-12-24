import logging
import sqlite3

from backend.respond import *
from backend.utypes import *


# aux
def sql_decorator(x):
    if not x:
        return "NULL"
    if type(x) is str:
        return '"%s"' % (x.replace('"', '""'), )
    return '%s' % str(x)


class DB:
    def __init__(self):
        self.db_path = None
        self.__ready = False
        self.__con = None
        self.__cur = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

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
            source      INTEGER REFERENCES Users(uid),
            value       REAL NOT NULL,
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
        logging.info(f'Closing db "{self.db_path}"')
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

    def get_user_group(self, uid):
        req = f"""
        SELECT gid FROM Users WHERE uid = {uid}
        """
        ret = self.cur.execute(req).fetchone()
        return Ok(ret[0])

    def add_user(self, uid):
        r = self.add_group()
        if r.bad(): return r
        gid = r.unpack()
        req = f"""
        INSERT INTO Users VALUES ({uid}, {gid})
        """
        self.cur.execute(req)
        return Ok()

    def set_user_group(self, uid, gid):
        req = f"""
        UPDATE Users SET gid = {gid} WHERE uid = {uid}
        """
        self.cur.execute(req)
        return Ok()

    # Groups

    def add_group(self):
        req = f"""
        INSERT Into Groups VALUES (NULL)
        """
        self.cur.execute(req)
        return Ok(self.cur.lastrowid)

    def get_group_users(self, gid):
        req = f"""
        SELECT uid FROM Users WHERE gid = {gid}
        """
        ret = self.cur.execute(req).fetchall()
        ret = [elem[0] for elem in ret]
        return Ok(ret)

    # Transactions

    def get_transaction(self, tx_id):
        req = f"""
        SELECT time, source, value, comment FROM Transactions WHERE tx_id = {tx_id}
        """
        _ = self.cur.execute(req).fetchone()
        return Transaction(tx_id, _[0], _[1], _[2], _[3]) if _ else None

    def has_transaction(self, tx_id):
        return self.get_transaction(tx_id) is not None

    def add_transaction(self, source_id, value, comment=None):
        req = f"""
        INSERT INTO Transactions
        VALUES (NULL, CURRENT_TIMESTAMP, {source_id}, {value}, {sql_decorator(comment)})
        """
        self.cur.execute(req)
        return Ok(self.cur.lastrowid)

    def get_last_transaction_ids(self, user_id, count):
        assert isinstance(user_id, int) or user_id is None
        assert isinstance(count, int) and count > 0
        order_by = 'tx_id'  # time ?
        maybe_constrain = f'WHERE source = {user_id}' if user_id else ''
        req = f"""
        SELECT tx_id FROM Transactions {maybe_constrain}
        ORDER BY {order_by} DESC LIMIT {count}
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

    def get_transaction_range_by_date(self, date_range):
        assert isinstance(date_range, list)
        tx_range = []

        maybe_constrain = ''
        if date_range[0]:
            maybe_constrain = f"WHERE time >= '{date_range[0]}'"

        req = f"""
        SELECT MIN(tx_id) FROM Transactions {maybe_constrain}
        """
        _ = self.cur.execute(req).fetchone()
        if not _:
            return Error(
                STATUS.OTHER_ERROR,
                error=f'db:get_transaction_range_by_date({date_range}). min')
        tx_range.append(_[0])

        maybe_constrain = ''
        if date_range[1]:
            maybe_constrain = f"WHERE time <= '{date_range[1]} 23:59:59'"

        req = f"""
        SELECT MAX(tx_id) FROM Transactions {maybe_constrain}
        """
        _ = self.cur.execute(req).fetchone()
        if not _:
            return Error(
                STATUS.OTHER_ERROR,
                error=f'db:get_transaction_range_by_date({date_range}). max')
        tx_range.append(_[0])

        return Ok(tx_range)

    # Counts

    def add_count(self, tx_id, user_id, value):
        req = f"""
        INSERT INTO Counts VALUES ({tx_id}, {user_id}, {value})
        """
        self.cur.execute(req)
        return Ok()

    def get_counts(self, tx_id):
        req = f"""
        SELECT user, value FROM Counts WHERE tx_id = {tx_id}
        """
        ret = []
        counts = self.cur.execute(req).fetchall()
        for count in counts:
            ret.append(Count(tx_id, count[0], count[1]))
        return Ok(ret)

    def get_user_count_value(self, user_id):
        req = f"""
        SELECT SUM(value) FROM Counts WHERE user={user_id}
        """
        _ = self.cur.execute(req).fetchone()
        if _: return Ok(_[0] if _[0] else 0)
        return Error(STATUS.OTHER_ERROR,
                     error=f'db:get_user_count_value(user_id={user_id})')

    def add_counts_with_inverse_values(self, cancel_tx, new_tx):
        counts = self.get_counts(cancel_tx).unpack()
        for count in counts:
            req = f"""
            INSERT INTO Counts VALUES ({new_tx}, {count.user}, {-count.value})
            """
            self.cur.execute(req)
        return Ok()
