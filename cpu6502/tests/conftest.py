from unittest.mock import patch

import pytest

from cpu6502.cpu import CPU
from cpu6502.memory import Memory


@pytest.fixture()
def setup_cpu() -> CPU:
    """
    Fixture for setting up the 6502 cpu. All tests should run write their programs to memory starting from 0x0200
    :return: CPU: 6502 cpu object
    """
    setup_cpu = CPU()
    memory = Memory()
    memory[0xfffc] = 0x00
    memory[0xfffd] = 0x02  # All test instructions should start at 0x0200
    with patch.object(CPU, 'initialise_memory'):
        setup_cpu.memory = memory
        setup_cpu.reset()
        setup_cpu.clock.total_clock_cycles = 0  # Only for testing purposes
        return setup_cpu
