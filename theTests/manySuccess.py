#
# README
#  - These tests further inspect the expected suite and test state after "run"
#    is called.  The fixtures here will be more involved compared to the others.
#


# ------- #
# Imports #
# ------- #

from num2words import num2words
from simple_test_process.state import _getState as getTestState
from types import SimpleNamespace as o
from . import spyReporter
from .utils import makeGetPathToFixture, runProcess

import sys


# ---- #
# Init #
# ---- #

getPathToFixture = makeGetPathToFixture("many")

success = getPathToFixture("success")
noGrepArgs = o(grepTests=[], grepSuites=[], grep=[])


# ---- #
# Main #
# ---- #


def runTests(r):
    sys.path.insert(0, success)
    code = "runProcess(success, 'theTests.spyReporter', 'False', noGrepArgs)"
    result = runProcess(success, "theTests.spyReporter", "False", noGrepArgs)
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

    sys.path.pop(0)
    del sys.modules["tests"]
    return r


# # ------- #
# # Helpers #
# # ------- #


def hasExpectedRootTests(state):
    for i in range(1, 6):
        test = state.tests[i - 1]
        testIsCorrect = (
            test.label == num2words(i) + " test"
            and test.fn.__name__ == num2words(i) + "Test"
            and test.parentSuite is None
            and test.rootState is state
            and test.succeeded
        )

        if not testIsCorrect:
            return False

    return True


def hasExpectedRootSuites(state):
    suite1 = state.suites[0]
    suite2 = state.suites[1]

    return (
        suite1.label == "one suite"
        and suite1.fn.__name__ == "oneSuite"
        and suite1.parentSuite is None
        and suite1.rootState is state
        and suite1.succeeded
        and suite2.label == "two suite"
        and suite2.fn.__name__ == "twoSuite"
        and suite2.parentSuite is None
        and suite2.rootState is state
        and suite2.succeeded
        and hasExpectedNestedTests(state)
        and hasExpectedNestedSuites(state)
    )


def hasExpectedNestedTests(state):
    suite1 = state.suites[0]
    suite2 = state.suites[1]
    subSuite1 = state.suites[1].suites[0]

    subTest1 = suite1.tests[0]
    subTest2 = suite1.tests[1]
    subTest3 = suite2.tests[0]
    subSubTest1 = suite2.suites[0].tests[0]

    return (
        subTest1.label == "sub test 1"
        and subTest1.fn.__name__ == "subTest1"
        and subTest1.parentSuite is suite1
        and subTest1.rootState is state
        and subTest1.succeeded
        and subTest2.label == "sub test 2"
        and subTest2.fn.__name__ == "subTest2"
        and subTest2.parentSuite is suite1
        and subTest2.rootState is state
        and subTest2.succeeded
        and subTest3.label == "sub test 3"
        and subTest3.fn.__name__ == "subTest3"
        and subTest3.parentSuite is suite2
        and subTest3.rootState is state
        and subTest3.succeeded
        and subSubTest1.label == "sub-sub test 1"
        and subSubTest1.fn.__name__ == "subSubTest1"
        and subSubTest1.parentSuite is subSuite1
        and subSubTest1.rootState is state
        and subSubTest1.succeeded
    )


def hasExpectedNestedSuites(state):
    subSuite1 = state.suites[1].suites[0]

    return (
        subSuite1.label == "sub suite 1"
        and subSuite1.fn.__name__ == "subSuite1"
        and len(subSuite1.tests) == 1
        and subSuite1.suites == []
        and subSuite1.parentSuite is state.suites[1]
        and subSuite1.rootState is state
        and subSuite1.succeeded
    )
