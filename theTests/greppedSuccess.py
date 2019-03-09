#
# README
#  - These tests further inspect the expected suite and test state after "run"
#    is called.  The fixtures here will be more involved compared to the others.
#
#    Also, there's no 'grepFailed' because the grep logic doesn't have any
#    effect on success or fail - and it was easier to keep the 'Success' pattern
#    from previous tests
#


# ------- #
# Imports #
# ------- #

from simple_test_process.state import _getState as getTestState
from types import SimpleNamespace as o
from . import spyReporter
from .utils import makeGetPathToFixture, runProcess

import sys


# ---- #
# Init #
# ---- #

getPathToFixture = makeGetPathToFixture("grepped")

success = getPathToFixture("success")


# ---- #
# Main #
# ---- #


def runTests(r):
    sys.path.insert(0, success)
    grepKeep = o(grepTests=[], grepSuites=[], grep=["keep"])
    code = "runProcess(success, 'theTests.spyReporter', 'False', grepKeep)"
    result = runProcess(success, "theTests.spyReporter", "False", grepKeep)
    testState = getTestState()
    passed = (
        result.code == 0
        and result.stdout is None
        and result.stderr is None
        and hasExpectedRootTests(testState)
        and hasExpectedRootSuites(testState)
        and spyReporter.lastCalledState.wasCalled is True
        and spyReporter.lastCalledState.testState is testState
    )
    if not passed:
        r.addError(code)

    grepTwoTest = o(grepTests=["^two test$"], grepSuites=[], grep=[])
    code = "runProcess(success, 'theTests.spyReporter', 'False', grepTwoTest)"
    result = runProcess(success, "theTests.spyReporter", "False", grepTwoTest)
    testState = getTestState()
    passed = (
        result.code == 0
        and result.stdout is None
        and result.stderr is None
        and hasTest2(testState)
        and len(testState.suites) == 0
        and spyReporter.lastCalledState.wasCalled is True
        and spyReporter.lastCalledState.testState is testState
    )
    if not passed:
        r.addError(code)

    grepSubSuite1 = o(grepTests=[], grepSuites=["^sub suite 1 keep$"], grep=[])
    code = "runProcess(success, 'theTests.spyReporter', 'False', grepSubSuite1)"
    result = runProcess(success, "theTests.spyReporter", "False", grepSubSuite1)
    testState = getTestState()
    passed = (
        result.code == 0
        and result.stdout is None
        and result.stderr is None
        and len(testState.tests) == 0
        and hasSubSuite1(testState)
        and spyReporter.lastCalledState.wasCalled is True
        and spyReporter.lastCalledState.testState is testState
    )
    if not passed:
        r.addError(code)

    sys.path.pop(0)
    del sys.modules["tests"]
    return r


# ------- #
# Helpers #
# ------- #


def hasExpectedRootTests(state):
    test1 = state.tests[0]
    test4 = state.tests[1]

    return (
        len(state.tests) == 2
        and test1.label == "one test keep"
        and test1.fn.__name__ == "oneTest"
        and test1.parentSuite is None
        and test1.rootState is state
        and test1.succeeded
        and test4.label == "four test keep"
        and test4.fn.__name__ == "fourTest"
        and test4.parentSuite is None
        and test4.rootState is state
        and test4.succeeded
    )


def hasExpectedRootSuites(state):
    suite2 = state.suites[0]
    subSuite1 = suite2.suites[0]
    subTest1 = subSuite1.tests[0]

    return (
        len(state.suites) == 1
        and suite2.label == "two suite"
        and suite2.fn.__name__ == "twoSuite"
        and suite2.parentSuite is None
        and suite2.rootState is state
        and suite2.succeeded
        and len(suite2.tests) == 0
        and len(suite2.suites) == 1
        and subSuite1.label == "sub suite 1 keep"
        and subSuite1.fn.__name__ == "subSuite1"
        and subSuite1.parentSuite is suite2
        and subSuite1.rootState is state
        and subSuite1.succeeded
        and len(subSuite1.tests) == 1
        and len(subSuite1.suites) == 0
        and subTest1.label == "sub-sub test 1"
        and subTest1.fn.__name__ == "subSubTest1"
        and subTest1.parentSuite is subSuite1
        and subTest1.rootState is state
        and subTest1.succeeded
    )


def hasTest2(state):
    test = state.tests[0]

    return (
        len(state.tests) == 1
        and test.label == "two test"
        and test.fn.__name__ == "twoTest"
        and test.parentSuite is None
        and test.rootState is state
        and test.succeeded
    )


def hasSubSuite1(state):
    suite2 = state.suites[0]
    subSuite1 = suite2.suites[0]
    subTest1 = subSuite1.tests[0]

    return (
        len(state.suites) == 1
        and suite2.label == "two suite"
        and suite2.fn.__name__ == "twoSuite"
        and suite2.parentSuite is None
        and suite2.rootState is state
        and suite2.succeeded
        and len(suite2.tests) == 0
        and len(suite2.suites) == 1
        and subSuite1.label == "sub suite 1 keep"
        and subSuite1.fn.__name__ == "subSuite1"
        and subSuite1.parentSuite is suite2
        and subSuite1.rootState is state
        and subSuite1.succeeded
        and len(subSuite1.tests) == 1
        and len(subSuite1.suites) == 0
        and subTest1.label == "sub-sub test 1"
        and subTest1.fn.__name__ == "subSubTest1"
        and subTest1.parentSuite is subSuite1
        and subTest1.rootState is state
        and subTest1.succeeded
    )
