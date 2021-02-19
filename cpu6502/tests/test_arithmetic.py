import numpy as np
import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestADC:

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_adc_immediate(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.memory[0x0200] = 0x69  # ADC instruction
        setup_cpu.memory[0x0201] = value
        setup_cpu.acc = acc
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(value + acc + carry_flag)
        expected_carry_flag = value + acc + carry_flag > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        """
        x       y       r        Overflow
        1.... + 1.... = 0.... -> True
        0.... + 0.... = 1.... -> True
        0.... + 1.... = 0.... -> False
        0.... + 1.... = 1.... -> False
        1.... + 0.... = 1.... -> False
        1.... + 0.... = 0.... -> False

        (x == y) != r
        """
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 2

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_adc_zero_page(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.memory[0x0200] = 0x65  # ADC instruction
        setup_cpu.memory[0x0201] = 0x1a
        setup_cpu.memory[0x1a] = value
        setup_cpu.acc = acc
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(value + acc + carry_flag)
        expected_carry_flag = value + acc + carry_flag > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_adc_zero_page_x(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.memory[0x0200] = 0x75  # ADC instruction
        setup_cpu.memory[0x0201] = 0xb1
        setup_cpu.memory[0xb1 + 0x10] = value
        setup_cpu.acc = acc
        setup_cpu.idx = 0x10
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(value + acc + carry_flag)
        expected_carry_flag = value + acc + carry_flag > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_adc_absolute(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.memory[0x0200] = 0x6d  # ADC instruction
        setup_cpu.memory[0x0201] = 0xb1
        setup_cpu.memory[0x0202] = 0xac
        setup_cpu.memory[0xacb1] = value
        setup_cpu.acc = acc
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(value + acc + carry_flag)
        expected_carry_flag = value + acc + carry_flag > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_adc_absolute_x_no_page_crossed(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.memory[0x0200] = 0x7d  # ADC instruction
        setup_cpu.memory[0x0201] = 0xb1
        setup_cpu.memory[0x0202] = 0xac
        setup_cpu.memory[0xacb1 + 0x01] = value
        setup_cpu.acc = acc
        setup_cpu.idx = 0x01
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(value + acc + carry_flag)
        expected_carry_flag = value + acc + carry_flag > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_adc_absolute_x_page_crossed(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.memory[0x0200] = 0x7d  # ADC instruction
        setup_cpu.memory[0x0201] = 0xb1
        setup_cpu.memory[0x0202] = 0xac
        setup_cpu.memory[0xacb1 + 0xff] = value
        setup_cpu.acc = acc
        setup_cpu.idx = 0xff
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(value + acc + carry_flag)
        expected_carry_flag = value + acc + carry_flag > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 5

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_adc_absolute_y_no_page_crossed(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.memory[0x0200] = 0x79  # ADC instruction
        setup_cpu.memory[0x0201] = 0xb1
        setup_cpu.memory[0x0202] = 0xac
        setup_cpu.memory[0xacb1 + 0x01] = value
        setup_cpu.acc = acc
        setup_cpu.idy = 0x01
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(value + acc + carry_flag)
        expected_carry_flag = value + acc + carry_flag > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_adc_absolute_y_page_crossed(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.memory[0x0200] = 0x79  # ADC instruction
        setup_cpu.memory[0x0201] = 0xb1
        setup_cpu.memory[0x0202] = 0xac
        setup_cpu.memory[0xacb1 + 0xff] = value
        setup_cpu.acc = acc
        setup_cpu.idy = 0xff
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(value + acc + carry_flag)
        expected_carry_flag = value + acc + carry_flag > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 5

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_adc_indexed_indirect(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.idx = 0x10
        setup_cpu.memory[0x0200] = 0x61  # ADC instruction
        setup_cpu.memory[0x201] = 0xb8
        setup_cpu.memory[0xb8 + setup_cpu.idx] = 0x88
        setup_cpu.memory[0xb8 + setup_cpu.idx + 1] = 0x7a
        setup_cpu.memory[0x7a88] = value
        setup_cpu.acc = acc
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(value + acc + carry_flag)
        expected_carry_flag = value + acc + carry_flag > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 6

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_adc_indirect_indexed_no_page_crossed(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.idy = 0x01
        setup_cpu.memory[0x0200] = 0x71  # ADC instruction
        setup_cpu.memory[0x201] = 0x00ae
        setup_cpu.memory[0x00ae] = 0x37
        setup_cpu.memory[0x00af] = 0x21
        setup_cpu.memory[0x2137 + 0x01] = value
        setup_cpu.acc = acc
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(value + acc + carry_flag)
        expected_carry_flag = value + acc + carry_flag > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 5

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_adc_indirect_indexed_page_crossed(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.idy = 0xff
        setup_cpu.memory[0x0200] = 0x71  # ADC instruction
        setup_cpu.memory[0x201] = 0x00ae
        setup_cpu.memory[0x00ae] = 0x37
        setup_cpu.memory[0x00af] = 0x21
        setup_cpu.memory[0x2137 + 0xff] = value
        setup_cpu.acc = acc
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(value + acc + carry_flag)
        expected_carry_flag = value + acc + carry_flag > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 6


@pytest.mark.usefixtures('setup_cpu')
class TestSBC:

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_sbc_immediate(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.memory[0x0200] = 0xe9  # SBC instruction
        setup_cpu.memory[0x0201] = value
        setup_cpu.acc = acc
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(acc - value - (1 - carry_flag))
        expected_carry_flag = acc - value - (1 - carry_flag) > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 2

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_sbc_zero_page(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.memory[0x0200] = 0xe5  # SBC instruction
        setup_cpu.memory[0x0201] = 0x1a
        setup_cpu.memory[0x1a] = value
        setup_cpu.acc = acc
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(acc - value - (1 - carry_flag))
        expected_carry_flag = acc - value - (1 - carry_flag) > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_sbc_zero_page_x(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.memory[0x0200] = 0xf5  # SBC instruction
        setup_cpu.memory[0x0201] = 0x1a
        setup_cpu.memory[0x1a + 0x20] = value
        setup_cpu.acc = acc
        setup_cpu.idx = 0x20
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(acc - value - (1 - carry_flag))
        expected_carry_flag = acc - value - (1 - carry_flag) > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_sbc_absolute(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.memory[0x0200] = 0xed  # SBC instruction
        setup_cpu.memory[0x0201] = 0xb1
        setup_cpu.memory[0x0202] = 0xac
        setup_cpu.memory[0xacb1] = value
        setup_cpu.acc = acc
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(acc - value - (1 - carry_flag))
        expected_carry_flag = acc - value - (1 - carry_flag) > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_sbc_absolute_x_no_page_crossed(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.memory[0x0200] = 0xfd  # SBC instruction
        setup_cpu.memory[0x0201] = 0xb1
        setup_cpu.memory[0x0202] = 0xac
        setup_cpu.memory[0xacb1 + 0x01] = value
        setup_cpu.acc = acc
        setup_cpu.idx = 0x01
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(acc - value - (1 - carry_flag))
        expected_carry_flag = acc - value - (1 - carry_flag) > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_sbc_absolute_x_page_crossed(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.memory[0x0200] = 0xfd  # SBC instruction
        setup_cpu.memory[0x0201] = 0xb1
        setup_cpu.memory[0x0202] = 0xac
        setup_cpu.memory[0xacb1 + 0xff] = value
        setup_cpu.acc = acc
        setup_cpu.idx = 0xff
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(acc - value - (1 - carry_flag))
        expected_carry_flag = acc - value - (1 - carry_flag) > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 5

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_sbc_absolute_y_no_page_crossed(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.memory[0x0200] = 0xf9  # SBC instruction
        setup_cpu.memory[0x0201] = 0xb1
        setup_cpu.memory[0x0202] = 0xac
        setup_cpu.memory[0xacb1 + 0x01] = value
        setup_cpu.acc = acc
        setup_cpu.idy = 0x01
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(acc - value - (1 - carry_flag))
        expected_carry_flag = acc - value - (1 - carry_flag) > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_sbc_absolute_y_page_crossed(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.memory[0x0200] = 0xf9  # SBC instruction
        setup_cpu.memory[0x0201] = 0xb1
        setup_cpu.memory[0x0202] = 0xac
        setup_cpu.memory[0xacb1 + 0xff] = value
        setup_cpu.acc = acc
        setup_cpu.idy = 0xff
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(acc - value - (1 - carry_flag))
        expected_carry_flag = acc - value - (1 - carry_flag) > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 5

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_sbc_indexed_indirect(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.idx = 0x10
        setup_cpu.memory[0x0200] = 0xe1  # SBC instruction
        setup_cpu.memory[0x201] = 0xb8
        setup_cpu.memory[0xb8 + setup_cpu.idx] = 0x88
        setup_cpu.memory[0xb8 + setup_cpu.idx + 1] = 0x7a
        setup_cpu.memory[0x7a88] = value
        setup_cpu.acc = acc
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(acc - value - (1 - carry_flag))
        expected_carry_flag = acc - value - (1 - carry_flag) > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 6

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_sbc_indirect_indexed_no_page_crossed(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.idy = 0x01
        setup_cpu.memory[0x0200] = 0xf1  # SBC instruction
        setup_cpu.memory[0x201] = 0x00ae
        setup_cpu.memory[0x00ae] = 0x37
        setup_cpu.memory[0x00af] = 0x21
        setup_cpu.memory[0x2137 + 0x01] = value
        setup_cpu.acc = acc
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(acc - value - (1 - carry_flag))
        expected_carry_flag = acc - value - (1 - carry_flag) > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 5

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xef, 0xff])
    @pytest.mark.parametrize('value', [0x0, 0x2, 0xf1, 0xfe])
    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_sbc_indirect_indexed_page_crossed(self, setup_cpu, acc, value, carry_flag):
        setup_cpu.idy = 0xff
        setup_cpu.memory[0x0200] = 0xf1  # SBC instruction
        setup_cpu.memory[0x201] = 0x00ae
        setup_cpu.memory[0x00ae] = 0x37
        setup_cpu.memory[0x00af] = 0x21
        setup_cpu.memory[0x2137 + 0xff] = value
        setup_cpu.acc = acc
        setup_cpu.ps['carry_flag'] = carry_flag
        expected_value = np.ubyte(acc - value - (1 - carry_flag))
        expected_carry_flag = acc - value - (1 - carry_flag) > 0xff
        expected_zero_flag = expected_value == 0
        expected_negative_flag = (expected_value & 0b10000000) != 0
        expected_overflow_flag = ((value >> 7) == (acc >> 7)) != (expected_value >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.acc == expected_value
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.ps['overflow_flag'] == expected_overflow_flag
        assert setup_cpu.clock.total_clock_cycles == 6


@pytest.mark.usefixtures('setup_cpu')
class TestCMP:

    @pytest.mark.parametrize('value', [0x0, 0x1, 0xff, 0xfe, 0x54])
    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xfe, 0x64])
    def test_cmp_immediate(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0xc9  # CMP instruction
        setup_cpu.memory[0x0201] = value
        setup_cpu.acc = acc
        expected_carry_flag = acc >= value
        expected_zero_flag = acc == value
        expected_negative_flag = ((acc - value) >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 2

    @pytest.mark.parametrize('value', [0x0, 0x1, 0xff, 0xfe, 0x54])
    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xfe, 0x64])
    def test_cmp_zero_page(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0xc5  # CMP instruction
        setup_cpu.memory[0x0201] = 0xab
        setup_cpu.memory[0xab] = value
        setup_cpu.acc = acc
        expected_carry_flag = acc >= value
        expected_zero_flag = acc == value
        expected_negative_flag = ((acc - value) >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('value', [0x0, 0x1, 0xff, 0xfe, 0x54])
    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xfe, 0x64])
    def test_cmp_zero_page_x(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0xd5  # CMP instruction
        setup_cpu.memory[0x0201] = 0xab
        setup_cpu.memory[0xab + 0x10] = value
        setup_cpu.acc = acc
        setup_cpu.idx = 0x10
        expected_carry_flag = acc >= value
        expected_zero_flag = acc == value
        expected_negative_flag = ((acc - value) >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('value', [0x0, 0x1, 0xff, 0xfe, 0x54])
    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xfe, 0x64])
    def test_cmp_absolute(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0xcd  # CMP instruction
        setup_cpu.memory[0x0201] = 0xab
        setup_cpu.memory[0x0202] = 0xcd
        setup_cpu.memory[0xcdab] = value
        setup_cpu.acc = acc
        expected_carry_flag = acc >= value
        expected_zero_flag = acc == value
        expected_negative_flag = ((acc - value) >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('value', [0x0, 0x1, 0xff, 0xfe, 0x54])
    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xfe, 0x64])
    def test_cmp_absolute_x_no_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0xdd  # CMP instruction
        setup_cpu.memory[0x0201] = 0xab
        setup_cpu.memory[0x0202] = 0xcd
        setup_cpu.memory[0xcdab + 0x01] = value
        setup_cpu.acc = acc
        setup_cpu.idx = 0x01
        expected_carry_flag = acc >= value
        expected_zero_flag = acc == value
        expected_negative_flag = ((acc - value) >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('value', [0x0, 0x1, 0xff, 0xfe, 0x54])
    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xfe, 0x64])
    def test_cmp_absolute_x_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0xdd  # CMP instruction
        setup_cpu.memory[0x0201] = 0xab
        setup_cpu.memory[0x0202] = 0xcd
        setup_cpu.memory[0xcdab + 0xff] = value
        setup_cpu.acc = acc
        setup_cpu.idx = 0xff
        expected_carry_flag = acc >= value
        expected_zero_flag = acc == value
        expected_negative_flag = ((acc - value) >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 5

    @pytest.mark.parametrize('value', [0x0, 0x1, 0xff, 0xfe, 0x54])
    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xfe, 0x64])
    def test_cmp_absolute_y_no_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0xd9  # CMP instruction
        setup_cpu.memory[0x0201] = 0xab
        setup_cpu.memory[0x0202] = 0xcd
        setup_cpu.memory[0xcdab + 0x01] = value
        setup_cpu.acc = acc
        setup_cpu.idy = 0x01
        expected_carry_flag = acc >= value
        expected_zero_flag = acc == value
        expected_negative_flag = ((acc - value) >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('value', [0x0, 0x1, 0xff, 0xfe, 0x54])
    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xfe, 0x64])
    def test_cmp_absolute_y_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0xd9  # CMP instruction
        setup_cpu.memory[0x0201] = 0xab
        setup_cpu.memory[0x0202] = 0xcd
        setup_cpu.memory[0xcdab + 0xff] = value
        setup_cpu.acc = acc
        setup_cpu.idy = 0xff
        expected_carry_flag = acc >= value
        expected_zero_flag = acc == value
        expected_negative_flag = ((acc - value) >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 5

    @pytest.mark.parametrize('value', [0x0, 0x1, 0xff, 0xfe, 0x54])
    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xfe, 0x64])
    def test_cmp_indexed_indirect(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0xc1  # CMP instruction
        setup_cpu.memory[0x0201] = 0x5e
        setup_cpu.memory[np.ubyte(0x5e + 0x2f)] = 0xcd
        setup_cpu.memory[np.ubyte(0x5e + 0x2f) + 1] = 0xab
        setup_cpu.memory[0xabcd] = value
        setup_cpu.acc = acc
        setup_cpu.idx = 0x2f
        expected_carry_flag = acc >= value
        expected_zero_flag = acc == value
        expected_negative_flag = ((acc - value) >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 6

    @pytest.mark.parametrize('value', [0x0, 0x1, 0xff, 0xfe, 0x54])
    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xfe, 0x64])
    def test_cmp_indirect_indexed_no_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0xd1  # CMP instruction
        setup_cpu.memory[0x0201] = 0x5e
        setup_cpu.memory[0x5e] = 0xcd
        setup_cpu.memory[0x5f] = 0xab
        setup_cpu.memory[0xabcd + 0x01] = value
        setup_cpu.acc = acc
        setup_cpu.idy = 0x01
        expected_carry_flag = acc >= value
        expected_zero_flag = acc == value
        expected_negative_flag = ((acc - value) >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 5

    @pytest.mark.parametrize('value', [0x0, 0x1, 0xff, 0xfe, 0x54])
    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xff, 0xfe, 0x64])
    def test_cmp_indirect_indexed_page_crossed(self, setup_cpu, acc, value):
        setup_cpu.memory[0x0200] = 0xd1  # CMP instruction
        setup_cpu.memory[0x0201] = 0x5e
        setup_cpu.memory[0x5e] = 0xcd
        setup_cpu.memory[0x5f] = 0xab
        setup_cpu.memory[0xabcd + 0xff] = value
        setup_cpu.acc = acc
        setup_cpu.idy = 0xff
        expected_carry_flag = acc >= value
        expected_zero_flag = acc == value
        expected_negative_flag = ((acc - value) >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 6


@pytest.mark.usefixtures('setup_cpu')
class TestCPX:

    @pytest.mark.parametrize('value', [0x0, 0x1, 0xff, 0xfe, 0x54])
    @pytest.mark.parametrize('idx', [0x0, 0x1, 0xff, 0xfe, 0x64])
    def test_cpx_immediate(self, setup_cpu, idx, value):
        setup_cpu.memory[0x0200] = 0xe0  # CPX instruction
        setup_cpu.memory[0x0201] = value
        setup_cpu.idx = idx
        expected_carry_flag = idx >= value
        expected_zero_flag = idx == value
        expected_negative_flag = ((idx - value) >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 2

    @pytest.mark.parametrize('value', [0x0, 0x1, 0xff, 0xfe, 0x54])
    @pytest.mark.parametrize('idx', [0x0, 0x1, 0xff, 0xfe, 0x64])
    def test_cpx_zero_page(self, setup_cpu, idx, value):
        setup_cpu.memory[0x0200] = 0xce4  # CPX instruction
        setup_cpu.memory[0x0201] = 0xab
        setup_cpu.memory[0xab] = value
        setup_cpu.idx = idx
        expected_carry_flag = idx >= value
        expected_zero_flag = idx == value
        expected_negative_flag = ((idx - value) >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('value', [0x0, 0x1, 0xff, 0xfe, 0x54])
    @pytest.mark.parametrize('idx', [0x0, 0x1, 0xff, 0xfe, 0x64])
    def test_cpx_absolute(self, setup_cpu, idx, value):
        setup_cpu.memory[0x0200] = 0xec  # CPX instruction
        setup_cpu.memory[0x0201] = 0xab
        setup_cpu.memory[0x0202] = 0xcd
        setup_cpu.memory[0xcdab] = value
        setup_cpu.idx = idx
        expected_carry_flag = idx >= value
        expected_zero_flag = idx == value
        expected_negative_flag = ((idx - value) >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 4


@pytest.mark.usefixtures('setup_cpu')
class TestCPY:

    @pytest.mark.parametrize('value', [0x0, 0x1, 0xff, 0xfe, 0x54])
    @pytest.mark.parametrize('idy', [0x0, 0x1, 0xff, 0xfe, 0x64])
    def test_cpy_immediate(self, setup_cpu, idy, value):
        setup_cpu.memory[0x0200] = 0xc0  # CPY instruction
        setup_cpu.memory[0x0201] = value
        setup_cpu.idy = idy
        expected_carry_flag = idy >= value
        expected_zero_flag = idy == value
        expected_negative_flag = ((idy - value) >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 2

    @pytest.mark.parametrize('value', [0x0, 0x1, 0xff, 0xfe, 0x54])
    @pytest.mark.parametrize('idy', [0x0, 0x1, 0xff, 0xfe, 0x64])
    def test_cpy_zero_page(self, setup_cpu, idy, value):
        setup_cpu.memory[0x0200] = 0xc4  # CPY instruction
        setup_cpu.memory[0x0201] = 0xab
        setup_cpu.memory[0xab] = value
        setup_cpu.idy = idy
        expected_carry_flag = idy >= value
        expected_zero_flag = idy == value
        expected_negative_flag = ((idy - value) >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('value', [0x0, 0x1, 0xff, 0xfe, 0x54])
    @pytest.mark.parametrize('idy', [0x0, 0x1, 0xff, 0xfe, 0x64])
    def test_cpy_absolute(self, setup_cpu, idy, value):
        setup_cpu.memory[0x0200] = 0xcc  # CPY instruction
        setup_cpu.memory[0x0201] = 0xab
        setup_cpu.memory[0x0202] = 0xcd
        setup_cpu.memory[0xcdab] = value
        setup_cpu.idy = idy
        expected_carry_flag = idy >= value
        expected_zero_flag = idy == value
        expected_negative_flag = ((idy - value) >> 7)
        setup_cpu.execute(1)
        assert setup_cpu.ps['carry_flag'] == expected_carry_flag
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 4
