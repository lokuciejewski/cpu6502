import numpy as np
import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestAND:

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    def test_and_immediate(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x29  # AND instruction
        setup_cpu.memory[0x0201] = value
        setup_cpu.acc = acc
        expected_value = acc & value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 2
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('zp_address', [0x0, 0x1, 0xff])
    def test_and_zero_page(self, setup_cpu, acc, value, zp_address):
        setup_cpu.memory[0x0200] = 0x25  # AND instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.memory[zp_address] = value
        setup_cpu.acc = acc
        expected_value = acc & value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 3
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('zp_address', [0x0, 0x1, 0xff])
    @pytest.mark.parametrize('idx', [0x0, 0x1, 0xff])
    def test_and_zero_page_x(self, setup_cpu, acc, value, zp_address, idx):
        setup_cpu.memory[0x0200] = 0x35  # AND instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.idx = idx
        setup_cpu.memory[np.ubyte(zp_address + setup_cpu.idx)] = value
        setup_cpu.acc = acc
        expected_value = acc & value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x0), (0xff, 0xff), (0x2a, 0x1c)])
    def test_and_absolute(self, setup_cpu, acc, value, address_fst, address_snd):
        setup_cpu.memory[0x0200] = 0x2d  # AND instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address] = value
        setup_cpu.acc = acc
        expected_value = acc & value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x0), (0xff, 0xaa), (0x2a, 0x1c)])
    @pytest.mark.parametrize('idx', [0x0, 0x1, 0x10])
    def test_and_absolute_x_no_page_crossed(self, setup_cpu, acc, value, idx, address_fst, address_snd):
        setup_cpu.memory[0x0200] = 0x3d  # AND instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        setup_cpu.idx = idx
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idx] = value
        setup_cpu.acc = acc
        expected_value = acc & value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0xaa), (0x2a, 0x1c)])
    @pytest.mark.parametrize('idx', [0xff, 0xfe])
    def test_and_absolute_x_page_crossed(self, setup_cpu, acc, value, idx, address_fst, address_snd):
        setup_cpu.memory[0x0200] = 0x3d  # AND instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        setup_cpu.idx = idx
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idx] = value
        setup_cpu.acc = acc
        expected_value = acc & value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 5
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x0), (0xff, 0x10), (0x2a, 0x1c)])
    @pytest.mark.parametrize('idy', [0x0, 0x1, 0xa1])
    def test_and_absolute_y_no_page_crossed(self, setup_cpu, acc, value, idy, address_fst, address_snd):
        setup_cpu.memory[0x0200] = 0x39  # AND instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        setup_cpu.idy = idy
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idy] = value
        setup_cpu.acc = acc
        expected_value = acc & value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0xaa), (0xfa, 0xde), (0x2a, 0x1c)])
    @pytest.mark.parametrize('idy', [0xff, 0xfe])
    def test_and_absolute_y_page_crossed(self, setup_cpu, acc, value, idy, address_fst, address_snd):
        setup_cpu.memory[0x0200] = 0x39  # AND instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        setup_cpu.idy = idy
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idy] = value
        setup_cpu.acc = acc
        expected_value = acc & value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 5
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address', [0x0, 0xaa, 0xff])
    @pytest.mark.parametrize('idx', [0xff, 0xfe])
    @pytest.mark.parametrize('zp_address', [0xff, 0x01, 0x00, 0xab])
    def test_and_indexed_indirect(self, setup_cpu, acc, value, address, idx, zp_address):
        setup_cpu.memory[0x0200] = 0x21  # AND instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.memory[zp_address] = address
        setup_cpu.idx = idx
        setup_cpu.memory[np.ubyte(address + setup_cpu.idx)] = value
        setup_cpu.acc = acc
        expected_value = acc & value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 6
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0xaa), (0xff, 0xaa), (0x2a, 0x1c)])
    @pytest.mark.parametrize('idy', [0x01, 0x00])
    @pytest.mark.parametrize('zp_address', [0xff, 0x01, 0x00, 0xab])
    def test_and_indirect_indexed_no_page_crossed(self, setup_cpu, acc, value, address_fst, address_snd, idy,
                                                  zp_address):
        setup_cpu.memory[0x0200] = 0x31  # AND instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.memory[zp_address] = address_snd
        setup_cpu.memory[zp_address + 1] = address_fst
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idy] = value
        setup_cpu.idy = idy
        setup_cpu.acc = acc
        expected_value = acc & value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 5
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0xaa), (0xff, 0xaa), (0x2a, 0x1c)])
    @pytest.mark.parametrize('idy', [0xff, 0xfe])
    @pytest.mark.parametrize('zp_address', [0xff, 0x01, 0x00, 0xab])
    def test_and_indirect_indexed_page_crossed(self, setup_cpu, acc, value, address_fst, address_snd, idy,
                                               zp_address):
        setup_cpu.memory[0x0200] = 0x31  # AND instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.memory[zp_address] = address_snd
        setup_cpu.memory[zp_address + 1] = address_fst
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idy] = value
        setup_cpu.idy = idy
        setup_cpu.acc = acc
        expected_value = acc & value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 6
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag


