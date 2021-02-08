import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestRTS:

    def test_rts_implied(self, setup_cpu):
        pass
