import numpy as np
import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestASL:

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    def test_asl_accumulator(self, setup_cpu, value):
        setup_cpu.memory[0x0200] = 0x0a  # ASL instruction
        setup_cpu.acc = value
        expected_value = np.ubyte(value * 2)
        expected_carry_flag = (value >> 7)
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 2

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    def test_asl_zero_page(self, setup_cpu, value):
        setup_cpu.memory[0x0200] = 0x06  # ASL instruction
        setup_cpu.memory[0x0201] = 0xb4
        setup_cpu.memory[0xb4] = value
        expected_value = np.ubyte(value * 2)
        expected_carry_flag = (value >> 7)
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.memory[0xb4] == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 5

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    def test_asl_zero_page_x(self, setup_cpu, value):
        setup_cpu.memory[0x0200] = 0x16  # ASL instruction
        setup_cpu.memory[0x0201] = 0xb4
        setup_cpu.memory[0xb4 + 0x12] = value
        setup_cpu.idx = 0x12
        expected_value = np.ubyte(value * 2)
        expected_carry_flag = (value >> 7)
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.memory[0xb4 + 0x12] == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 6

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    def test_asl_absolute(self, setup_cpu, value):
        setup_cpu.memory[0x0200] = 0x0e  # ASL instruction
        setup_cpu.memory[0x0201] = 0x86
        setup_cpu.memory[0x0202] = 0x21
        setup_cpu.memory[0x2186] = value
        expected_value = np.ubyte(value * 2)
        expected_carry_flag = (value >> 7)
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x2186] == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 6

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    def test_asl_absolute_x(self, setup_cpu, value):
        setup_cpu.memory[0x0200] = 0x1e  # ASL instruction
        setup_cpu.memory[0x0201] = 0x86
        setup_cpu.memory[0x0202] = 0x21
        setup_cpu.memory[0x2186 + 0xab] = value
        setup_cpu.idx = 0xab
        expected_value = np.ubyte(value * 2)
        expected_carry_flag = (value >> 7)
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x2186 + 0xab] == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 7


@pytest.mark.usefixtures('setup_cpu')
class TestLSR:

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    def test_lsr_accumulator(self, setup_cpu, value):
        setup_cpu.memory[0x0200] = 0x4a  # LSR instruction
        setup_cpu.acc = value
        expected_value = np.ubyte(value / 2)
        expected_carry_flag = value % 2
        expected_zero_flag = expected_value == 0
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert not setup_cpu.ps['negative_flag']
        assert setup_cpu.clock.total_clock_cycles == 2

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    def test_lsr_zero_page(self, setup_cpu, value):
        setup_cpu.memory[0x0200] = 0x46  # LSR instruction
        setup_cpu.memory[0x0201] = 0xb5
        setup_cpu.memory[0xb5] = value
        expected_value = np.ubyte(value / 2)
        expected_carry_flag = value % 2
        expected_zero_flag = expected_value == 0
        setup_cpu.execute(1)
        assert setup_cpu.memory[0xb5] == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert not setup_cpu.ps['negative_flag']
        assert setup_cpu.clock.total_clock_cycles == 5

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    def test_lsr_zero_page_x(self, setup_cpu, value):
        setup_cpu.memory[0x0200] = 0x56  # LSR instruction
        setup_cpu.memory[0x0201] = 0xb5
        setup_cpu.memory[0xb5 + 0x12] = value
        setup_cpu.idx = 0x12
        expected_value = np.ubyte(value / 2)
        expected_carry_flag = value % 2
        expected_zero_flag = expected_value == 0
        setup_cpu.execute(1)
        assert setup_cpu.memory[0xb5 + 0x12] == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert not setup_cpu.ps['negative_flag']
        assert setup_cpu.clock.total_clock_cycles == 6

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    def test_lsr_absolute(self, setup_cpu, value):
        setup_cpu.memory[0x0200] = 0x4e  # LSR instruction
        setup_cpu.memory[0x0201] = 0x81
        setup_cpu.memory[0x0202] = 0x21
        setup_cpu.memory[0x2181] = value
        expected_value = np.ubyte(value / 2)
        expected_carry_flag = value % 2
        expected_zero_flag = expected_value == 0
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x2181] == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert not setup_cpu.ps['negative_flag']
        assert setup_cpu.clock.total_clock_cycles == 6

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    def test_lsr_absolute_x(self, setup_cpu, value):
        setup_cpu.memory[0x0200] = 0x5e  # LSR instruction
        setup_cpu.memory[0x0201] = 0x81
        setup_cpu.memory[0x0202] = 0x21
        setup_cpu.memory[0x2181 + 0xab] = value
        setup_cpu.idx = 0xab
        expected_value = np.ubyte(value / 2)
        expected_carry_flag = value % 2
        expected_zero_flag = expected_value == 0
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x2181 + 0xab] == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert not setup_cpu.ps['negative_flag']
        assert setup_cpu.clock.total_clock_cycles == 7


