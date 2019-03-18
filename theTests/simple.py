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

getPathToFixture = makeGetPathToFixture("simple")

error = getPathToFixture("error")
fail = getPathToFixture("fail")
noTests = getPathToFixture("noTests")
success = getPathToFixture("success")
successDir = getPathToFixture("successDir")
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
        and len(testState.tests) == 1
        and spyReporter.lastCalledState.testState is testState
    )
    if not passed:
        r.addError(code)

    #
    # silent
    #
    spyReporter.resetLastCalledState()
    code = "runProcess(success, 'theTests.spyReporter', 'True', noGrepArgs)"
    result = runProcess(success, "theTests.spyReporter", "True", noGrepArgs)
    testState = getTestState()
    passed = (
        result.code == 0
        and result.stdout is None
        and result.stderr is None
        and len(testState.tests) == 1
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
    code = "runProcess(fail, 'theTests.spyReporter', 'False', noGrepArgs)"
    result = runProcess(fail, "theTests.spyReporter", "False", noGrepArgs)
    testState = getTestState()
    expectedErrorStr = "test failed"
    passed = (
        result.code == 1
        and result.stdout is None
        and result.stderr is None
        and len(testState.tests) == 1
        and expectedErrorStr in str(testState.tests[0].error)
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
    code = "runProcess(error, 'theTests.spyReporter', 'False', noGrepArgs)"
    result = runProcess(error, "theTests.spyReporter", "False", noGrepArgs)
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
    code = "runProcess(successDir, 'theTests.spyReporter', 'False', noGrepArgs)"
    result = runProcess(successDir, "theTests.spyReporter", "False", noGrepArgs)
    testState = getTestState()
    passed = (
        result.code == 0
        and result.stdout is None
        and result.stderr is None
        and len(testState.tests) == 1
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
    code = "runProcess(noTests, 'theTests.spyReporter', 'False', noGrepArgs)"
    result = runProcess(noTests, "theTests.spyReporter", "False", noGrepArgs)
    testState = getTestState()
    expectedErrorStr = "No tests were found in any python files"
    passed = (
        result.code == 2
        and result.stdout is None
        and expectedErrorStr in result.stderr
        and len(testState.tests) == 0
        and spyReporter.lastCalledState.wasCalled is False
    )
    if not passed:
        r.addError(code)

    sys.path.pop(0)
    return r
