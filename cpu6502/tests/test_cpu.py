from unittest.mock import patch

import pytest

from cpu6502.cpu import CPU, Instructions


@pytest.mark.usefixtures('setup_cpu')
class TestCPU:

    def test_cpu_reset(self):
        cpu = CPU()
        cpu.reset()
        assert cpu.pc == 0xfffc
        assert cpu.sp == 0x0100
        assert cpu.acc == 0x0
        assert cpu.idx == 0x0
        assert cpu.idy == 0x0
        assert not cpu.ps['interrupt_disable']
        assert not cpu.ps['decimal_mode']

    @pytest.mark.parametrize('num_of_instructions', [0, 1, 2, 5])
    def test_cpu_execute(self, setup_cpu, num_of_instructions):
        with patch.object(Instructions, 'execute') as mocked_exec, \
                patch.object(CPU, 'fetch_byte') as mocked_fetch:
            setup_cpu.execute(num_of_instructions)
            assert mocked_exec.call_count == num_of_instructions
            assert mocked_fetch.call_count == num_of_instructions

    @pytest.mark.parametrize('address', [0x0000, 0xffff, 0x0001, 0xfffe, 0x0e01])
    @pytest.mark.parametrize('value', [0x00, 0x01, 0xff, 0xfe, 0xae])
    def test_cpu_fetch_byte(self, setup_cpu, address, value):
        setup_cpu.pc = address
        setup_cpu.memory[address] = value
        assert setup_cpu.fetch_byte() == hex(value)
        assert setup_cpu.clock.total_clock_cycles == 1

    @pytest.mark.parametrize('address', [0x0000, 0xffff, 0x0001, 0xfffe, 0x0e01])
    @pytest.mark.parametrize('value', [0x00, 0x01, 0xff, 0xfe, 0xae])
    def test_cpu_read_byte(self, setup_cpu, address, value):
        setup_cpu.memory[address] = value
        assert setup_cpu.read_byte(address) == hex(value)
        assert setup_cpu.clock.total_clock_cycles == 1


