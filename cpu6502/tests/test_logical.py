import pytest


@pytest.mark.usefixtures('setup_cpu')
class AND:

    def test_and_immediate(self, setup_cpu):
        pass

    def test_and_zero_page(self, setup_cpu):
        pass

    def test_and_zero_page_x(self, setup_cpu):
        pass

    def test_and_absolute(self, setup_cpu):
        pass

    def test_and_absolute_x(self, setup_cpu):
        pass

    def test_and_absolute_y(self, setup_cpu):
        pass

    def test_and_indexed_indirect(self, setup_cpu):
        pass

    def test_and_indirect_indexed(self, setup_cpu):
        pass


@pytest.mark.usefixtures('setup_cpu')
class EOR:

    def test_eor_immediate(self, setup_cpu):
        pass

    def test_eor_zero_page(self, setup_cpu):
        pass

    def test_eor_zero_page_x(self, setup_cpu):
        pass

    def test_eor_absolute(self, setup_cpu):
        pass

    def test_eor_absolute_x(self, setup_cpu):
        pass

    def test_eor_absolute_y(self, setup_cpu):
        pass

    def test_eor_indexed_indirect(self, setup_cpu):
        pass

    def test_eor_indirect_indexed(self, setup_cpu):
        pass


@pytest.mark.usefixtures('setup_cpu')
class ORA:

    def test_ora_immediate(self, setup_cpu):
        pass

    def test_ora_zero_page(self, setup_cpu):
        pass

    def test_ora_zero_page_x(self, setup_cpu):
        pass

    def test_ora_absolute(self, setup_cpu):
        pass

    def test_ora_absolute_x(self, setup_cpu):
        pass

    def test_ora_absolute_y(self, setup_cpu):
        pass

    def test_ora_indexed_indirect(self, setup_cpu):
        pass

    def test_ora_indirect_indexed(self, setup_cpu):
        pass


@pytest.mark.parametrize('setup_cpu')
class BIT:

    def test_bit_zero_page(self, setup_cpu):
        pass

    def test_bit_absolute(self, setup_cpu):
        pass
