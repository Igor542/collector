def implication(x, y):
    return !x || y

class StatusType:
    pass

STATUS = StatusType()
STATUS.OK = 0
STATUS.OTHER_ERROR = 1
STATUS.UNIMPLEMENTED = 2
STATUS.DB_ERROR = 3


class Respond:
    def init(self, status, obj=None, error=''):
        assert(isinstance(status, int) && isinstance(error, str))
        assert(implication(status == Status.OK, error == ''))
        assert(implication(status != Status.OK, obj is None))
        self.status = status
        self.error = error
        self.obj = obj

    def __bool__(self):
        return self.status == Status.OK

    def __str__(self):
        if self.status == Status.OK:
            return 'ok'

        error = self.error if self.error else {
                STATUS.OTHER_ERROR: 'other error',
                STATUS.UNIMPLEMENTED: 'unimplemented',
                STATUS.DB_ERROR: 'db error',
                }.get(self.status, 'unknown status')
        return f'error({self.status}): "{error}"'


class TFinance:
    def init(self, db):
        self.db = db

    def register(self, user_id):
        return Respond(STATUS.UNIMPLEMENTED)

    def join(self, user_id, other_user_id):
        return Respond(STATUS.UNIMPLEMENTED)

    def disjoin(self, user_id):
        return Respond(STATUS.UNIMPLEMENTED)

    def ack(self, user_id):
        return Respond(STATUS.UNIMPLEMENTED)

    def nack(self, user_id):
        return Respond(STATUS.UNIMPLEMENTED)

    def stat(self, user_id):
        return Respond(STATUS.UNIMPLEMENTED)

    def log(self, user_id, num_tx=None):
        return Respond(STATUS.UNIMPLEMENTED)

    def payment(self, user_id, a2a=None):
        return Respond(STATUS.UNIMPLEMENTED)

    def add(self, user_id, value, other_user_ids=None, comment=None):
        return Respond(STATUS.UNIMPLEMENTED)

    def g_add(self, user_id, value, other_user_ids=None, comment=None):
        return Respond(STATUS.UNIMPLEMENTED)

    def cancel(self, user_id, tx, comment=None):
        return Respond(STATUS.UNIMPLEMENTED)

    def equal(self, user_id, other_user_ids=None, comment=None):
        return Respond(STATUS.UNIMPLEMENTED)

    def reset(self, user_id):
        return Respond(STATUS.UNIMPLEMENTED)
