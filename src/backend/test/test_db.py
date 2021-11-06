import os
import sys
import time

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, p)
import backend.db as db
# from backend import db
from backend.respond import *

def gen_db(fname):
    if os.path.isfile(fname):
        os.remove(fname)
    d = db.DB()
    assert(d.open(fname).ok())
    return d

def test1():
    d = gen_db('_test1.db')
    assert(d.has_user(1234) == False)
    assert(d.add_user(1234).ok())
    assert(d.has_user(1234) == True)
    assert(d.has_user(2234) == False)
    try:
        d.add_user(1234)
    except:
        pass
    else:
        assert(False)
    assert(d.add_user(3456).ok())
    s = d.get_all_users()
    assert(s.ok())
    assert(len(s.unpack()) == 2)
    d.close()

def test2():
    d = gen_db('_test2.db')
    assert(d.add_user(1).ok())
    assert(d.add_user(2).ok())
    s = d.add_transaction(1)
    assert(s.ok())
    assert(s.unpack() == 1)
    s = d.add_transaction(2, 'comment')
    assert(s.ok() and s.unpack() == 2)

    s = d.get_last_transactions(2)
    assert(s.ok)
    lst = s.unpack()
    assert(len(lst) == 2)
    assert(lst[0] == 2)
    assert(lst[1] == 1)
    s = d.get_last_transactions(2, user_id=1)
    assert(s.ok())
    lst = s.unpack()
    assert(len(lst) == 1 and lst[0] == 1)

    for i in range(10):
        d.add_transaction(2, f'comment {i}')
    s = d.get_last_transactions(20, user_id=2)
    assert(s.ok() and len(s.unpack()) == 11)

    d.close()

def test3():
    d = gen_db('_test2.db')
    assert(d.add_user(1).ok())
    assert(d.add_user(2).ok())
    assert(d.add_user(3).ok())
    tr_id = d.add_transaction(1).unpack()
    assert(d.add_count(tr_id, 1, +50).ok())
    assert(d.add_count(tr_id, 2, -50).ok())

test1()
test2()
test3()
