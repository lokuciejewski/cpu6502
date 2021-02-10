import numpy as np
import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestSTA:

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    @pytest.mark.parametrize('zp_address', [0x0, 0x1, 0xfe, 0xff])
    def test_sta_zero_page(self, setup_cpu, value, zp_address):
        setup_cpu.acc = value
        setup_cpu.memory[0x0200] = 0x85  # STA instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.execute(1)
        assert setup_cpu.memory[zp_address] == value
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    @pytest.mark.parametrize('zp_address', [0x0, 0x1, 0xf0, 0xf0])
    @pytest.mark.parametrize('idx', [0x00, 0x01, 0x0f, 0x0e])
    def test_sta_zero_page_x(self, setup_cpu, value, zp_address, idx):
        setup_cpu.acc = value
        setup_cpu.idx = idx
        setup_cpu.memory[0x0200] = 0x95  # STA instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.execute(1)
        assert setup_cpu.memory[np.ubyte(zp_address + idx)] == value
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x00, 0x01), (0x02, 0xee), (0xfa, 0xa1)])
    def test_sta_absolute(self, setup_cpu, value, address_snd, address_fst):
        setup_cpu.acc = value
        setup_cpu.memory[0x0200] = 0x8d  # STA instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        setup_cpu.execute(1)
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        assert setup_cpu.memory[address] == value
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x00, 0x01), (0x02, 0xee), (0xfa, 0xa1)])
    @pytest.mark.parametrize('idx', [0x00, 0x01, 0x0f, 0x0e])
    def test_sta_absolute_x(self, setup_cpu, value, address_snd, address_fst, idx):
        setup_cpu.acc = value
        setup_cpu.idx = idx
        setup_cpu.memory[0x0200] = 0x9d  # STA instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        setup_cpu.execute(1)
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        assert setup_cpu.memory[address + idx] == value
        assert setup_cpu.clock.total_clock_cycles == 5

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x00, 0x01), (0x02, 0xee), (0xfa, 0xa1)])
    @pytest.mark.parametrize('idy', [0x00, 0x01, 0x0f, 0x0e])
    def test_sta_absolute_y(self, setup_cpu, value, address_snd, address_fst, idy):
        setup_cpu.acc = value
        setup_cpu.idy = idy
        setup_cpu.memory[0x0200] = 0x99  # STA instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        setup_cpu.execute(1)
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        assert setup_cpu.memory[address + idy] == value
        assert setup_cpu.clock.total_clock_cycles == 5

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    @pytest.mark.parametrize('zp_address', [0x1, 0x0, 0xff])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x00, 0x01), (0x02, 0xee), (0xfa, 0xa1)])
    @pytest.mark.parametrize('idx', [0x00, 0x01, 0x0f, 0x0e])
    def test_sta_indexed_indirect(self, setup_cpu, value, address_snd, address_fst, idx, zp_address):
        setup_cpu.memory[0x0200] = 0x81  # STA instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.idx = idx
        setup_cpu.acc = value
        address = np.ubyte(zp_address + setup_cpu.idx)
        setup_cpu.memory[address] = address_snd
        setup_cpu.memory[address + 1] = address_fst
        target_address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.execute(1)
        assert setup_cpu.memory[target_address] == value
        assert setup_cpu.clock.total_clock_cycles == 6

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    @pytest.mark.parametrize('zp_address', [0x1, 0x0, 0xff])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x00, 0x01), (0x02, 0xee), (0xfa, 0xa1)])
    @pytest.mark.parametrize('idy', [0x00, 0x01, 0x0f, 0x0e])
    def test_sta_indirect_indexed(self, setup_cpu, value, address_snd, address_fst, idy, zp_address):
        setup_cpu.memory[0x0200] = 0x91  # STA instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.idy = idy
        setup_cpu.acc = value
        setup_cpu.memory[zp_address] = address_snd
        setup_cpu.memory[zp_address + 1] = address_fst
        target_address = address_snd + (address_fst << 8) + setup_cpu.idy
        setup_cpu.execute(1)
        assert setup_cpu.memory[target_address] == value
        assert setup_cpu.clock.total_clock_cycles == 6


@pytest.mark.usefixtures('setup_cpu')
class TestSTX:

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    @pytest.mark.parametrize('zp_address', [0x0, 0x1, 0xfe, 0xff])
    def test_stx_zero_page(self, setup_cpu, value, zp_address):
        setup_cpu.idx = value
        setup_cpu.memory[0x0200] = 0x86  # STX instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.execute(1)
        assert setup_cpu.memory[zp_address] == value
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    @pytest.mark.parametrize('zp_address', [0x0, 0x1, 0xf0, 0xf0])
    @pytest.mark.parametrize('idy', [0x00, 0x01, 0x0f, 0x0e])
    def test_stx_zero_page_y(self, setup_cpu, value, zp_address, idy):
        setup_cpu.idx = value
        setup_cpu.idy = idy
        setup_cpu.memory[0x0200] = 0x96  # STX instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.execute(1)
        assert setup_cpu.memory[zp_address + idy] == value
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x00, 0x01), (0x02, 0xee), (0xfa, 0xa1)])
    def test_stx_absolute(self, setup_cpu, value, address_snd, address_fst):
        setup_cpu.idx = value
        setup_cpu.memory[0x0200] = 0x8e  # STX instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        setup_cpu.execute(1)
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        assert setup_cpu.memory[address] == value
        assert setup_cpu.clock.total_clock_cycles == 4


@pytest.mark.usefixtures('setup_cpu')
class TestSTY:

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    @pytest.mark.parametrize('zp_address', [0x0, 0x1, 0xfe, 0xff])
    def test_sty_zero_page(self, setup_cpu, value, zp_address):
        setup_cpu.idy = value
        setup_cpu.memory[0x0200] = 0x84  # STY instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.execute(1)
        assert setup_cpu.memory[zp_address] == value
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    @pytest.mark.parametrize('zp_address', [0x0, 0x1, 0xf0, 0xf0])
    @pytest.mark.parametrize('idx', [0x00, 0x01, 0x0f, 0x0e])
    def test_sty_zero_page_x(self, setup_cpu, value, zp_address, idx):
        setup_cpu.idy = value
        setup_cpu.idx = idx
        setup_cpu.memory[0x0200] = 0x94  # STY instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.execute(1)
        assert setup_cpu.memory[np.ubyte(zp_address + idx)] == value
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x00, 0x01), (0x02, 0xee), (0xfa, 0xa1)])
    def test_sty_absolute(self, setup_cpu, value, address_snd, address_fst):
        setup_cpu.idy = value
        setup_cpu.memory[0x0200] = 0x8c  # STY instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        setup_cpu.execute(1)
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        assert setup_cpu.memory[address] == value
        assert setup_cpu.clock.total_clock_cycles == 4
