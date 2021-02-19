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
        setup_cpu.memory[0x0200] = 0x06  # ASL instruction
        setup_cpu.memory[0x0201] = 0xb4
        setup_cpu.memory[0xb4 + 0x12] = value
        setup_cpu.idx = 0x12
        expected_value = np.ubyte(value * 2)
        expected_carry_flag = (value >> 7)
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.memory[0xb4] == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 6

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x40, 0xaa, 0xaf, 0xfe, 0xff, 0x7f])
    def test_asl_absolute(self, setup_cpu, value):
        setup_cpu.memory[0x0200] = 0x06  # ASL instruction
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
        setup_cpu.memory[0x0200] = 0x06  # ASL instruction
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

    def test_lsr_accumulator(self, setup_cpu):
        pass

    def test_lsr_zero_page(self, setup_cpu):
        pass

    def test_lsr_zero_page_x(self, setup_cpu):
        pass

    def test_lsr_absolute(self, setup_cpu):
        pass

    def test_lsr_absolute_x(self, setup_cpu):
        pass


@pytest.mark.usefixtures('setup_cpu')
class TestROL:

    def test_rol_accumulator(self, setup_cpu):
        pass

    def test_rol_zero_page(self, setup_cpu):
        pass

    def test_rol_zero_page_x(self, setup_cpu):
        pass

    def test_rol_absolute(self, setup_cpu):
        pass

    def test_rol_absolute_x(self, setup_cpu):
        pass


@pytest.mark.usefixtures('setup_cpu')
class TestROR:

    def test_ror_accumulator(self, setup_cpu):
        pass

    def test_ror_zero_page(self, setup_cpu):
        pass

    def test_ror_zero_page_x(self, setup_cpu):
        pass

    def test_ror_absolute(self, setup_cpu):
        pass

    def test_ror_absolute_x(self, setup_cpu):
        pass
