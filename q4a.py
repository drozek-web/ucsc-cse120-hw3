import pyrtl

def datapath(zero, lt, opcode):
    op0 = opcode[0]
    op1 = opcode[1]

    blt = ~op0 & ~op1 & lt
    bge = op0 & ~op1 & ~lt
    beq = ~op0 & op1 & zero
    bne = op0 & op1 & ~zero

    branch = blt | bge | beq | bne

    return branch

if __name__ == "__main__":
    pyrtl.reset_working_block()

    zero = pyrtl.Input(1, "zero")
    lt = pyrtl.Input(1, "lt")
    opcode = pyrtl.Input(2, "opcode")

    branch_out = datapath(zero, lt, opcode)

    branch = pyrtl.Output(1, "branch")
    branch <<= branch_out

    sim = pyrtl.Simulation()

    # Example test case below, this should PASS
    try:
        sim.step({"zero" : 0, "lt" : 1, "opcode": 0})
        assert sim.inspect("branch") == 1
        print("Test PASS")
    except:
        print("Test FAIL")
    
    # TODO: write test cases here
    for op in range(4):
        for z in range(2):
            for less in range(2):
                sim.step({"zero": z, "lt": less, "opcode": op})
                if op == 0:
                    expected = less
                elif op == 1:
                    expected = 1 - less
                elif op == 2:
                    expected = z
                else:
                    expected = 1 - z
                actual = sim.inspect("branch")
                assert actual == expected, (
                    f"FAIL: opcode={op:02b}, zero={z}, "
                    f"lt={less}, expected={expected}, got={actual}"
                )
    print("All 16 test cases passed!")