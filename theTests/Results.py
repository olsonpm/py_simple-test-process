# ------- #
# Imports #
# ------- #

from simple_chalk import green, red
from simple_test_process.fns import isEmpty


# ---- #
# Init #
# ---- #

x = red("✘")
o = green("✔")


# ---- #
# Main #
# ---- #


class Results:
    def __init__(self, name, *, level=0):
        self.level = level
        self.name = name
        self.errors = []

    def addError(self, e):
        self.errors.append(e)
        return self

    def shouldHaveRaisedAnError(self, code):
        self.errors.append(f"'{code}' should have raised an error")
        return self

    def shouldNotHaveRaisedAnError(self, code):
        self.errors.append(f"'{code}' should not have raised an error")
        return self

    def raisedUnexpectedError(self, code):
        self.errors.append(f"'{code}' raised an unexpected error")
        return self

    def printResults(self):
        name = self.name
        errors = self.errors
        indent = "  " * self.level

        if isEmpty(errors):
            print(f"{indent}{o} {name}")
        else:
            print()
            print(f"{indent}{name}")

            for e in errors:
                print(f"{indent}  {x} {e}")

            print()
