def afterTest1():
    afterTest1.numTimesRan += 1


def beforeTest1():
    beforeTest1.numTimesRan += 1


def afterSuite1():
    afterSuite1.numTimesRan += 1


def beforeSuite1():
    beforeSuite1.numTimesRan += 1


def afterEachSuite1():
    afterEachSuite1.numTimesRan += 1


def beforeEachSuite1():
    beforeEachSuite1.numTimesRan += 1


def afterEachSuite2():
    afterEachSuite2.numTimesRan += 1


def beforeEachSuite2():
    beforeEachSuite2.numTimesRan += 1


afterTest1.numTimesRan = 0
beforeTest1.numTimesRan = 0
afterSuite1.numTimesRan = 0
beforeSuite1.numTimesRan = 0
afterEachSuite1.numTimesRan = 0
beforeEachSuite1.numTimesRan = 0
afterEachSuite2.numTimesRan = 0
beforeEachSuite2.numTimesRan = 0


@test("test1", after=afterTest1, before=beforeTest1)
def test1():
    pass


@suite(
    "suite1",
    after=afterSuite1,
    afterEach=afterEachSuite1,
    before=beforeSuite1,
    beforeEach=beforeEachSuite1,
)
def suite1():
    @test("test2")
    def test2():
        pass

    @suite("suite2", afterEach=afterEachSuite2, beforeEach=beforeEachSuite2)
    def suite2():
        @test("test3")
        def test3():
            pass
