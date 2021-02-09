import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestSTX:

    def test_stx_zero_page(self, setup_cpu):
        pass

    def test_stx_zero_page_y(self, setup_cpu):
        pass

    def test_stx_absolute(self, setup_cpu):
        pass
