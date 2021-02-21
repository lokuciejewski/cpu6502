from unittest.mock import patch

import pytest

from cpu6502.cpu import CPU
from cpu6502.memory import Memory


@pytest.mark.usefixtures('setup_cpu')
class TestFunctional:

    def test_functional(self, setup_cpu):
        memory = Memory()
        try:
            memory.load_binary_file('6502_functional_test.bin', start_offset=0xa)
        except FileNotFoundError:
            memory.load_binary_file('cpu6502/tests/6502_functional_test.bin', start_offset=0xa)
        with patch.object(CPU, 'initialise_memory'):
            setup_cpu.memory = memory
            setup_cpu.reset()
            setup_cpu.pc = 0x400

        old_pc = setup_cpu.pc
        while setup_cpu.pc < 0xffff:
            setup_cpu.execute(1)
            assert setup_cpu.pc != old_pc
            old_pc = setup_cpu.pc
