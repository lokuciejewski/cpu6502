import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestASL:

    def test_asl_accumulator(self, setup_cpu):
        pass

    def test_asl_zero_page(self, setup_cpu):
        pass

    def test_asl_zero_page_x(self, setup_cpu):
        pass

    def test_asl_absolute(self, setup_cpu):
        pass

    def test_asl_absolute_x(self, setup_cpu):
        pass


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
