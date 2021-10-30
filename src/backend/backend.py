from respond import *
from db import DB

class TFinance:
    def __init__(self, db):
        assert(isinstance(db, DB))
        assert(db.ready())
        self.db = db

    def register(self, user_id):
        assert(isinstance(user_id, int))
        if self.db.has_user(user_id):
            return Error(STATUS.LOGIC_ERROR, f'user @@{user_id} already registered')
        return self.db.register(user_id)

    def join(self, user_id, other_user_id):
        return Error(STATUS.UNIMPLEMENTED)

    def disjoin(self, user_id):
        return Error(STATUS.UNIMPLEMENTED)

    def ack(self, user_id):
        return Error(STATUS.UNIMPLEMENTED)

    def nack(self, user_id):
        return Error(STATUS.UNIMPLEMENTED)

    def stat(self, user_id):
        return Error(STATUS.UNIMPLEMENTED)

    def log(self, user_id, num_tx=None):
        return Error(STATUS.UNIMPLEMENTED)

    def payment(self, user_id, a2a=None):
        return Error(STATUS.UNIMPLEMENTED)

    def add(self, user_id, value, other_user_ids=None, comment=None):
        return Error(STATUS.UNIMPLEMENTED)

    def g_add(self, user_id, value, other_user_ids=None, comment=None):
        return Error(STATUS.UNIMPLEMENTED)

    def cancel(self, user_id, tx, comment=None):
        return Error(STATUS.UNIMPLEMENTED)

    def pay(self, user_id, other_user_ids=None, comment=None):
        return Error(STATUS.UNIMPLEMENTED)

    def reset(self, user_id):
        return Error(STATUS.UNIMPLEMENTED)