@pytest.mark.usefixtures('setup_cpu')
class TestEOR:

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    def test_eor_immediate(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x49  # EOR instruction
        setup_cpu.memory[0x0201] = value
        setup_cpu.acc = acc
        expected_value = acc ^ value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 2
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('zp_address', [0x0, 0x1, 0xff])
    def test_eor_zero_page(self, setup_cpu, acc, value, zp_address):
        setup_cpu.memory[0x0200] = 0x45  # EOR instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.memory[zp_address] = value
        setup_cpu.acc = acc
        expected_value = acc ^ value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 3
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('zp_address', [0x0, 0x1, 0xff])
    @pytest.mark.parametrize('idx', [0x0, 0x1, 0xff])
    def test_eor_zero_page_x(self, setup_cpu, acc, value, zp_address, idx):
        setup_cpu.memory[0x0200] = 0x55  # EOR instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.idx = idx
        setup_cpu.memory[np.ubyte(zp_address + setup_cpu.idx)] = value
        setup_cpu.acc = acc
        expected_value = acc ^ value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x0), (0xff, 0xff), (0x2a, 0x1c)])
    def test_eor_absolute(self, setup_cpu, acc, value, address_fst, address_snd):
        setup_cpu.memory[0x0200] = 0x4d  # EOR instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address] = value
        setup_cpu.acc = acc
        expected_value = acc ^ value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x0), (0xfa, 0xaa), (0x2a, 0x1c)])
    @pytest.mark.parametrize('idx', [0x0, 0x1, 0xa1])
    def test_eor_absolute_x_no_page_crossed(self, setup_cpu, acc, value, idx, address_fst, address_snd):
        setup_cpu.memory[0x0200] = 0x5d  # EOR instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        setup_cpu.idx = idx
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idx] = value
        setup_cpu.acc = acc
        expected_value = acc ^ value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0xaa), (0xfa, 0xaa), (0x2a, 0x1c)])
    @pytest.mark.parametrize('idx', [0xff, 0xfe])
    def test_eor_absolute_x_page_crossed(self, setup_cpu, acc, value, idx, address_fst, address_snd):
        setup_cpu.memory[0x0200] = 0x5d  # EOR instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        setup_cpu.idx = idx
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idx] = value
        setup_cpu.acc = acc
        expected_value = acc ^ value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 5
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x0), (0xfa, 0xaa), (0x2a, 0x1c)])
    @pytest.mark.parametrize('idy', [0x0, 0x1, 0xa1])
    def test_eor_absolute_y_no_page_crossed(self, setup_cpu, acc, value, idy, address_fst, address_snd):
        setup_cpu.memory[0x0200] = 0x59  # EOR instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        setup_cpu.idy = idy
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idy] = value
        setup_cpu.acc = acc
        expected_value = acc ^ value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0xaa), (0xfa, 0xaa), (0x2a, 0x1c)])
    @pytest.mark.parametrize('idy', [0xff, 0xfe])
    def test_eor_absolute_y_page_crossed(self, setup_cpu, acc, value, idy, address_fst, address_snd):
        setup_cpu.memory[0x0200] = 0x59  # EOR instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        setup_cpu.idy = idy
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idy] = value
        setup_cpu.acc = acc
        expected_value = acc ^ value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 5
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address', [0x0, 0xff, 0x01])
    @pytest.mark.parametrize('idx', [0xff, 0xfe])
    @pytest.mark.parametrize('zp_address', [0xff, 0x00, 0xab])
    def test_eor_indexed_indirect(self, setup_cpu, acc, value, address, idx, zp_address):
        setup_cpu.memory[0x0200] = 0x41  # EOR instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.memory[zp_address] = address
        setup_cpu.idx = idx
        setup_cpu.memory[np.ubyte(address + setup_cpu.idx)] = value
        setup_cpu.acc = acc
        expected_value = acc ^ value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 6
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb22])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0xaa), (0xff, 0xaa), (0x2a, 0x1c)])
    @pytest.mark.parametrize('idy', [0x01, 0x00])
    @pytest.mark.parametrize('zp_address', [0xff, 0x01, 0x00, 0xab])
    def test_eor_indirect_indexed_no_page_crossed(self, setup_cpu, acc, value, address_fst, address_snd, idy,
                                                  zp_address):
        setup_cpu.memory[0x0200] = 0x51  # EOR instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.memory[zp_address] = address_snd
        setup_cpu.memory[zp_address + 1] = address_fst
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idy] = value
        setup_cpu.idy = idy
        setup_cpu.acc = acc
        expected_value = acc ^ value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 5
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0xaa), (0xff, 0xaa), (0x2a, 0x1c)])
    @pytest.mark.parametrize('idy', [0xff, 0xfe])
    @pytest.mark.parametrize('zp_address', [0xff, 0x01, 0x00, 0xab])
    def test_eor_indirect_indexed_page_crossed(self, setup_cpu, acc, value, address_fst, address_snd, idy,
                                               zp_address):
        setup_cpu.memory[0x0200] = 0x51  # EOR instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.memory[zp_address] = address_snd
        setup_cpu.memory[zp_address + 1] = address_fst
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idy] = value
        setup_cpu.idy = idy
        setup_cpu.acc = acc
        expected_value = acc ^ value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 6
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag


