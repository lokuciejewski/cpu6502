import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestSTA:

    def test_sta_zero_page(self, setup_cpu):
        pass

    def test_sta_zero_page_x(self, setup_cpu):
        pass

    def test_sta_absolute(self, setup_cpu):
        pass

    def test_sta_absolute_x(self, setup_cpu):
        pass

    def test_sta_absolute_y(self, setup_cpu):
        pass

    def test_sta_indirect_x(self, setup_cpu):
        pass

    def test_sta_indirect_y(self, setup_cpu):
        pass
