# ------- #
# Imports #
# ------- #

from case_conversion import separate_words
from .Results import Results
from .utils import getModuleBasename
from simple_test_process.fns import forEach, invokeAttr, isLaden
from . import greppedSuccess, manyFail, manySuccess, simple


# ---- #
# Init #
# ---- #

modules = [simple, manySuccess, manyFail, greppedSuccess]


# ---- #
# Main #
# ---- #


def runTests():
    resultsList = []
    for m in modules:
        moduleName = separate_words(getModuleBasename(m))
        r = Results(moduleName, level=0)
        results = m.runTests(r)
        resultsList.append(results)

    forEach(invokeAttr("printResults"))(resultsList)


__all__ = ["runTests"]


# ------- #
# Helpers #
# ------- #


def hasErrors(result):
    return isLaden(result.errors)
