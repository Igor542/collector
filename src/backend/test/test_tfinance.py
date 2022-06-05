import os
import sys
import time

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(os.path.dirname(TEST_DIR))

sys.path.insert(0, SRC_DIR)
import backend.tfinance as tf
import backend.db as db
from backend.respond import *


def gen_tf(fname):
    dump_dir = TEST_DIR + '/.dump'
    if not os.path.isdir(dump_dir):
        os.mkdir(dump_dir)
    fname = dump_dir + '/' + fname
    if os.path.isfile(fname):
        os.remove(fname)
    d = db.DB()
    assert d.open(fname).ok()
    t = tf.TFinance(d)
    return t


def test1():
    t = gen_tf('test_tf_1.db')
    assert t.register(1).ok()
    assert t.register(2).ok()
    assert t.register(3).ok()

    assert t.add(1, 100, [2], 'tr between 1 and 2').ok()
    assert t.add(1, 15, [2, 3], 'tr between 1, 2, and 3').ok()

    res = t.stat(1).unpack()
    assert res[1] == 60 and res[2] == -55 and res[3] == -5

    assert t.cancel(1, 1, 'revert "tr between 1, 2, and 3"').ok()

    res = t.stat(1).unpack()
    assert res[1] == 10 and res[2] == -5 and res[3] == -5

    res = t.log(1, 1, 1)
    assert res.ok()
    res = res.unpack()
    assert len(res) == 1
    assert res[0].user == 1 and res[0].value == -100

    assert t.add(2, 30, [1, 3], '')

    res = t.log(1, None, 3)
    assert res.ok()
    res = res.unpack()
    assert len(res) == 3
    assert res[0].user == 2 and res[0].value == 30
    assert res[1].user == 1 and res[1].value == -100
    assert res[2].user == 1 and res[2].value == 15

    assert t.compensate(1).ok()

    res = t.payment(1)
    assert res.ok() and len(res.unpack()) == 0

    t.db.close()


def test2():
    t = gen_tf('test_tf_2.db')
    # Create a group of 3 users
    assert t.register(1).ok()
    assert t.register(2).ok()
    assert t.register(3).ok()
    t.join(1, 2)
    t.join(3, 2)
    u1_gid = t.db.get_user_group(1)
    assert u1_gid.ok()
    u2_gid = t.db.get_user_group(2)
    assert u2_gid.ok()
    assert u1_gid.unpack() == u2_gid.unpack()
    # Kick user 1
    assert t.disjoin(1).ok()
    u1_gid = t.db.get_user_group(1)
    assert u1_gid.ok()
    u2_gid = t.db.get_user_group(2)
    assert u2_gid.ok()
    u3_gid = t.db.get_user_group(2)
    assert u2_gid.ok()
    assert u1_gid.unpack() != u2_gid.unpack()
    assert u2_gid.unpack() == u3_gid.unpack()
    # Try to kick the same user again
    assert t.disjoin(1).bad()


def test3():
    t = gen_tf('test_tf_3.db')
    assert t.register(1).ok()
    assert t.register(2).ok()
    assert t.register(3).ok()
    t.join(1, 2)

    assert t.g_add(1, 100, [2], 'tr between 1 and 2').ok()
    res = t.stat(1).unpack()
    assert res[1] == 0 and res[2] == 0 and res[3] == 0

    assert t.g_add(1, 200, [2, 3], 'tr between 1, 2, and 3').ok()
    res = t.stat(1).unpack()
    assert res[1] == 100 and res[2] == 0 and res[3] == -100

    assert t.g_add(3, 200, [1, 2], 'tr between 1, 2, and 3').ok()
    res = t.stat(1).unpack()
    assert res[1] == 50 and res[2] == -50 and res[3] == 0


def test4():
    t = gen_tf('test_tf_4.db')

    # Create a group of 3 users
    assert t.register(1).ok()
    assert t.register(2).ok()
    assert t.register(3).ok()

    assert t.e_add(1, 20, [], 'e_add must have non-empty others').bad()
    assert t.e_add(1, 20, [1, 2, 3],
                   'e_add should not include user_id in others').bad()

    assert t.add(1, 100, [2], 'tr between 1 and 2').ok()
    assert t.e_add(1, 20, [2, 3], 'tr between 2 and 3, where 1 pays').ok()

    res = t.stat(1).unpack()
    assert res[1] == (100 - 50) + (20 - 0), f'res[1] = {res[1]}'
    assert res[2] == (-50) + (-10)
    assert res[3] == (-10)

    res = t.payment(1).unpack()
    assert len(res) == 2
    if True:
        p1, p2 = res[0], res[1]
        if p1.src == 3 and p2.src == 2: p1, p2 = p2, p1
        assert p1.src == 2 and p1.dst == 1 and p1.value == 60
        assert p2.src == 3 and p2.dst == 1 and p2.value == 10

    res = t.spent(1, True, None, None).unpack()
    assert res[1] == 120 and res[2] == 0 and res[3] == 0

    res = t.spent(1, False, None, None).unpack()
    assert res[1] == 50 and res[2] == 60 and res[3] == 10

    assert t.cancel(1, 1, 'revert "tr between 1 and 2"').ok()
    res = t.stat(1).unpack()
    assert res[1] == 20 and res[2] == -10 and res[3] == -10

    assert t.cancel(1, 3, 'cancel revert').ok()
    assert t.cancel(1, 2, 'cancel tr between 2 and 3, where 1 pays').ok()
    res = t.stat(1).unpack()
    assert res[1] == 50 and res[2] == -50 and res[3] == 0


if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
