import os
import sys
import time

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(os.path.dirname(TEST_DIR))

sys.path.insert(0, SRC_DIR)
import backend.db as db
from backend.respond import *


def gen_db(fname):
    dump_dir = TEST_DIR + '/.dump'
    if not os.path.isdir(dump_dir):
        os.mkdir(dump_dir)
    fname = dump_dir + '/' + fname
    if os.path.isfile(fname):
        os.remove(fname)
    d = db.DB()
    assert d.open(fname).ok()
    return d


def test1():
    d = gen_db('test_db_1.db')
    assert d.has_user(1234) == False
    assert d.add_user(1234).ok()
    assert d.has_user(1234) == True
    assert d.has_user(2234) == False
    try:
        d.add_user(1234)
    except:
        pass
    else:
        assert False
    assert d.add_user(3456).ok()
    s = d.get_all_users()
    assert s.ok()
    users = s.unpack()
    assert len(users) == 2
    assert 1234 in users
    assert 3456 in users
    d.close()


def test2():
    d = gen_db('test_db_2.db')
    assert d.add_user(1).ok()
    assert d.add_user(2).ok()
    s = d.add_transaction(1, 100)
    assert s.ok()
    assert s.unpack() == 1
    s = d.add_transaction(2, 50, 'comment')
    assert s.ok() and s.unpack() == 2

    s = d.get_last_transaction_ids(user_id=None, count=2)
    assert s.ok
    lst = s.unpack()
    assert len(lst) == 2
    assert lst[0] == 2
    assert lst[1] == 1
    s = d.get_last_transaction_ids(user_id=1, count=20)
    assert s.ok()
    lst = s.unpack()
    assert len(lst) == 1 and lst[0] == 1

    for i in range(10):
        d.add_transaction(2, 30, f'comment {i}')
    s = d.get_last_transaction_ids(user_id=2, count=20)
    assert s.ok() and len(s.unpack()) == 11

    tx = d.add_transaction(2, 20, 'super').unpack()
    assert d.has_transaction(tx)
    tx_info = d.get_transaction(tx)
    assert tx_info.user == 2 and tx_info.value == 20 and tx_info.comment == 'super'

    d.close()


def test3():
    d = gen_db('test_db_3.db')
    assert d.add_user(1).ok()
    assert d.add_user(2).ok()
    assert d.add_user(3).ok()
    tr_id = d.add_transaction(1, 100).unpack()
    assert d.add_count(tr_id, 1, +50).ok()
    assert d.add_count(tr_id, 2, -50).ok()
    tr_id1 = tr_id
    tr_id = d.add_transaction(2, 200).unpack()
    assert d.add_count(tr_id, 1, +100).ok()
    assert d.add_count(tr_id, 2, -50).ok()
    assert d.add_count(tr_id, 3, -50).ok()
    assert d.get_user_count_value(1).unpack() == 150
    users = d.get_transaction_users(tr_id).unpack()
    assert 1 in users and 2 in users and 3 in users
    users = d.get_transaction_users(tr_id1).unpack()
    assert 1 in users and 2 in users


if __name__ == '__main__':
    test1()
    test2()
    test3()
