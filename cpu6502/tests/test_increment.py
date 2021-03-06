import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestINC:

    @pytest.mark.parametrize('start_val, end_val', [(0x0, 0x1), (0x1, 0x2), (0xab, 0xac), (0xfe, 0xff), (0xff, 0x0)])
    def test_inc_zero_page(self, setup_cpu, start_val, end_val):
        setup_cpu.memory[0x0200] = 0xe6  # INC instruction
        setup_cpu.memory[0x0201] = 0xa4
        setup_cpu.memory[0xa4] = start_val
        expected_zero_flag = end_val == 0
        expected_negative_flag = (end_val >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.memory[0xa4] == end_val
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 5

    @pytest.mark.parametrize('start_val, end_val', [(0x0, 0x1), (0x1, 0x2), (0xab, 0xac), (0xfe, 0xff), (0xff, 0x0)])
    def test_inc_zero_page_x(self, setup_cpu, start_val, end_val):
        setup_cpu.memory[0x0200] = 0xf6  # INC instruction
        setup_cpu.memory[0x0201] = 0xa4
        setup_cpu.memory[0xa4 + 0x10] = start_val
        setup_cpu.idx = 0x10
        expected_zero_flag = end_val == 0
        expected_negative_flag = (end_val >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.memory[0xa4 + 0x10] == end_val
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 6

    @pytest.mark.parametrize('start_val, end_val', [(0x0, 0x1), (0x1, 0x2), (0xab, 0xac), (0xfe, 0xff), (0xff, 0x0)])
    def test_inc_absolute(self, setup_cpu, start_val, end_val):
        setup_cpu.memory[0x0200] = 0xee  # INC instruction
        setup_cpu.memory[0x0201] = 0x45
        setup_cpu.memory[0x0202] = 0x46
        setup_cpu.memory[0x4645] = start_val
        expected_zero_flag = end_val == 0
        expected_negative_flag = (end_val >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x4645] == end_val
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 6

    @pytest.mark.parametrize('start_val, end_val', [(0x0, 0x1), (0x1, 0x2), (0xab, 0xac), (0xfe, 0xff), (0xff, 0x0)])
    def test_inc_absolute_x(self, setup_cpu, start_val, end_val):
        setup_cpu.memory[0x0200] = 0xfe  # INC instruction
        setup_cpu.memory[0x0201] = 0x45
        setup_cpu.memory[0x0202] = 0x46
        setup_cpu.memory[0x4645 + 0x1e] = start_val
        setup_cpu.idx = 0x1e
        expected_zero_flag = end_val == 0
        expected_negative_flag = (end_val >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.memory[0x4645 + 0x1e] == end_val
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 7


@pytest.mark.usefixtures('setup_cpu')
class TestINX:

    @pytest.mark.parametrize('start_val, end_val', [(0x0, 0x1), (0x1, 0x2), (0xab, 0xac), (0xfe, 0xff), (0xff, 0x0)])
    def test_inx_implied(self, setup_cpu, start_val, end_val):
        setup_cpu.memory[0x0200] = 0xe8  # INX instruction
        setup_cpu.idx = start_val
        expected_zero_flag = end_val == 0
        expected_negative_flag = (end_val >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.idx == end_val
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 2


@pytest.mark.usefixtures('setup_cpu')
class TestINY:

    @pytest.mark.parametrize('start_val, end_val', [(0x0, 0x1), (0x1, 0x2), (0xab, 0xac), (0xfe, 0xff), (0xff, 0x0)])
    def test_iny_implied(self, setup_cpu, start_val, end_val):
        setup_cpu.memory[0x0200] = 0xc8  # INY instruction
        setup_cpu.idy = start_val
        expected_zero_flag = end_val == 0
        expected_negative_flag = (end_val >> 7) == 1
        setup_cpu.execute(1)
        assert setup_cpu.idy == end_val
        assert setup_cpu.ps['zero_flag'] == expected_zero_flag
        assert setup_cpu.ps['negative_flag'] == expected_negative_flag
        assert setup_cpu.clock.total_clock_cycles == 2
