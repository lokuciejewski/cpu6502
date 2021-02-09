import pytest


class TestNOP:

    @pytest.mark.parametrize('pc', [0x0000, 0x0001, 0x0fff, 0xffff])
    def test_nop_implied(self, setup_cpu, pc):
        setup_cpu.pc = pc
        setup_cpu.memory[setup_cpu.pc] = 0xea  # NOP instruction
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + 2
        assert setup_cpu.clock.total_clock_cycles == 2
