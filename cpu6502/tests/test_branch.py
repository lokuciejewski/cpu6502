import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestBCC:

    def test_bcc_no_page_crossed(self, setup_cpu):
        pass

    def test_bcc_page_crossed(self, setup_cpu):
        pass


@pytest.mark.usefixtures('setup_cpu')
class TestBCS:

    def test_bcc_no_page_crossed(self, setup_cpu):
        pass

    def test_bcc_page_crossed(self, setup_cpu):
        pass


@pytest.mark.usefixtures('setup_cpu')
class TestBEQ:

    def test_bcc_no_page_crossed(self, setup_cpu):
        pass

    def test_bcc_page_crossed(self, setup_cpu):
        pass


@pytest.mark.usefixtures('setup_cpu')
class TestBMI:

    def test_bcc_no_page_crossed(self, setup_cpu):
        pass

    def test_bcc_page_crossed(self, setup_cpu):
        pass


@pytest.mark.usefixtures('setup_cpu')
class TestBNE:

    def test_bcc_no_page_crossed(self, setup_cpu):
        pass

    def test_bcc_page_crossed(self, setup_cpu):
        pass


@pytest.mark.usefixtures('setup_cpu')
class TestBPL:

    def test_bcc_no_page_crossed(self, setup_cpu):
        pass

    def test_bcc_page_crossed(self, setup_cpu):
        pass


@pytest.mark.usefixtures('setup_cpu')
class TestBVC:

    def test_bcc_no_page_crossed(self, setup_cpu):
        pass

    def test_bcc_page_crossed(self, setup_cpu):
        pass


@pytest.mark.usefixtures('setup_cpu')
class TestBVS:

    def test_bcc_no_page_crossed(self, setup_cpu):
        pass

    def test_bcc_page_crossed(self, setup_cpu):
        pass
