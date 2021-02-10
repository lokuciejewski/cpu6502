from unittest.mock import patch

import pytest

from cpu6502.cpu import CPU
from cpu6502.memory import Memory


@pytest.mark.usefixtures('setup_cpu')
class TestNOP:

    @pytest.mark.parametrize('pc', [0x0000, 0x0001, 0x0fff, 0xffff])
    def test_nop_implied(self, setup_cpu, pc):
        setup_cpu.pc = pc
        setup_cpu.memory[setup_cpu.pc] = 0xea  # NOP instruction
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + 2
        assert setup_cpu.clock.total_clock_cycles == 2


class TestRES:

    def test_res_implied(self):
        cpu = CPU()
        with patch.object(CPU, 'reset') as mocked_reset:
            cpu.pc = 0x0200
            cpu.memory = Memory()
            cpu.memory[0x0200] = 0xbb  # RES
            cpu.execute(1)
            assert mocked_reset.called_once()
