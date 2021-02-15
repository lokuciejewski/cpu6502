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
    def test_and_zero_page(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x25  # AND instruction
        setup_cpu.memory[0x0201] = 0xee
        setup_cpu.memory[0xee] = value
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
    def test_and_zero_page_x(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x35  # AND instruction
        setup_cpu.memory[0x0201] = 0xee
        setup_cpu.idx = 0x05
        setup_cpu.memory[0xee + 0x05] = value
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
    def test_and_absolute(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x2d  # AND instruction
        setup_cpu.memory[0x0201] = 0x69
        setup_cpu.memory[0x0202] = 0xdd
        setup_cpu.memory[0xdd69] = value
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
    def test_and_absolute_x_no_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x3d  # AND instruction
        setup_cpu.memory[0x0201] = 0xdd
        setup_cpu.memory[0x0202] = 0x11
        setup_cpu.idx = 0x01
        setup_cpu.memory[0x11dd + 0x01] = value
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
    def test_and_absolute_x_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x3d  # AND instruction
        setup_cpu.memory[0x0201] = 0xee
        setup_cpu.memory[0x0202] = 0xaa
        setup_cpu.idx = 0xff
        setup_cpu.memory[0xaaee + 0xff] = value
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
    def test_and_absolute_y_no_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x39  # AND instruction
        setup_cpu.memory[0x0201] = 0xad
        setup_cpu.memory[0x0202] = 0xda
        setup_cpu.idy = 0x01
        setup_cpu.memory[0xdaad + 0x01] = value
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
    def test_and_absolute_y_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x39  # AND instruction
        setup_cpu.memory[0x0201] = 0xfe
        setup_cpu.memory[0x0202] = 0x21
        setup_cpu.idy = 0xff
        setup_cpu.memory[0x21fe + 0xff] = value
        setup_cpu.acc = acc
        expected_value = acc & value
        expected_zero_flag = (expected_value == 0)
        expected_negative_flag = (expected_value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.clock.total_clock_cycles == 5
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag

    @pytest.mark.parametrize('acc', [0x1, 0x0, 0xff, 0xa2])
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    def test_and_indexed_indirect(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x21  # AND instruction
        setup_cpu.memory[0x0201] = 0x99
        setup_cpu.idx = 0x30
        setup_cpu.memory[0x99 + 0x30] = 0xcc
        setup_cpu.memory[0x99 + 0x30 + 1] = 0xbb
        setup_cpu.memory[0xbbcc] = value
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
    def test_and_indirect_indexed_no_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x31  # AND instruction
        setup_cpu.memory[0x0201] = 0xcc
        setup_cpu.memory[0xcc] = 0x44
        setup_cpu.memory[0xcc + 1] = 0x32
        setup_cpu.memory[0x3244 + 0x01] = value
        setup_cpu.idy = 0x01
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
    def test_and_indirect_indexed_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x31  # AND instruction
        setup_cpu.memory[0x0201] = 0xcc
        setup_cpu.memory[0xcc] = 0x44
        setup_cpu.memory[0xcc + 1] = 0x32
        setup_cpu.memory[0x3244 + 0xff] = value
        setup_cpu.idy = 0xff
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
    def test_eor_zero_page(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x45  # EOR instruction
        setup_cpu.memory[0x0201] = 0x69
        setup_cpu.memory[0x69] = value
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
    def test_eor_zero_page_x(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x55  # EOR instruction
        setup_cpu.memory[0x0201] = 0xf2
        setup_cpu.idx = 0x0a
        setup_cpu.memory[0xf2 + 0x0a] = value
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
    def test_eor_absolute(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x4d  # EOR instruction
        setup_cpu.memory[0x0201] = 0x09
        setup_cpu.memory[0x0202] = 0x60
        setup_cpu.memory[0x6009] = value
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
    def test_eor_absolute_x_no_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x5d  # EOR instruction
        setup_cpu.memory[0x0201] = 0x37
        setup_cpu.memory[0x0202] = 0x21
        setup_cpu.idx = 0x69
        setup_cpu.memory[0x2137 + 0x69] = value
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
    def test_eor_absolute_x_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x5d  # EOR instruction
        setup_cpu.memory[0x0201] = 0x37
        setup_cpu.memory[0x0202] = 0x21
        setup_cpu.idx = 0xff
        setup_cpu.memory[0x2137 + 0xff] = value
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
    def test_eor_absolute_y_no_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x59  # EOR instruction
        setup_cpu.memory[0x0201] = 0xaa
        setup_cpu.memory[0x0202] = 0xbb
        setup_cpu.idy = 0x01
        setup_cpu.memory[0xbbaa + 0x01] = value
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
    def test_eor_absolute_y_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x59  # EOR instruction
        setup_cpu.memory[0x0201] = 0xaa
        setup_cpu.memory[0x0202] = 0xbb
        setup_cpu.idy = 0xff
        setup_cpu.memory[0xbbaa + 0xff] = value
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
    def test_eor_indexed_indirect(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x41  # EOR instruction
        setup_cpu.memory[0x0201] = 0x69
        setup_cpu.idx = 0x45
        setup_cpu.memory[0x69 + 0x45] = 0x77
        setup_cpu.memory[0x69 + 0x45 + 1] = 0xaa
        setup_cpu.memory[0xaa77] = value
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
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    def test_eor_indirect_indexed_no_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x51  # EOR instruction
        setup_cpu.memory[0x0201] = 0x69
        setup_cpu.memory[0x69] = 0x11
        setup_cpu.memory[0x69 + 1] = 0x22
        setup_cpu.memory[0x2211 + 0x01] = value
        setup_cpu.idy = 0x01
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
    def test_eor_indirect_indexed_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x51  # EOR instruction
        setup_cpu.memory[0x0201] = 0x69
        setup_cpu.memory[0x69] = 0x11
        setup_cpu.memory[0x69 + 1] = 0x22
        setup_cpu.memory[0x2211 + 0xff] = value
        setup_cpu.idy = 0xff
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
    def test_ora_zero_page(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x05  # ORA instruction
        setup_cpu.memory[0x0201] = 0xa1
        setup_cpu.memory[0xa1] = value
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
    def test_ora_zero_page_x(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x15  # ORA instruction
        setup_cpu.memory[0x0201] = 0xa0
        setup_cpu.idx = 0x2a
        setup_cpu.memory[0xa0 + 0x2a] = value
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
    def test_ora_absolute(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x0d  # ORA instruction
        setup_cpu.memory[0x0201] = 0x32
        setup_cpu.memory[0x0202] = 0x14
        setup_cpu.memory[0x1432] = value
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
    def test_ora_absolute_x_no_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x1d  # ORA instruction
        setup_cpu.memory[0x0201] = 0xcd
        setup_cpu.memory[0x0202] = 0xba
        setup_cpu.idx = 0x01
        setup_cpu.memory[0xbacd + 0x01] = value
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
    def test_ora_absolute_x_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x1d  # ORA instruction
        setup_cpu.memory[0x0201] = 0xef
        setup_cpu.memory[0x0202] = 0x60
        setup_cpu.idx = 0xff
        setup_cpu.memory[0x60ef + 0xff] = value
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
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    def test_ora_absolute_y_no_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x19  # ORA instruction
        setup_cpu.memory[0x0201] = 0x01
        setup_cpu.memory[0x0202] = 0xff
        setup_cpu.idy = 0x02
        setup_cpu.memory[0xff01 + 0x02] = value
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
    def test_ora_absolute_y_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x19  # ORA instruction
        setup_cpu.memory[0x0201] = 0xee
        setup_cpu.memory[0x0202] = 0x10
        setup_cpu.idy = 0xff
        setup_cpu.memory[0x10ee + 0xff] = value
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
    @pytest.mark.parametrize('value', [0x21, 0xff, 0x0, 0xb2])
    def test_ora_indexed_indirect(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x01  # ORA instruction
        setup_cpu.memory[0x0201] = 0xa9
        setup_cpu.idx = 0x10
        setup_cpu.memory[0xa9 + 0x10] = 0xdd
        setup_cpu.memory[0xa9 + 0x10 + 1] = 0xaa
        setup_cpu.memory[0xaadd] = value
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
    def test_ora_indirect_indexed_no_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x11  # ORA instruction
        setup_cpu.memory[0x0201] = 0x9b
        setup_cpu.memory[0x9b] = 0x11
        setup_cpu.memory[0x9b + 1] = 0xab
        setup_cpu.memory[0xab11 + 0x3] = value
        setup_cpu.idy = 0x3
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
    def test_ora_indirect_indexed_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x11  # ORA instruction
        setup_cpu.memory[0x0201] = 0x8c
        setup_cpu.memory[0x8c] = 0xfe
        setup_cpu.memory[0x8c + 1] = 0x88
        setup_cpu.memory[0x88fe + 0xff] = value
        setup_cpu.idy = 0xff
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
    def test_bit_zero_page(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x24  # BIT instruction
        setup_cpu.memory[0x0201] = 0xc4
        setup_cpu.memory[0xc4] = value
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
    def test_bit_absolute(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0x2c  # BIT instruction
        setup_cpu.memory[0x0201] = 0x2c
        setup_cpu.memory[0x0202] = 0xe2
        setup_cpu.memory[0xe22c] = value
        setup_cpu.acc = acc
        expected_zero_flag = ((value & acc) == 0)
        expected_overflow_flag = (value & 0b01000000)
        expected_negative_flag = (value & 0b10000000 != 0)
        setup_cpu.execute(1)
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 4
