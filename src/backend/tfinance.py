from backend.respond import *
from backend.utypes import *
import backend.db
import backend.umath


class TFinance:
    def __init__(self, db):
        assert isinstance(db, backend.db.DB)
        assert db.ready()
        self.db = db

    def exit(self):
        self.db.close()

    def register(self, user_id):
        assert isinstance(user_id, int)
        if self.db.has_user(user_id):
            return Error(STATUS.LOGIC_ERROR,
                         f'user "{user_id}" already registered')
        return self.db.add_user(user_id)

    def join(self, user_id, other_user_id):
        assert isinstance(user_id, int) and isinstance(other_user_id, int)
        if not self.db.has_user(user_id):
            return Error(STATUS.LOGIC_ERROR,
                         f'user "{user_id}" is not registered')
        if not self.db.has_user(other_user_id):
            return Error(STATUS.LOGIC_ERROR,
                         f'user "{other_user_id}" is not registered')

        other_user_gid = self.db.get_user_group(other_user_id)
        if other_user_gid.bad(): return other_user_gid

        return self.db.set_user_group(user_id, other_user_gid.unpack())

    def disjoin(self, user_id):
        assert isinstance(user_id, int)
        if not self.db.has_user(user_id):
            return Error(STATUS.LOGIC_ERROR,
                         f'user "{user_id}" is not registered')

        user_gid = self.db.get_user_group(user_id)
        if user_gid.bad(): return user_gid
        user_gid = user_gid.unpack()

        group_users = self.db.get_group_users(user_gid)
        if group_users.bad(): return group_users
        group_users = group_users.unpack()

        if len(group_users) == 1:
            return Error(STATUS.LOGIC_ERROR,
                         f'user "{user_id}" is not in a group')

        new_group = self.db.add_group()
        if new_group.bad(): return new_group

        return self.db.set_user_group(user_id, new_group.unpack())

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

    def log(self, user_id, other_user_id, count):
        assert isinstance(other_user_id, int) or other_user_id is None
        assert isinstance(count, int) and count > 0
        last_tx_ids = self.db.get_last_transaction_ids(other_user_id, count)
        if last_tx_ids.bad(): return last_tx_ids
        ret = []
        for tx_id in last_tx_ids.unpack():
            tx_info = self.db.get_transaction(tx_id)
            if not tx_info: return ERROR(STATUS.DB_CORRUPTED)
            ret.append(tx_info)
        return Ok(ret)

    """ returns a list of utypes.PayOffItems """

    def payment(self, user_id):
        users = self.db.get_all_users()
        if users.bad(): return users
        state = []
        total = 0.
        for user in users.unpack():
            value = self.db.get_user_count_value(user)
            if value.bad(): return value
            value = value.unpack()
            state.append((user, value))
            total += value

        # check that total sum is zero
        if abs(total) > 0.01:
            return Error(STATUS.DB_CORRUPTED,
                         error=f'grand total is non-zero: {total}')

        ret = backend.umath.payment(state)
        return Ok(ret)

    def add(self, user_id, value, other_user_ids=None, comment=None):
        tx_id = self.db.add_transaction(user_id, value, comment).unpack()

        if not other_user_ids:
            other_user_ids = set(self.db.get_all_users().unpack())
        else:
            other_user_ids = set(other_user_ids).union({user_id})

        n_users = len(other_user_ids)
        value_per_user = 1. * value / n_users

        for uid in other_user_ids:
            this_value = -value_per_user + (value if uid == user_id else 0)
            self.db.add_count(tx_id, uid, this_value)

        return Ok()

    def g_add(self, user_id, value, other_user_ids=None, comment=None):
        user_gid = self.db.get_user_group(user_id)
        if user_gid.bad(): return user_gid
        user_gid = user_gid.unpack()

        if not other_user_ids:
            other_user_ids = set(self.db.get_all_users().unpack())
        else:
            other_user_ids = set(other_user_ids).union({user_id})

        tx_id = self.db.add_transaction(user_id, value, comment).unpack()

        groups = {user_gid: [user_id]}
        for uid in other_user_ids:
            gid = self.db.get_user_group(uid).unpack()
            if gid == user_gid: continue
            if gid not in groups: groups[gid] = []
            groups[gid].append(uid)

        value_per_group = 1. * value / len(groups)

        for gid, user_ids in groups.items():
            this_group_size = len(user_ids)
            if gid == user_gid:
                this_value = value - value_per_group
            else:
                this_value = -value_per_group / this_group_size
            for uid in user_ids:
                self.db.add_count(tx_id, uid, this_value)

        return Ok()

    def cancel(self, user_id, tx, comment=None):
        tx_info = self.db.get_transaction(tx)
        if not tx_info:
            return Error(STATUS.LOGIC_ERROR,
                         f'transaction ({tx}) does not exist')
        if tx_info.user != user_id:
            return Error(
                STATUS.LOGIC_ERROR,
                f'''transaction ({tx}) can only be canceled by "{tx_info.user}", not by "{user_id}"'''
            )

        cancel_comment = f'cancel ({tx}) from {tx_info.time}.'
        if comment: cancel_comment += ' ' + comment
        new_tx_id = self.db.add_transaction(user_id, -tx_info.value,
                                            cancel_comment).unpack()

        self.db.add_counts_with_inverse_values(tx, new_tx_id).unpack()

        return Ok()

    def compensate(self, user_id, comment=None):
        comment = 'compensate.' + (' ' + comment if comment else '')
        tx_id = self.db.add_transaction('NULL', 0, comment)
        if tx_id.bad():
            return tx_id
        else:
            tx_id = tx_id.unpack()

        user_ids = self.db.get_all_users()
        if user_ids.bad(): return user_ids
        for user_id in user_ids.unpack():
            value = self.db.get_user_count_value(user_id)
            if value.bad(): return value
            self.db.add_count(tx_id, user_id, -value.unpack())
        return Ok()
