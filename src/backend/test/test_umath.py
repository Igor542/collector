import os
import sys
import time

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(os.path.dirname(TEST_DIR))

sys.path.insert(0, SRC_DIR)
import backend.umath

def validate(state):
    ret = backend.umath.payment(state)
    state = dict(state)
    for r in ret:
        state[r.src] += r.value
        state[r.dst] -= r.value
    for k, v in state.items():
        assert v == 0

def test1():
    state = [
        ('u1',  40),
        ('u2', -35),
        ('u3', -50),
        ('u4',  60),
        ('u5', -15),
    ]
    validate(state)


if __name__ == '__main__':
    test1()
