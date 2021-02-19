from unittest.mock import patch

import numpy as np
import pytest

from cpu6502.cpu import CPU
from cpu6502.instructions.instructions import Instructions
from cpu6502.memory import Memory


@pytest.mark.usefixtures('setup_cpu')
class TestCPU:

    @pytest.mark.parametrize('pc_address_fst, pc_address_snd', [(0x0, 0x1), (0x0, 0x0), (0x0, 0xff), (0xff, 0xff)])
    def test_cpu_reset(self, pc_address_fst, pc_address_snd):
        cpu = CPU()
        memory = Memory()
        memory[0xfffc] = pc_address_snd
        memory[0xfffd] = pc_address_fst
        with patch.object(CPU, 'initialise_memory'):
            cpu.memory = memory
            cpu.reset()
        pc_address = pc_address_snd + (pc_address_fst << 8)
        assert cpu.pc == pc_address
        assert cpu.sp == 0xff
        assert cpu.acc == 0x0
        assert cpu.idx == 0x0
        assert cpu.idy == 0x0
        assert not cpu.ps['interrupt_flag']
        assert not cpu.ps['decimal_flag']
        assert cpu.clock.total_clock_cycles == 7

    @pytest.mark.parametrize('ps, result', [({
                                                 'carry_flag': True,
                                                 'zero_flag': True,
                                                 'interrupt_flag': False,
                                                 'decimal_flag': True,
                                                 'break_flag': False,
                                                 'overflow_flag': False,
                                                 'negative_flag': True
                                             }, 0b01101001),
                                            ({
                                                 'carry_flag': False,
                                                 'zero_flag': False,
                                                 'interrupt_flag': False,
                                                 'decimal_flag': False,
                                                 'break_flag': False,
                                                 'overflow_flag': False,
                                                 'negative_flag': False
                                             }, 0b00000000),
                                            ({
                                                 'carry_flag': True,
                                                 'zero_flag': True,
                                                 'interrupt_flag': True,
                                                 'decimal_flag': True,
                                                 'break_flag': True,
                                                 'overflow_flag': True,
                                                 'negative_flag': True
                                             }, 0b01111111)])
    def test_cpu_convert_ps_to_binary(self, setup_cpu, ps, result):
        setup_cpu.ps = ps
        assert setup_cpu.convert_ps_to_binary() == result
        assert setup_cpu.clock.total_clock_cycles == 0

    @pytest.mark.parametrize('result, bin_ps', [({
                                                     'carry_flag': True,
                                                     'zero_flag': True,
                                                     'interrupt_flag': False,
                                                     'decimal_flag': True,
                                                     'break_flag': False,
                                                     'overflow_flag': False,
                                                     'negative_flag': True
                                                 }, 0b01101001),
                                                ({
                                                     'carry_flag': False,
                                                     'zero_flag': False,
                                                     'interrupt_flag': False,
                                                     'decimal_flag': False,
                                                     'break_flag': False,
                                                     'overflow_flag': False,
                                                     'negative_flag': False
                                                 }, 0b00000000),
                                                ({
                                                     'carry_flag': True,
                                                     'zero_flag': True,
                                                     'interrupt_flag': True,
                                                     'decimal_flag': True,
                                                     'break_flag': True,
                                                     'overflow_flag': True,
                                                     'negative_flag': True
                                                 }, 0b01111111)])
    @pytest.mark.parametrize('sp', [0x0, 0xf1, 0xfe])
    def test_cpu_convert_binary_to_ps(self, setup_cpu, result, bin_ps, sp):
        setup_cpu.sp = sp
        setup_cpu.memory[sp + 0x0100] = np.ubyte(bin_ps)
        setup_cpu.convert_binary_to_ps()
        assert setup_cpu.ps == result
        assert setup_cpu.clock.total_clock_cycles == 3

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
        assert setup_cpu.pc == address + 1

    @pytest.mark.parametrize('address', [0x0000, 0xffff, 0x0001, 0xfffe, 0x0e01])
    @pytest.mark.parametrize('value', [0x00, 0x01, 0xff, 0xfe, 0xae])
    def test_cpu_read_byte(self, setup_cpu, address, value):
        pc_start = setup_cpu.pc
        setup_cpu.memory[address] = value
        assert setup_cpu.read_byte(address) == hex(value)
        assert setup_cpu.clock.total_clock_cycles == 1
        assert setup_cpu.pc == pc_start

    @pytest.mark.parametrize('address', [0x0200, 0xffff, 0x0001, 0xfffe, 0x0e01])
    @pytest.mark.parametrize('value', [0x00, 0x01, 0xff, 0xfe, 0xae])
    def test_cpu_write_byte_ok(self, setup_cpu, address, value):
        pc_start = setup_cpu.pc
        setup_cpu.write_byte(address, value)
        assert setup_cpu.memory[address] == value
        assert setup_cpu.clock.total_clock_cycles == 1
        assert setup_cpu.pc == pc_start

    @pytest.mark.parametrize('address', [0x0100, 0x0101, 0x0120, 0x01fe, 0x01ff])
    def test_cpu_write_byte_on_stack(self, setup_cpu, address):
        pc_start = setup_cpu.pc
        setup_cpu.write_byte(address, 0x10)
        assert setup_cpu.memory[address] == 0x0
        assert setup_cpu.clock.total_clock_cycles == 0
        assert setup_cpu.pc == pc_start

    @pytest.mark.parametrize('address', [0x0000, 0xfffe, 0x0001, 0x0e01])
    @pytest.mark.parametrize('value', [0x0100, 0x0010, 0xffff, 0xfeef, 0xefef])
    def test_cpu_fetch_word(self, setup_cpu, address, value):
        setup_cpu.pc = address
        setup_cpu.memory[address] = value
        setup_cpu.memory[address + 1] = value >> 8
        assert setup_cpu.fetch_word() == hex(value)
        assert setup_cpu.clock.total_clock_cycles == 2
        assert setup_cpu.pc == address + 2

    @pytest.mark.parametrize('address', [0x0000, 0x0001, 0xfffe, 0x0e01])
    @pytest.mark.parametrize('value', [0x0100, 0x0010, 0xffff, 0xfeef, 0xefef])
    def test_cpu_read_word(self, setup_cpu, address, value):
        pc_start = setup_cpu.pc
        setup_cpu.memory[address] = value
        setup_cpu.memory[address + 1] = value >> 8
        assert setup_cpu.read_word(address) == hex(value)
        assert setup_cpu.clock.total_clock_cycles == 2
        assert setup_cpu.pc == pc_start

    @pytest.mark.parametrize('address', [0x0000, 0x0001, 0xfffe, 0x0e01])
    @pytest.mark.parametrize('value', [0x0100, 0x0010, 0xffff, 0xfeef, 0xefef])
    def test_cpu_write_word_ok(self, setup_cpu, address, value):
        pc_start = setup_cpu.pc
        setup_cpu.write_word(address, value)
        assert setup_cpu.memory[address] == np.ubyte(value)
        assert setup_cpu.memory[address + 1] == np.ubyte(value >> 8)
        assert setup_cpu.clock.total_clock_cycles == 2
        assert setup_cpu.pc == pc_start

    @pytest.mark.parametrize('address', [0x0100, 0x0101, 0x0120, 0x01fe, 0x01ff])
    def test_cpu_write_word_on_stack(self, setup_cpu, address):
        pc_start = setup_cpu.pc
        setup_cpu.write_word(address, 0xae10)
        assert setup_cpu.memory[address] == 0x0
        assert setup_cpu.clock.total_clock_cycles == 0
        assert setup_cpu.pc == pc_start

    @pytest.mark.parametrize('value', [0x00, 0x01, 0xff, 0xfe, 0xae])
    @pytest.mark.parametrize('sp', [0x01, 0xfe, 0xaa, 0xff])
    def test_cpu_push_byte_on_stack_ok(self, setup_cpu, value, sp):
        pc_start = setup_cpu.pc
        setup_cpu.sp = sp
        setup_cpu.push_byte_on_stack(value)
        assert setup_cpu.memory[sp + 0x0100] == value
        assert setup_cpu.sp == sp - 1
        assert setup_cpu.clock.total_clock_cycles == 2
        assert setup_cpu.pc == pc_start

    def test_cpu_push_byte_on_stack_full(self, setup_cpu):
        pc_start = setup_cpu.pc
        setup_cpu.sp = 0x00
        setup_cpu.push_byte_on_stack(0xab)
        assert setup_cpu.memory[0x0100] == 0x0
        assert setup_cpu.sp == 0x00
        assert setup_cpu.clock.total_clock_cycles == 0
        assert setup_cpu.pc == pc_start

    @pytest.mark.parametrize('value', [0x00, 0x01, 0xff, 0xfe, 0xae])
    @pytest.mark.parametrize('sp', [0xfe, 0x00, 0xaa])
    def test_cpu_pop_byte_from_stack_ok(self, setup_cpu, value, sp):
        pc_start = setup_cpu.pc
        setup_cpu.sp = sp
        setup_cpu.memory[sp + 0x0100] = value
        assert hex(value) == setup_cpu.pull_byte_from_stack()
        assert setup_cpu.sp == sp + 1
        assert setup_cpu.clock.total_clock_cycles == 3
        assert setup_cpu.pc == pc_start

    def test_cpu_pop_byte_from_stack_empty(self, setup_cpu):
        pc_start = setup_cpu.pc
        setup_cpu.sp = 0xff
        assert setup_cpu.pull_byte_from_stack() is None
        assert setup_cpu.sp == 0xff
        assert setup_cpu.clock.total_clock_cycles == 0
        assert setup_cpu.pc == pc_start

    @pytest.mark.parametrize('value', [0x0100, 0x0010, 0xffee, 0xeeff, 0xefef, 0xfefe])
    @pytest.mark.parametrize('sp', [0xff, 0x02, 0xfd, 0xaa])
    def test_cpu_push_word_on_stack_ok(self, setup_cpu, value, sp):
        pc_start = setup_cpu.pc
        setup_cpu.sp = sp
        setup_cpu.push_word_on_stack(value)
        assert setup_cpu.memory[setup_cpu.sp + 0x0102] == np.ubyte(value)
        assert setup_cpu.memory[setup_cpu.sp + 0x0101] == np.ubyte(value >> 8)
        assert setup_cpu.sp == sp - 2
        assert setup_cpu.clock.total_clock_cycles == 3
        assert setup_cpu.pc == pc_start

    @pytest.mark.parametrize('sp', [0x00, 0x01])
    def test_cpu_push_word_on_stack_full(self, setup_cpu, sp):
        pc_start = setup_cpu.pc
        setup_cpu.sp = sp
        setup_cpu.push_word_on_stack(0xabcd)
        assert setup_cpu.memory[sp + 0x0100] == 0x0
        assert setup_cpu.sp == sp
        assert setup_cpu.clock.total_clock_cycles == 0
        assert setup_cpu.pc == pc_start

    @pytest.mark.parametrize('value', [0x0100, 0x0010, 0xffee, 0xeeff, 0xefef, 0xfefe])
    @pytest.mark.parametrize('sp', [0x01, 0xfd, 0xaa, 0xfd])
    def test_cpu_pop_word_from_stack_ok(self, setup_cpu, value, sp):
        pc_start = setup_cpu.pc
        setup_cpu.sp = sp
        setup_cpu.memory[setup_cpu.sp + 0x0102] = np.ubyte(value)
        setup_cpu.memory[setup_cpu.sp + 0x0101] = np.ubyte(value >> 8)
        assert hex(value) == setup_cpu.pull_word_from_stack()
        assert setup_cpu.sp == sp + 2
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.pc == pc_start

    @pytest.mark.parametrize('sp', [0xff, 0xfe])
    def test_cpu_pop_word_from_stack_empty(self, setup_cpu, sp):
        pc_start = setup_cpu.pc
        setup_cpu.sp = sp
        assert setup_cpu.pull_word_from_stack() is None
        assert setup_cpu.sp == sp
        assert setup_cpu.clock.total_clock_cycles == 0
        assert setup_cpu.pc == pc_start
