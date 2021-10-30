import utils

class StatusType(utils.ExtedableType):
    pass

STATUS = StatusType()
STATUS.OK = 0
STATUS.OTHER_ERROR = 1
STATUS.UNIMPLEMENTED = 2
STATUS.LOGIC_ERROR = 3
STATUS.DB_NOT_READY = 4

def status_to_str(status):
    assert(isinstance(status, int))
    return {
            STATUS.OTHER_ERROR: 'other error',
            STATUS.UNIMPLEMENTED: 'unimplemented',
            STATUS.LOGIC_ERROR: 'logic error',
            STATUS.DB_NOT_READY: 'db not ready',
            }.get(status, 'unknown status')


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
        error = self.error if self.error else status_to_str(self.status)
        return f'error({self.status}): "{error}"'


class Ok(Respond):
    def __init__(self, obj=None):
        super().__init__(self, STATUS.OK, obj)


class Error(Respond):
    def __init__(self, status, error=''):
        assert(status != STATUS.OK)
        super().__init__(self, status, error=error)
