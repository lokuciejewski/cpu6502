from unittest.mock import patch

from cpu6502.cpu import CPU
from cpu6502.memory import Memory


class TestRES:

    def test_res_implied(self):
        cpu = CPU()
        with patch.object(CPU, 'reset') as mocked_reset:
            cpu.pc = 0x0200
            cpu.memory = Memory()
            cpu.memory[0x0200] = 0xbb  # RES
            assert mocked_reset.called_once()