@pytest.mark.usefixtures('setup_cpu')
class TestROL:

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_rol_accumulator(self, setup_cpu, value, carry_flag):
        setup_cpu.memory[0x0200] = 0x2a  # ROL instruction
        setup_cpu.acc = value
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte((value << 1) + carry_flag)
        expected_carry_flag = (value >> 7)
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 2

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_rol_zero_page(self, setup_cpu, value, carry_flag):
        setup_cpu.memory[0x0200] = 0x26  # ROL instruction
        setup_cpu.memory[0x0201] = 0x27
        setup_cpu.memory[0x27] = value
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte((value << 1) + carry_flag)
        expected_carry_flag = (value >> 7)
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x27] == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 5

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_rol_zero_page_x(self, setup_cpu, value, carry_flag):
        setup_cpu.memory[0x0200] = 0x36  # ROL instruction
        setup_cpu.memory[0x0201] = 0x27
        setup_cpu.memory[0x27 + 0x69] = value
        setup_cpu.idx = 0x69
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte((value << 1) + carry_flag)
        expected_carry_flag = (value >> 7)
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x27 + 0x69] == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 6

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_rol_absolute(self, setup_cpu, value, carry_flag):
        setup_cpu.memory[0x0200] = 0x2e  # ROL instruction
        setup_cpu.memory[0x0201] = 0x75
        setup_cpu.memory[0x0202] = 0x09
        setup_cpu.memory[0x0975] = value
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte((value << 1) + carry_flag)
        expected_carry_flag = (value >> 7)
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x0975] == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 6

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_rol_absolute_x(self, setup_cpu, value, carry_flag):
        setup_cpu.memory[0x0200] = 0x3e  # ROL instruction
        setup_cpu.memory[0x0201] = 0x75
        setup_cpu.memory[0x0202] = 0x09
        setup_cpu.memory[0x0975 + 0x89] = value
        setup_cpu.idx = 0x89
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte((value << 1) + carry_flag)
        expected_carry_flag = (value >> 7)
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x0975 + 0x89] == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 6


@pytest.mark.usefixtures('setup_cpu')
class TestROR:

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_ror_accumulator(self, setup_cpu, value, carry_flag):
        setup_cpu.memory[0x0200] = 0x6a  # ROR instruction
        setup_cpu.acc = value
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte((value >> 1) + (carry_flag << 7))
        expected_carry_flag = value % 2
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 2

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_ror_zero_page(self, setup_cpu, value, carry_flag):
        setup_cpu.memory[0x0200] = 0x66  # ROR instruction
        setup_cpu.memory[0x0201] = 0x27
        setup_cpu.memory[0x27] = value
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte((value >> 1) + (carry_flag << 7))
        expected_carry_flag = value % 2
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x27] == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 5

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_ror_zero_page_x(self, setup_cpu, value, carry_flag):
        setup_cpu.memory[0x0200] = 0x76  # ROR instruction
        setup_cpu.memory[0x0201] = 0x27
        setup_cpu.memory[0x27 + 0x69] = value
        setup_cpu.idx = 0x69
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte((value >> 1) + (carry_flag << 7))
        expected_carry_flag = value % 2
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x27 + 0x69] == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 6

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_ror_absolute(self, setup_cpu, value, carry_flag):
        setup_cpu.memory[0x0200] = 0x6e  # ROR instruction
        setup_cpu.memory[0x0201] = 0x27
        setup_cpu.memory[0x0202] = 0x09
        setup_cpu.memory[0x0927] = value
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte((value >> 1) + (carry_flag << 7))
        expected_carry_flag = value % 2
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x0927] == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 6

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_ror_absolute_x(self, setup_cpu, value, carry_flag):
        setup_cpu.memory[0x0200] = 0x7e  # ROR instruction
        setup_cpu.memory[0x0200] = 0x7e  # ROR instruction
        setup_cpu.memory[0x0201] = 0x27
        setup_cpu.memory[0x0202] = 0x09
        setup_cpu.memory[0x0927 + 0x89] = value
        setup_cpu.idx = 0x89
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte((value >> 1) + (carry_flag << 7))
        expected_carry_flag = value % 2
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x0927 + 0x89] == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 6
