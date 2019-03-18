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

getPathToFixture = makeGetPathToFixture("beforeAndAfterEach")

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
    test1 = testState.tests[0]
    suite1 = testState.suites[0]
    suite2 = suite1.suites[0]
    passed = (
        result.code == 0
        and result.stdout is None
        and result.stderr is None
        and len(testState.tests) == 1
        and len(testState.suites) == 1
        and test1.after.__name__ == "afterTest1"
        and test1.after.numTimesRan == 1
        and test1.before.__name__ == "beforeTest1"
        and test1.before.numTimesRan == 1
        and test1.before.__name__ == "beforeTest1"
        and test1.before.numTimesRan == 1
        and suite1.after.__name__ == "afterSuite1"
        and suite1.after.numTimesRan == 1
        and suite1.before.__name__ == "beforeSuite1"
        and suite1.before.numTimesRan == 1
        and len(suite1.afterEach) == 1
        and len(suite1.beforeEach) == 1
        and suite1.afterEach[0].__name__ == "afterEachSuite1"
        and suite1.afterEach[0].numTimesRan == 2
        and suite1.beforeEach[0].__name__ == "beforeEachSuite1"
        and suite1.beforeEach[0].numTimesRan == 2
        and len(suite2.afterEach) == 2
        and len(suite2.beforeEach) == 2
        and suite2.afterEach[1].__name__ == "afterEachSuite2"
        and suite2.afterEach[1].numTimesRan == 1
        and suite2.beforeEach[1].__name__ == "beforeEachSuite2"
        and suite2.beforeEach[1].numTimesRan == 1
        and spyReporter.lastCalledState.testState is testState
    )
    if not passed:
        print("suite1.after.numTimesRan: " + str(suite1.after.numTimesRan))
        r.addError(code)

    sys.path.pop(0)
    return r
