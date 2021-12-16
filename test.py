@test.describe("Fixed tests")
def fixed_tests():
    @test.it("Allocate is constrained by memory size")
    def it_1():
        mem = MemoryManager([None] * 256)
        test.expect_error("Cannot allocate more memory than exists", lambda: mem.allocate(512))
        pointer1 = mem.allocate(128)
        test.expect(pointer1 >= 0, "Alloc should return pointer")
        test.expect_error("Cannot allocate more memory than available", lambda: mem.allocate(129))
    
    @test.it("Allocate does not have a memory overhead")
    def it_2():
        mem = MemoryManager([None] * 256)
        for i in range(256):
            test.expect(0 <= mem.allocate(1) < 256, "Should be able to allocate 256 blocks of size 1")

    @test.it("Released memory may be re-allocated")
    def it_3():
        mem = MemoryManager([None] * 64)
        pointer1 = mem.allocate(32)
        pointer2 = mem.allocate(32)
        mem.release(pointer1)
        test.expect(mem.allocate(32) < 64, "Should be able to allocate 32 bits")

    @test.it("Released memory is merged when free blocks are adjacent")
    def it_4():
        mem = MemoryManager([None] * 64)
        pointer1 = mem.allocate(16)
        pointer2 = mem.allocate(16)
        pointer3 = mem.allocate(16)
        pointer4 = mem.allocate(16)
        mem.release(pointer2)
        mem.release(pointer3);
        test.expect(mem.allocate(32) < 64, "Deallocated memory should be merged")

    @test.it("May not write to unallocated blocks")
    def it_5():
        mem = MemoryManager([None] * 64)
        test.expect_error("No memory has been allocated", lambda: mem.write(1,1))

    @test.it("May write to allocated blocks")
    def it_6():
        array = [None] * 64
        a, b, c, d = 0, 1, 31, 32
        mem = MemoryManager(array)
        pointer1 = mem.allocate(32)
        mem.write(pointer1, a)
        mem.write(pointer1 + b, b)
        mem.write(pointer1 + c, c)
        test.expect_error('should throw on write to allocated pointer + 32', lambda: mem.write(pointer1 + d, d))
        test.assert_equals(array[pointer1 + a], a, "Value at pointer + {}".format(a))
        test.assert_equals(array[pointer1 + b], b, "Value at pointer + {}".format(b))
        test.assert_equals(array[pointer1 + c], c, "Value at pointer + {}".format(c))
        test.assert_not_equals(array[pointer1 + d], d, "Value at pointer + {}".format(d))

    @test.it("May not read from unallocated blocks")
    def it_7():
        mem = MemoryManager([None] * 64)
        test.expect_error("No memory has been allocated", lambda: mem.read(1))

    @test.it("May read from allocated blocks")
    def it_8():
        mem = MemoryManager([None] * 64)
        pointer1 = mem.allocate(32)
        mem.write(pointer1, 1)
        mem.read(pointer1)
        test.assert_equals(mem.read(pointer1), 1, "Correct value should be returned")
        test.assert_equals(mem.read(pointer1 + 1), None, "Unwritten location should be undefined")