@pytest.mark.usefixtures('setup_cpu')
class TestORA:

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0])
    def test_ora_immediate(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x09  # ORA instruction
        setup_cpu.memory[0x0201] = value
        setup_cpu.acc = acc
        expected_value = acc | value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 2
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0])
    @pytest.mark.parametrize('zp_address', [0x0, 0x1, 0xff, 0xba])
    def test_ora_zero_page(self, setup_cpu, acc, value, zp_address):
        setup_cpu.memory[0x0200] = 0x05  # ORA instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.memory[zp_address] = value
        setup_cpu.acc = acc
        expected_value = acc | value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 3
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0])
    @pytest.mark.parametrize('zp_address', [0x0, 0x1, 0xff])
    @pytest.mark.parametrize('idx', [0x0, 0x1, 0xff, 0xaa])
    def test_ora_zero_page_x(self, setup_cpu, acc, value, zp_address, idx):
        setup_cpu.memory[0x0200] = 0x15  # ORA instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.idx = idx
        setup_cpu.memory[np.ubyte(zp_address + setup_cpu.idx)] = value
        setup_cpu.acc = acc
        expected_value = acc | value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x0), (0xff, 0xff), (0x2a, 0x1c)])
    def test_ora_absolute(self, setup_cpu, acc, value, address_fst, address_snd):
        setup_cpu.memory[0x0200] = 0x0d  # ORA instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address] = value
        setup_cpu.acc = acc
        expected_value = acc | value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x0), (0xff, 0xaa), (0x2a, 0x1c)])
    @pytest.mark.parametrize('idx', [0x0, 0x1, 0xa1])
    def test_ora_absolute_x_no_page_crossed(self, setup_cpu, acc, value, idx, address_fst, address_snd):
        setup_cpu.memory[0x0200] = 0x1d  # ORA instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        setup_cpu.idx = idx
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idx] = value
        setup_cpu.acc = acc
        expected_value = acc | value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0xaa), (0xff, 0xaa), (0x2a, 0x1c)])
    @pytest.mark.parametrize('idx', [0xff, 0xfe])
    def test_ora_absolute_x_page_crossed(self, setup_cpu, acc, value, idx, address_fst, address_snd):
        setup_cpu.memory[0x0200] = 0x1d  # ORA instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        setup_cpu.idx = idx
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idx] = value
        setup_cpu.acc = acc
        expected_value = acc & value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 5
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x0), (0xff, 0xaa), (0x2a, 0x1c)])
    @pytest.mark.parametrize('idy', [0x0, 0x1, 0xa1])
    def test_ora_absolute_y_no_page_crossed(self, setup_cpu, acc, value, idy, address_fst, address_snd):
        setup_cpu.memory[0x0200] = 0x19  # ORA instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        setup_cpu.idy = idy
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idy] = value
        setup_cpu.acc = acc
        expected_value = acc | value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0xaa), (0xff, 0xaa), (0x2a, 0x1c)])
    @pytest.mark.parametrize('idy', [0xff, 0xfe])
    def test_ora_absolute_y_page_crossed(self, setup_cpu, acc, value, idy, address_fst, address_snd):
        setup_cpu.memory[0x0200] = 0x19  # ORA instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        setup_cpu.idy = idy
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idy] = value
        setup_cpu.acc = acc
        expected_value = acc  | value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 5
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address', [0x0, 0xaa, 0xff])
    @pytest.mark.parametrize('idx', [0xff, 0xfe])
    @pytest.mark.parametrize('zp_address', [0xff, 0x01, 0x00, 0xab])
    def test_ora_indexed_indirect(self, setup_cpu, acc, value, address, idx, zp_address):
        setup_cpu.memory[0x0200] = 0x01  # ORA instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.memory[zp_address] = address
        setup_cpu.idx = idx
        setup_cpu.memory[np.ubyte(address + setup_cpu.idx)] = value
        setup_cpu.acc = acc
        expected_value = acc | value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 6
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0xaa), (0xff, 0xaa), (0x2a, 0x1c)])
    @pytest.mark.parametrize('idy', [0x01, 0x00, 0x02])
    @pytest.mark.parametrize('zp_address', [0xff, 0x01, 0x00, 0xab])
    def test_ora_indirect_indexed_no_page_crossed(self, setup_cpu, acc, value, address_fst, address_snd, idy,
                                                  zp_address):
        setup_cpu.memory[0x0200] = 0x11  # ORA instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.memory[zp_address] = address_snd
        setup_cpu.memory[zp_address + 1] = address_fst
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idy] = value
        setup_cpu.idy = idy
        setup_cpu.acc = acc
        expected_value = acc | value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 5
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0xaa), (0xff, 0xaa), (0x2a, 0x1c)])
    @pytest.mark.parametrize('idy', [0xff, 0xfe])
    @pytest.mark.parametrize('zp_address', [0xff, 0x01, 0x00, 0xab])
    def test_ora_indirect_indexed_page_crossed(self, setup_cpu, acc, value, address_fst, address_snd, idy,
                                               zp_address):
        setup_cpu.memory[0x0200] = 0x11  # ORA instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.memory[zp_address] = address_snd
        setup_cpu.memory[zp_address + 1] = address_fst
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idy] = value
        setup_cpu.idy = idy
        setup_cpu.acc = acc
        expected_value = acc | value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 6
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag


@pytest.mark.usefixtures('setup_cpu')
class TestBIT:

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    @pytest.mark.parametrize('zp_address', [0xff, 0x01, 0x00, 0xab])
    def test_bit_zero_page(self, setup_cpu, acc, value, zp_address):
        setup_cpu.memory[0x0200] = 0x24  # BIT instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.memory[zp_address] = value
        setup_cpu.acc = acc
        expected_zero_flag = ((value & acc) == 0)
        expected_overflow_flag = (value & 0b01000000)
        expected_negative_flag = (value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xa2, 0xf1])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2, 0xf2])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0xaa), (0x0, 0xb1), (0xff, 0xaa), (0x2a, 0x1c)])
    def test_bit_absolute(self, setup_cpu, acc, value, address_fst, address_snd):
        setup_cpu.memory[0x0200] = 0x2c  # BIT instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address] = value
        setup_cpu.acc = acc
        expected_zero_flag = ((value & acc) == 0)
        expected_overflow_flag = (value & 0b01000000)
        expected_negative_flag = (value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 4
