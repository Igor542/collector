import os
import sys
import time

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(os.path.dirname(TEST_DIR))

sys.path.insert(0, SRC_DIR)
import backend.umath

def test1():
    state = [
        ('u1',  40),
        ('u2', -35),
        ('u3', -50),
        ('u4',  60),
        ('u5',  -5),
    ]
    ret = backend.umath.payment(state)
    for i in ret:
        print(i)


if __name__ == '__main__':
    test1()
