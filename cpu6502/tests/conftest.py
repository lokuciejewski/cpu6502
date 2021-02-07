import pytest

from cpu6502.cpu import CPU


@pytest.fixture()
def setup_cpu() -> CPU:
    """
    Fixture for setting up the 6502 cpu. All tests should run write their programs to memory starting from 0x0200
    :return: CPU: 6502 cpu object
    """
    setup_cpu = CPU()
    setup_cpu.reset()
    setup_cpu.memory[0xfffc] = 0x4c
    setup_cpu.memory[0xfffd] = 0x00
    setup_cpu.memory[0xfffe] = 0x02  # JMP 0x0200
    setup_cpu.execute(1)
    setup_cpu.clock.total_clock_cycles = 0
    return setup_cpu
