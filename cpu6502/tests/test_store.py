import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestSTA:

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    def test_sta_zero_page(self, setup_cpu, value):
        setup_cpu.acc = value
        setup_cpu.memory[0x0200] = 0x85  # STA instruction
        setup_cpu.memory[0x0201] = 0x10
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x10] == value
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    def test_sta_zero_page_x(self, setup_cpu, value):
        setup_cpu.acc = value
        setup_cpu.idx = 0x51
        setup_cpu.memory[0x0200] = 0x95  # STA instruction
        setup_cpu.memory[0x0201] = 0x25
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x25 + 0x51] == value
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    def test_sta_absolute(self, setup_cpu, value):
        setup_cpu.acc = value
        setup_cpu.memory[0x0200] = 0x8d  # STA instruction
        setup_cpu.memory[0x0201] = 0x88
        setup_cpu.memory[0x0202] = 0x77
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x7788] == value
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    def test_sta_absolute_x(self, setup_cpu, value,):
        setup_cpu.acc = value
        setup_cpu.idx = 0x20
        setup_cpu.memory[0x0200] = 0x9d  # STA instruction
        setup_cpu.memory[0x0201] = 0x77
        setup_cpu.memory[0x0202] = 0x66
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x6677 + 0x20] == value
        assert setup_cpu.clock.total_clock_cycles == 5

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    def test_sta_absolute_y(self, setup_cpu, value):
        setup_cpu.acc = value
        setup_cpu.idy = 0x20
        setup_cpu.memory[0x0200] = 0x99  # STA instruction
        setup_cpu.memory[0x0201] = 0x77
        setup_cpu.memory[0x0202] = 0x66
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x6677 + 0x20] == value
        assert setup_cpu.clock.total_clock_cycles == 5

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    def test_sta_indexed_indirect(self, setup_cpu, value):
        setup_cpu.memory[0x0200] = 0x81  # STA instruction
        setup_cpu.memory[0x0201] = 0x25
        setup_cpu.idx = 0x21
        setup_cpu.acc = value
        address = 0x25 + 0x21
        setup_cpu.memory[address] = 0x66
        setup_cpu.memory[address + 1] = 0x55
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x5566] == value
        assert setup_cpu.clock.total_clock_cycles == 6

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    def test_sta_indirect_indexed(self, setup_cpu, value):
        setup_cpu.memory[0x0200] = 0x91  # STA instruction
        setup_cpu.memory[0x0201] = 0x25
        setup_cpu.idy = 0x21
        setup_cpu.acc = value
        setup_cpu.memory[0x25] = 0x44
        setup_cpu.memory[0x25 + 1] = 0x55
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x5544 + 0x21] == value
        assert setup_cpu.clock.total_clock_cycles == 6


@pytest.mark.usefixtures('setup_cpu')
class TestSTX:

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    def test_stx_zero_page(self, setup_cpu, value):
        setup_cpu.idx = value
        setup_cpu.memory[0x0200] = 0x86  # STX instruction
        setup_cpu.memory[0x0201] = 0x56
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x56] == value
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    def test_stx_zero_page_y(self, setup_cpu, value):
        setup_cpu.idx = value
        setup_cpu.idy = 0x56
        setup_cpu.memory[0x0200] = 0x96  # STX instruction
        setup_cpu.memory[0x0201] = 0x27
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x27 + 0x56] == value
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    def test_stx_absolute(self, setup_cpu, value):
        setup_cpu.idx = value
        setup_cpu.memory[0x0200] = 0x8e  # STX instruction
        setup_cpu.memory[0x0201] = 0x33
        setup_cpu.memory[0x0202] = 0x11
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x1133] == value
        assert setup_cpu.clock.total_clock_cycles == 4


@pytest.mark.usefixtures('setup_cpu')
class TestSTY:

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    def test_sty_zero_page(self, setup_cpu, value):
        setup_cpu.idy = value
        setup_cpu.memory[0x0200] = 0x84  # STY instruction
        setup_cpu.memory[0x0201] = 0x12
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x12] == value
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    def test_sty_zero_page_x(self, setup_cpu, value):
        setup_cpu.idy = value
        setup_cpu.idx = 0x69
        setup_cpu.memory[0x0200] = 0x94  # STY instruction
        setup_cpu.memory[0x0201] = 0x93
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x93 + 0x69] == value
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x20, 0xff])
    def test_sty_absolute(self, setup_cpu, value):
        setup_cpu.idy = value
        setup_cpu.memory[0x0200] = 0x8c  # STY instruction
        setup_cpu.memory[0x0201] = 0x81
        setup_cpu.memory[0x0202] = 0x92
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x9281] == value
        assert setup_cpu.clock.total_clock_cycles == 4
