@test("one test")
def oneTest():
    pass


@test("two test")
def twoTest():
    pass


@suite("one suite")
def oneSuite():
    @test("sub test 1")
    def subTest1():
        pass

    @test("sub test 2")
    def subTest2():
        pass


@test("three test")
def threeTest():
    pass
