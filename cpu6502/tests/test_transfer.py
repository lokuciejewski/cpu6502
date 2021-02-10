import numpy as np
import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestTAX:

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_tax_implied(self, setup_cpu, value, neg_flag, zero_flag):
        setup_cpu.acc = value
        setup_cpu.memory[0x0200] = 0xaa  # TAX instruction
        setup_cpu.execute(1)
        assert setup_cpu.idx == value
        assert setup_cpu.clock.total_clock_cycles == 2
        assert setup_cpu.ps['negative_flag'] == neg_flag
        assert setup_cpu.ps['zero_flag'] == zero_flag


@pytest.mark.usefixtures('setup_cpu')
class TestTAY:

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_tax_implied(self, setup_cpu, value, neg_flag, zero_flag):
        setup_cpu.acc = value
        setup_cpu.memory[0x0200] = 0xa8  # TAY instruction
        setup_cpu.execute(1)
        assert setup_cpu.idy == value
        assert setup_cpu.clock.total_clock_cycles == 2
        assert setup_cpu.ps['negative_flag'] == neg_flag
        assert setup_cpu.ps['zero_flag'] == zero_flag


@pytest.mark.usefixtures('setup_cpu')
class TestTXA:

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_tax_implied(self, setup_cpu, value, neg_flag, zero_flag):
        setup_cpu.idx = value
        setup_cpu.memory[0x0200] = 0x8a  # TXA instruction
        setup_cpu.execute(1)
        assert setup_cpu.acc == value
        assert setup_cpu.clock.total_clock_cycles == 2
        assert setup_cpu.ps['negative_flag'] == neg_flag
        assert setup_cpu.ps['zero_flag'] == zero_flag


@pytest.mark.usefixtures('setup_cpu')
class TestTYA:

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_tax_implied(self, setup_cpu, value, neg_flag, zero_flag):
        setup_cpu.idy = value
        setup_cpu.memory[0x0200] = 0x98  # TYA instruction
        setup_cpu.execute(1)
        assert setup_cpu.acc == value
        assert setup_cpu.clock.total_clock_cycles == 2
        assert setup_cpu.ps['negative_flag'] == neg_flag
        assert setup_cpu.ps['zero_flag'] == zero_flag


@pytest.mark.usefixtures('setup_cpu')
class TestTSX:

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x00, True, False),
                                                            (0xff, False, True),
                                                            (0x01, False, False)])
    def test_tsx_implied(self, setup_cpu, value, neg_flag, zero_flag):
        setup_cpu.sp = value
        setup_cpu.memory[0x0200] = 0xba  # TSX instruction
        setup_cpu.execute(1)
        assert setup_cpu.idx == value
        assert setup_cpu.clock.total_clock_cycles == 2
        assert setup_cpu.ps['negative_flag'] == neg_flag
        assert setup_cpu.ps['zero_flag'] == zero_flag


@pytest.mark.usefixtures('setup_cpu')
class TestTXS:

    @pytest.mark.parametrize('value', [0x0, 0x1, 0x10, 0xff])
    def test_tsx_implied(self, setup_cpu, value):
        setup_cpu.idx = value
        setup_cpu.memory[0x0200] = 0x9a  # TXS instruction
        setup_cpu.execute(1)
        assert setup_cpu.sp == value
        assert setup_cpu.clock.total_clock_cycles == 2
