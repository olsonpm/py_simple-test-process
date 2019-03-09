# ------- #
# Imports #
# ------- #

from difflib import Differ
from os import path
from simple_test_process.runProcess import runProcess as runProcess_original
from simple_test_process.fns import joinWith, passThrough


# ---- #
# Init #
# ---- #

_d = Differ()
fixturesDir = path.join(path.dirname(__file__), "fixtures")


# ---- #
# Main #
# ---- #


def diff(left, right):
    result = _d.compare(
        left.splitlines(keepends=True), right.splitlines(keepends=True)
    )
    return passThrough(result, [list, joinWith("")])


def getModuleBasename(m):
    return m.__name__.split(".")[-1]


def makeGetPathToFixture(baseDir):
    def getPathToFixture(rest):
        return path.join(fixturesDir, baseDir, rest)

    return getPathToFixture


#
# I'm not sure how to organize this - as the kwargs are too verbose for a quick
#   reference as a failed test, but `runProcessWrapper` also pushes the strings
#   past 80 lines.  Whatever
#


def runProcess(projectDir, reporter, silent, grepArgs):
    return runProcess_original(
        projectDir=projectDir,
        reporter=reporter,
        silent=silent,
        grepArgs=grepArgs,
    )
