import pyrtl

if __name__ == "__main__":
    pyrtl.reset_working_block()

    enable = pyrtl.Input(1, "enable")
    reset = pyrtl.Input(1, "reset")
    y = pyrtl.Register(2, "y")

    # TODO: define y.next logic below using the specification in Q4.b)
    # For example: y.next <<= y ^ 1 ...
    next_bit0 = y[0] ^ enable
    next_bit1 = y[1] ^ (y[0] & enable)

    d0 = next_bit0 & ~reset
    d1 = next_bit1 & ~reset

    y.next <<= pyrtl.concat(d1, d0)

    out = pyrtl.Output(2, "out")
    out <<= y

    pyrtl.probe(d0, "d0")
    pyrtl.probe(d1, "d1")

    trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=trace)
    
    # TODO: write more sim.step() cases here and check if the waveform matches expected y.next value

    tests = [
        (1, 0, 0),  # Reset to 0
        (0, 1, 1),  # Increment: 0 -> 1
        (0, 1, 2),  # Increment: 1 -> 2
        (0, 1, 3),  # Increment: 2 -> 3
        (0, 1, 0),  # Wrap around: 3 -> 0
        (0, 0, 0),  # Hold at 0
        (0, 1, 1),  # Increment: 0 -> 1
        (1, 1, 0),  # Reset overrides enable
        (0, 0, 0),  # Hold at 0
    ]

    print("Starting 2-bit counter tests...\n")

    for i, (rst, en, expected) in enumerate(tests, start=1):
        sim.step({"reset": rst, "enable": en})

        actual_next = ((sim.inspect("d1") << 1) | sim.inspect("d0"))

        print(
            f"Test {i}: reset = {rst}, enable={en}, "
            f"current_y={sim.inspect('y'):02b}, "
            f"next_y={actual_next:02b}, "
            f"expected={expected:02b}"
        )

        assert actual_next == expected, (
            f"Test {i} failed: "
            f"expected next state {expected}, "
            f"got {actual_next}"
        )

    trace.render_trace()
    print("All counter tests passed!")