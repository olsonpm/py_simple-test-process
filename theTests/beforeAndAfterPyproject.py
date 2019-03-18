# ------- #
# Imports #
# ------- #

from os import path
from rm import rm
from simple_test_process.state import _getState as getTestState
from types import SimpleNamespace as o
from . import spyReporter
from .utils import makeGetPathToFixture, runProcess

import os
import sys


# ---- #
# Init #
# ---- #

getPathToFixture = makeGetPathToFixture("beforeAndAfterPyproject")

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
    successFiles = set(os.listdir(success))
    passed = (
        result.code == 0
        and result.stdout is None
        and result.stderr is None
        and len(testState.tests) == 1
        and testState.after.__name__ != "noop"
        and testState.before.__name__ != "noop"
        and "after-ran.txt" in successFiles
        and "before-ran.txt" in successFiles
        and spyReporter.lastCalledState.testState is testState
    )
    if not passed:
        print(result.stderr)
        r.addError(code)

    rm(
        [
            path.join(success, "after-ran.txt"),
            path.join(success, "before-ran.txt"),
        ]
    )

    sys.path.pop(0)
    return r
