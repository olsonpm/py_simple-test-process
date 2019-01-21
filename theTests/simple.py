# ------- #
# Imports #
# ------- #

from simple_test_process.runProcess import runProcess
from simple_test_process.state import _getState as getTestState
from . import spyReporter
from .utils import makeGetPathToFixture

import sys


# ---- #
# Init #
# ---- #

getPathToFixture = makeGetPathToFixture("simple")

error = getPathToFixture("error")
fail = getPathToFixture("fail")
noTests = getPathToFixture("noTests")
success = getPathToFixture("success")
successDir = getPathToFixture("successDir")


# ---- #
# Main #
# ---- #


def runTests(r):
    sys.path.insert(0, success)
    code = "runProcess(success, 'theTests.spyReporter', 'False')"
    result = runProcess(success, "theTests.spyReporter", "False")
    testState = getTestState()
    passed = (
        result.code == 0
        and result.stdout is None
        and result.stderr is None
        and len(testState.rootTests) == 1
        and spyReporter.lastCalledState.testState is testState
    )
    if not passed:
        r.addError(code)

    #
    # silent
    #
    spyReporter.resetLastCalledState()
    code = "runProcess(success, 'theTests.spyReporter', 'True')"
    result = runProcess(success, "theTests.spyReporter", "True")
    testState = getTestState()
    passed = (
        result.code == 0
        and result.stdout is None
        and result.stderr is None
        and len(testState.rootTests) == 1
        and spyReporter.lastCalledState.wasCalled is False
    )
    if not passed:
        r.addError(code)

    #
    # fail
    #
    del sys.modules["tests"]
    sys.path[0] = fail
    spyReporter.resetLastCalledState()
    code = "runProcess(fail, 'theTests.spyReporter', 'False')"
    result = runProcess(fail, "theTests.spyReporter", "False")
    testState = getTestState()
    expectedErrorStr = "test failed"
    passed = (
        result.code == 1
        and result.stdout is None
        and result.stderr is None
        and len(testState.rootTests) == 1
        and expectedErrorStr in str(testState.rootTests[0].error)
        and spyReporter.lastCalledState.wasCalled is True
        and spyReporter.lastCalledState.testState is testState
    )
    if not passed:
        r.addError(code)

    #
    # error
    #
    del sys.modules["tests"]
    sys.path[0] = error
    spyReporter.resetLastCalledState()
    code = "runProcess(error, 'theTests.spyReporter', 'False')"
    result = runProcess(error, "theTests.spyReporter", "False")
    expectedErrorStr = "test import error"
    passed = (
        result.code == 2
        and result.stdout is None
        and expectedErrorStr in result.stderr
        and spyReporter.lastCalledState.wasCalled is False
    )
    if not passed:
        r.addError(code)

    #
    # successDir
    #
    del sys.modules["tests"]
    sys.path[0] = successDir
    spyReporter.resetLastCalledState()
    code = "runProcess(successDir, 'theTests.spyReporter', 'False')"
    result = runProcess(successDir, "theTests.spyReporter", "False")
    testState = getTestState()
    passed = (
        result.code == 0
        and result.stdout is None
        and result.stderr is None
        and len(testState.rootTests) == 1
        and spyReporter.lastCalledState.wasCalled is True
    )
    if not passed:
        r.addError(code)

    #
    # noTests
    #
    del sys.modules["tests"]
    sys.path[0] = noTests
    spyReporter.resetLastCalledState()
    code = "runProcess(noTests, 'theTests.spyReporter', 'False')"
    result = runProcess(noTests, "theTests.spyReporter", "False")
    testState = getTestState()
    expectedErrorStr = "No tests were found in any python files"
    passed = (
        result.code == 2
        and result.stdout is None
        and expectedErrorStr in result.stderr
        and len(testState.rootTests) == 0
        and spyReporter.lastCalledState.wasCalled is False
    )
    if not passed:
        print(len(testState.rootTests))
        r.addError(code)

    sys.path.pop(0)
    return r
