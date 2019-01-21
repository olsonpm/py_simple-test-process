@test("one test")
def oneTest():
    raise Exception("one test")


@test("two test")
def twoTest():
    pass


@suite("one suite")
def oneSuite():
    @test("sub test 1")
    def subTest1():
        raise Exception("sub test 1")

    @test("sub test 2")
    def subTest2():
        pass


@test("three test")
def threeTest():
    pass
