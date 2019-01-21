@suite("two suite")
def twoSuite():
    @test("sub test 3")
    def subTest3():
        pass

    @suite("sub suite 1")
    def subSuite1():
        @test("sub-sub test 1")
        def subSubTest1():
            pass


@test("five test")
def fiveTest():
    pass
