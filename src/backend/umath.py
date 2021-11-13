from backend.utypes import PayOffItem

"""
Input:
    - state: list of pairs(key, value)
Returns:
    - list of PayOffItem
Requirement:
    - sum(value) = 0
"""
def payment(state):
    assert len(state) >= 1
    state = [x for x in state] # copy state

    def state_sort(state): state.sort(key = lambda x: x[1])

    length = len(state)

    ret = []
    while True:
        state_sort(state)

        dept = - state[0][1]
        if dept == 0: break

        for i in range(length):
            j = length - 1 - i
            if state[j][1] <= 0:
                assert j + 1 < length
                assert state[j+1][1] > 0
                ret.append(PayOffItem(state[0][0], state[j+1][0], dept))
                state[0] = (state[0][0], 0)
                state[j+1] = (state[j+1][0], state[j+1][1] - dept)
                state_sort(state)
                break
            elif state[j][1] <= dept:
                ret.append(PayOffItem(state[0][0], state[j][0], state[j][1]))
                state[0] = (state[0][0], state[0][1] + state[j][1])
                state[j] = (state[j][0], 0)
                state_sort(state)
                break

    return ret
