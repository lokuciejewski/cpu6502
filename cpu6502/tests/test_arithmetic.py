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
        expected_value = np.ubyte(value + acc + int(carry_flag))
        expected_carry_flag = value + acc + int(carry_flag) > 0xff
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

    def test_adc_zero_page(self, setup_cpu):
        pass

    def test_adc_zero_page_x(self, setup_cpu):
        pass

    def test_adc_absolute(self, setup_cpu):
        pass

    def test_adc_absolute_x_no_page_crossed(self, setup_cpu):
        pass

    def test_adc_absolute_x_page_crossed(self, setup_cpu):
        pass

    def test_adc_absolute_y_no_page_crossed(self, setup_cpu):
        pass

    def test_adc_absolute_y_page_crossed(self, setup_cpu):
        pass

    def test_adc_indexed_indirect(self, setup_cpu):
        pass

    def test_adc_indirect_indexed_no_page_crossed(self, setup_cpu):
        pass

    def test_adc_indirect_indexed_page_crossed(self, setup_cpu):
        pass


@pytest.mark.usefixtures('setup_cpu')
class TestSBC:

    def test_sbc_immediate(self, setup_cpu):
        pass

    def test_sbc_zero_page(self, setup_cpu):
        pass

    def test_sbc_zero_page_x(self, setup_cpu):
        pass

    def test_sbc_absolute(self, setup_cpu):
        pass

    def test_sbc_absolute_x_no_page_crossed(self, setup_cpu):
        pass

    def test_sbc_absolute_x_page_crossed(self, setup_cpu):
        pass

    def test_sbc_absolute_y_no_page_crossed(self, setup_cpu):
        pass

    def test_sbc_absolute_y_page_crossed(self, setup_cpu):
        pass

    def test_sbc_indexed_indirect(self, setup_cpu):
        pass

    def test_sbc_indirect_indexed_no_page_crossed(self, setup_cpu):
        pass

    def test_sbc_indirect_indexed_page_crossed(self, setup_cpu):
        pass


@pytest.mark.usefixtures('setup_cpu')
class TestCMP:

    def test_cmp_immediate(self, setup_cpu):
        pass

    def test_cmp_zero_page(self, setup_cpu):
        pass

    def test_cmp_zero_page_x(self, setup_cpu):
        pass

    def test_cmp_absolute(self, setup_cpu):
        pass

    def test_cmp_absolute_x_no_page_crossed(self, setup_cpu):
        pass

    def test_cmp_absolute_x_page_crossed(self, setup_cpu):
        pass

    def test_cmp_absolute_y_no_page_crossed(self, setup_cpu):
        pass

    def test_cmp_absolute_y_page_crossed(self, setup_cpu):
        pass

    def test_cmp_indexed_indirect(self, setup_cpu):
        pass

    def test_cmp_indirect_indexed_no_page_crossed(self, setup_cpu):
        pass

    def test_cmp_indirect_indexed_page_crossed(self, setup_cpu):
        pass


@pytest.mark.usefixtures('setup_cpu')
class TestCPX:

    def test_cpx_immediate(self, setup_cpu):
        pass

    def test_cpx_zero_page(self, setup_cpu):
        pass

    def test_cpx_absolute(self, setup_cpu):
        pass


@pytest.mark.usefixtures('setup_cpu')
class TestCPY:

    def test_cpy_immediate(self, setup_cpu):
        pass

    def test_cpy_zero_page(self, setup_cpu):
        pass

    def test_cpy_absolute(self, setup_cpu):
        pass
