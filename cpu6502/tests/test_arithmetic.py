import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestADC:

    def test_adc_immediate(self, setup_cpu):
        pass

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
