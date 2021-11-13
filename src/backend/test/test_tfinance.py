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

    t.db.close()


if __name__ == '__main__':
    test1()
