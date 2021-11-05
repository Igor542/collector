import utils

class StatusType(utils.ExtendableType):
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
    def __init__(self, status, **kwargs):
        assert(isinstance(status, int))

        self.status = status
        self.obj = None
        self.error = ''

        if status == STATUS.OK:
            if 'obj' in kwargs:
                self.obj = kwargs['obj']
        else:
            assert('error' in kwargs and isinstance(kwargs['error'], str))
            self.error = kwargs['error']

    def __bool__(self):
        return self.status == STATUS.OK

    def __str__(self):
        if self.status == STATUS.OK:
            return 'ok'
        error = self.error if self.error else status_to_str(self.status)
        return f'error({self.status}): "{error}"'


class Ok(Respond):
    def __init__(self, obj=None):
        super().__init__(STATUS.OK, obj=None)


class Error(Respond):
    def __init__(self, status, error=''):
        assert(status != STATUS.OK)
        super().__init__(status, error=error)
