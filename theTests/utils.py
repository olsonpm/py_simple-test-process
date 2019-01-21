# ------- #
# Imports #
# ------- #

from difflib import Differ
from os import path
from simple_test_process.fns import joinWith, passThrough
import subprocess
import sys


# ---- #
# Init #
# ---- #

_d = Differ()
fixturesDir = path.join(path.dirname(__file__), "fixtures")


# ---- #
# Main #
# ---- #


def run(projectDir, reporter, silent):
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "simple_test_process",
            projectDir,
            reporter,
            str(silent),
        ],
        cwd=projectDir,
    )


def makeGetPathToFixture(baseDir):
    def getPathToFixture(rest):
        return path.join(fixturesDir, baseDir, rest)

    return getPathToFixture


def getModuleBasename(m):
    return m.__name__.split(".")[-1]


def diff(left, right):
    result = _d.compare(
        left.splitlines(keepends=True), right.splitlines(keepends=True)
    )
    return passThrough(result, [list, joinWith("")])
