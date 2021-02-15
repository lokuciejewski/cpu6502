import numpy as np
import pytest

from cpu6502.instructions import AbstractInstruction


@pytest.mark.usefixtures('setup_cpu')
class TestAddressing:

    @pytest.mark.parametrize('address', [0x0, 0xff01, 0xffff, 0x01, 0x0101])
    @pytest.mark.parametrize('value', [0x0, 0xff, 0x01])
    def test_immediate(self, setup_cpu, address, value):
        setup_cpu.pc = address
        setup_cpu.memory[address] = value
        addressing = AbstractInstruction(setup_cpu)
        assert addressing.immediate() == value
        assert setup_cpu.clock.total_clock_cycles == 1

    @pytest.mark.parametrize('address', [0x0, 0xff01, 0xffff, 0x01, 0x0101])
    @pytest.mark.parametrize('value', [0x0, 0xff, 0x01])
    def test_zero_page(self, setup_cpu, address, value):
        setup_cpu.pc = address
        setup_cpu.memory[address] = value
        addressing = AbstractInstruction(setup_cpu)
        assert addressing.zero_page() == value
        assert setup_cpu.clock.total_clock_cycles == 1

    @pytest.mark.parametrize('address', [0x0, 0xff01, 0xffff, 0x01, 0x0101])
    @pytest.mark.parametrize('zp_address', [0x0, 0x01, 0xff, 0xe1])
    @pytest.mark.parametrize('idx', [0x0, 0xff, 0x10])
    def test_zero_page_x(self, setup_cpu, zp_address, idx, address):
        setup_cpu.pc = address
        setup_cpu.idx = idx
        setup_cpu.memory[address] = zp_address
        addressing = AbstractInstruction(setup_cpu)
        assert addressing.zero_page_x() == np.ubyte(zp_address + idx)
        assert setup_cpu.clock.total_clock_cycles == 1

    @pytest.mark.parametrize('address', [0x0, 0xff01, 0xffff, 0x01, 0x0101])
    @pytest.mark.parametrize('zp_address', [0x0, 0x01, 0xff, 0xe1])
    @pytest.mark.parametrize('idy', [0x0, 0xff, 0x10])
    def test_zero_page_y(self, setup_cpu, zp_address, idy, address):
        setup_cpu.pc = address
        setup_cpu.idy = idy
        setup_cpu.memory[address] = zp_address
        addressing = AbstractInstruction(setup_cpu)
        assert addressing.zero_page_y() == np.ubyte(zp_address + idy)
        assert setup_cpu.clock.total_clock_cycles == 1

    @pytest.mark.parametrize('address', [0x0, 0xff01, 0xfffe, 0x01, 0x0101])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x0), (0x0, 0x1), (0xff, 0xff), (0xab, 0xdc)])
    def test_absolute(self, setup_cpu, address_fst, address_snd, address):
        setup_cpu.pc = address
        setup_cpu.memory[address] = address_snd
        setup_cpu.memory[address + 1] = address_fst
        expected_address = address_snd + (address_fst << 8)
        addressing = AbstractInstruction(setup_cpu)
        assert expected_address == addressing.absolute()
        assert setup_cpu.clock.total_clock_cycles == 2

    @pytest.mark.parametrize('address', [0x0, 0xff01, 0xfffe, 0x01, 0x0101])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x0), (0x0, 0x1), (0xfe, 0xaf), (0xab, 0xdc)])
    @pytest.mark.parametrize('idx', [0x0, 0x01, 0x10])
    def test_absolute_x_no_page_crossed(self, setup_cpu, address_fst, address_snd, address, idx):
        setup_cpu.pc = address
        setup_cpu.idx = idx
        setup_cpu.memory[address] = address_snd
        setup_cpu.memory[address + 1] = address_fst
        expected_address = (address_snd + (address_fst << 8)) + idx
        addressing = AbstractInstruction(setup_cpu)
        assert expected_address == addressing.absolute_x()
        assert setup_cpu.clock.total_clock_cycles == 2

    @pytest.mark.parametrize('address', [0x0, 0xff01, 0xfffe, 0x01, 0x0101])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0xfe), (0x0, 0xaa), (0xfe, 0xaf), (0xab, 0xdc)])
    @pytest.mark.parametrize('idx', [0xf1, 0xff, 0xfa])
    def test_absolute_x_page_crossed(self, setup_cpu, address_fst, address_snd, address, idx):
        setup_cpu.pc = address
        setup_cpu.idx = idx
        setup_cpu.memory[address] = address_snd
        setup_cpu.memory[address + 1] = address_fst
        expected_address = (address_snd + (address_fst << 8)) + idx
        addressing = AbstractInstruction(setup_cpu)
        assert expected_address == addressing.absolute_x()
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('address', [0x0, 0xff01, 0xfffe, 0x01, 0x0101])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x0), (0x0, 0x1), (0xfe, 0xaf), (0xab, 0xdc)])
    @pytest.mark.parametrize('idy', [0x0, 0x01, 0x10])
    def test_absolute_y_no_page_crossed(self, setup_cpu, address_fst, address_snd, address, idy):
        setup_cpu.pc = address
        setup_cpu.idy = idy
        setup_cpu.memory[address] = address_snd
        setup_cpu.memory[address + 1] = address_fst
        expected_address = (address_snd + (address_fst << 8)) + idy
        addressing = AbstractInstruction(setup_cpu)
        assert expected_address == addressing.absolute_y()
        assert setup_cpu.clock.total_clock_cycles == 2

    @pytest.mark.parametrize('address', [0x0, 0xff01, 0xfffe, 0x01, 0x0101])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0xfe), (0x0, 0xaa), (0xfe, 0xaf), (0xab, 0xdc)])
    @pytest.mark.parametrize('idy', [0xf1, 0xff, 0xfa])
    def test_absolute_y_page_crossed(self, setup_cpu, address_fst, address_snd, address, idy):
        setup_cpu.pc = address
        setup_cpu.idy = idy
        setup_cpu.memory[address] = address_snd
        setup_cpu.memory[address + 1] = address_fst
        expected_address = (address_snd + (address_fst << 8)) + idy
        addressing = AbstractInstruction(setup_cpu)
        assert expected_address == addressing.absolute_y()
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('address', [0x2a1, 0xff01, 0xfffe, 0xa01, 0x0101])
    @pytest.mark.parametrize('zp_address', [0x0, 0xfe, 0xaa, 0xaf, 0xab, 0xdc])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x01), (0x20, 0xaa), (0xfe, 0xaf), (0xab, 0xdc)])
    @pytest.mark.parametrize('idx', [0x01, 0xff, 0x2a])
    def test_indexed_indirect(self, setup_cpu, zp_address, address, idx, address_fst, address_snd):
        setup_cpu.pc = address
        setup_cpu.idx = idx
        setup_cpu.memory[address] = zp_address
        target_address = np.ubyte(zp_address + idx)
        setup_cpu.memory[target_address] = address_snd
        setup_cpu.memory[target_address + 1] = address_fst
        expected_address = address_snd + (address_fst << 8)
        addressing = AbstractInstruction(setup_cpu)
        assert expected_address == addressing.indexed_indirect()
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('address', [0x2a1, 0xff01, 0xfffe, 0xa01, 0x0101])
    @pytest.mark.parametrize('zp_address', [0x0, 0xfe, 0xaa, 0xaf, 0xab, 0xdc])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x01), (0x20, 0xaa), (0xfe, 0xaf), (0xab, 0xdc)])
    @pytest.mark.parametrize('idy', [0x01, 0x0, 0x10])
    def test_indirect_indexed_no_page_crossed(self, setup_cpu, zp_address, address, idy, address_fst, address_snd):
        setup_cpu.pc = address
        setup_cpu.idy = idy
        setup_cpu.memory[address] = zp_address
        setup_cpu.memory[zp_address] = address_snd
        setup_cpu.memory[zp_address + 1] = address_fst
        expected_address = (address_snd + (address_fst << 8)) + idy
        addressing = AbstractInstruction(setup_cpu)
        assert expected_address == addressing.indirect_indexed()
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('address', [0x2a1, 0xff01, 0xfffe, 0xa01, 0x0101])
    @pytest.mark.parametrize('zp_address', [0x0, 0xfe, 0xaa, 0xaf, 0xab, 0xdc])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x21), (0x20, 0xaa), (0xfe, 0xaf), (0xab, 0xdc)])
    @pytest.mark.parametrize('idy', [0xff, 0xfe])
    def test_indirect_indexed_page_crossed(self, setup_cpu, zp_address, address, idy, address_fst, address_snd):
        setup_cpu.pc = address
        setup_cpu.idy = idy
        setup_cpu.memory[address] = zp_address
        setup_cpu.memory[zp_address] = address_snd
        setup_cpu.memory[zp_address + 1] = address_fst
        expected_address = (address_snd + (address_fst << 8)) + idy
        addressing = AbstractInstruction(setup_cpu)
        assert expected_address == addressing.indirect_indexed()
        assert setup_cpu.clock.total_clock_cycles == 4
