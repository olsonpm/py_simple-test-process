from copy import copy
from types import SimpleNamespace as o

initialLastCalledState = o(wasCalled=False)
lastCalledState = copy(initialLastCalledState)


def report(state):
    global lastCalledState
    lastCalledState = o(testState=state, wasCalled=True)


def resetLastCalledState():
    global lastCalledState
    lastCalledState = copy(initialLastCalledState)
