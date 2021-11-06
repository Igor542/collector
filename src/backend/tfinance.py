from backend.respond import *
from backend.db import DB

class TFinance:
    def __init__(self, db):
        assert(isinstance(db, DB))
        assert(db.ready())
        self.db = db

    def register(self, user_id):
        assert(isinstance(user_id, int))
        if self.db.has_user(user_id):
            return Error(STATUS.LOGIC_ERROR, f'user @@{user_id} already registered')
        return self.db.add_user(user_id)

    def join(self, user_id, other_user_id):
        return Error(STATUS.UNIMPLEMENTED)

    def disjoin(self, user_id):
        return Error(STATUS.UNIMPLEMENTED)

    def ack(self, user_id):
        return Error(STATUS.UNIMPLEMENTED)

    def nack(self, user_id):
        return Error(STATUS.UNIMPLEMENTED)

    def stat(self, user_id):
        ret = dict()
        users = self.db.get_all_users().unpack()
        for user in users:
            value = self.db.get_user_count_value(user)
            if value.bad(): return value
            ret[user] = value.unpack()
        return Ok(ret)

    def log(self, user_id, num_tx=None):
        return Error(STATUS.UNIMPLEMENTED)

    def payment(self, user_id, a2a=None):
        return Error(STATUS.UNIMPLEMENTED)

    def add(self, user_id, value, other_user_ids=None, comment=None):
        tr_id = self.db.add_transaction(user_id, comment=comment).unpack()

        if not other_user_ids:
            other_user_ids = set(self.db.get_all_users().unpack())
        else:
            other_user_ids = set(other_user_ids).union({user_id})

        n_users = len(other_user_ids)
        value_per_user = 1. * value / n_users

        for uid in other_user_ids:
            this_value = -value_per_user + (value if uid == user_id else 0)
            self.db.add_count(tr_id, uid, this_value).unpack()

        return Ok()

    def g_add(self, user_id, value, other_user_ids=None, comment=None):
        return Error(STATUS.UNIMPLEMENTED)

    def cancel(self, user_id, tx, comment=None):
        return Error(STATUS.UNIMPLEMENTED)

    def pay(self, user_id, other_user_ids=None, comment=None):
        return Error(STATUS.UNIMPLEMENTED)

    def reset(self, user_id):
        return Error(STATUS.UNIMPLEMENTED)
