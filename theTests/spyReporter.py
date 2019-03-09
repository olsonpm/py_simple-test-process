from copy import deepcopy
from types import SimpleNamespace as o

initialLastCalledState = o(wasCalled=False)
lastCalledState = deepcopy(initialLastCalledState)


def report(state):
    global lastCalledState
    lastCalledState = o(testState=state, wasCalled=True)


def resetLastCalledState():
    global lastCalledState
    lastCalledState = deepcopy(initialLastCalledState)
