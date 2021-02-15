import numpy as np
import pytest


# TODO: Add flag testing to all lda tests
@pytest.mark.usefixtures('setup_cpu')
class TestLDA:

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_lda_immediate(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.memory[0x0200] = 0xa9  # LDA instruction
        setup_cpu.memory[0x0201] = value
        setup_cpu.execute(1)
        assert setup_cpu.acc == value
        assert setup_cpu.clock.total_clock_cycles == 2
        assert setup_cpu.ps['negative_flag'] == neg_flag
        assert setup_cpu.ps['zero_flag'] == zero_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_lda_zero_page(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.memory[0x0200] = 0xa5  # LDA instruction
        setup_cpu.memory[0x0201] = 0xa0  # Example zp address
        setup_cpu.memory[0xa0] = value
        setup_cpu.execute(1)
        assert setup_cpu.acc == value
        assert setup_cpu.clock.total_clock_cycles == 3
        assert setup_cpu.ps['negative_flag'] == neg_flag
        assert setup_cpu.ps['zero_flag'] == zero_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_lda_zero_page_x(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.memory[0x0200] = 0xb5  # LDA instruction
        setup_cpu.memory[0x0201] = 0xa0
        setup_cpu.memory[0xa0 + 0x10] = value
        setup_cpu.idx = 0x10  # Example idx value
        setup_cpu.execute(1)
        assert setup_cpu.acc == value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['negative_flag'] == neg_flag
        assert setup_cpu.ps['zero_flag'] == zero_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_lda_absolute(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.memory[0x0200] = 0xad  # LDA instruction
        setup_cpu.memory[0x0201] = 0x10
        setup_cpu.memory[0x0202] = 0xaa  # Example address
        setup_cpu.memory[0xaa10] = value
        setup_cpu.execute(1)
        assert setup_cpu.acc == value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['negative_flag'] == neg_flag
        assert setup_cpu.ps['zero_flag'] == zero_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_lda_absolute_x_no_page_crossing(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.idx = 0x1
        setup_cpu.memory[0x0200] = 0xbd  # LDA instruction
        setup_cpu.memory[0x0201] = 0x10
        setup_cpu.memory[0x0202] = 0xaa
        setup_cpu.memory[0xaa10 + setup_cpu.idx] = value
        setup_cpu.execute(1)
        assert setup_cpu.acc == value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['negative_flag'] == neg_flag
        assert setup_cpu.ps['zero_flag'] == zero_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_lda_absolute_x_page_crossing(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.idx = 0xff
        setup_cpu.memory[0x0200] = 0xbd  # LDA instruction
        setup_cpu.memory[0x0201] = 0x10
        setup_cpu.memory[0x0202] = 0xaa
        setup_cpu.memory[0xaa10 + setup_cpu.idx] = value
        setup_cpu.execute(1)
        assert setup_cpu.acc == value
        assert setup_cpu.clock.total_clock_cycles == 5
        assert setup_cpu.ps['negative_flag'] == neg_flag
        assert setup_cpu.ps['zero_flag'] == zero_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_lda_absolute_y_no_page_crossing(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.idy = 0x1
        setup_cpu.memory[0x0200] = 0xb9  # LDA instruction
        setup_cpu.memory[0x0201] = 0x2a
        setup_cpu.memory[0x0202] = 0xbb
        setup_cpu.memory[0xbb2a + setup_cpu.idy] = value
        setup_cpu.execute(1)
        assert setup_cpu.acc == value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['negative_flag'] == neg_flag
        assert setup_cpu.ps['zero_flag'] == zero_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_lda_absolute_y_page_crossing(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.idy = 0xff
        setup_cpu.memory[0x0200] = 0xb9  # LDA instruction
        setup_cpu.memory[0x0201] = 0x2a
        setup_cpu.memory[0x0202] = 0xbb
        setup_cpu.memory[0xbb2a + setup_cpu.idy] = value
        setup_cpu.execute(1)
        assert setup_cpu.acc == value
        assert setup_cpu.clock.total_clock_cycles == 5
        assert setup_cpu.ps['negative_flag'] == neg_flag
        assert setup_cpu.ps['zero_flag'] == zero_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_lda_indexed_indirect(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.idx = 0x5a
        setup_cpu.memory[0x0200] = 0xa1  # LDA instruction
        setup_cpu.memory[0x201] = 0xb8
        setup_cpu.memory[np.ubyte(0xb8 + setup_cpu.idx)] = 0x88
        setup_cpu.memory[np.ubyte(0xb8 + setup_cpu.idx) + 1] = 0x7a
        setup_cpu.memory[0x7a88] = value
        setup_cpu.execute(1)
        assert setup_cpu.acc == value
        assert setup_cpu.clock.total_clock_cycles == 6
        assert setup_cpu.ps['negative_flag'] == neg_flag
        assert setup_cpu.ps['zero_flag'] == zero_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_lda_indirect_indexed_page_crossed(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.idy = 0xff
        setup_cpu.memory[0x0200] = 0xb1  # LDA instruction
        setup_cpu.memory[0x201] = 0x00ae
        setup_cpu.memory[0x00ae] = 0x37
        setup_cpu.memory[0x00af] = 0x21
        setup_cpu.memory[0x2137 + 0xff] = value
        setup_cpu.execute(1)
        assert setup_cpu.acc == value
        assert setup_cpu.clock.total_clock_cycles == 6
        assert setup_cpu.ps['negative_flag'] == neg_flag
        assert setup_cpu.ps['zero_flag'] == zero_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_lda_indirect_indexed_no_page_crossed(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.idy = 0x01
        setup_cpu.memory[0x0200] = 0xb1  # LDA instruction
        setup_cpu.memory[0x201] = 0x00ae
        setup_cpu.memory[0x00ae] = 0x37
        setup_cpu.memory[0x00af] = 0x21
        setup_cpu.memory[0x2137 + 0x01] = value
        setup_cpu.execute(1)
        assert setup_cpu.acc == value
        assert setup_cpu.clock.total_clock_cycles == 5
        assert setup_cpu.ps['negative_flag'] == neg_flag
        assert setup_cpu.ps['zero_flag'] == zero_flag


@pytest.mark.usefixtures('setup_cpu')
class TestLDX:

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_ldx_immediate(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.memory[0x0200] = 0xa2  # LDX instruction
        setup_cpu.memory[0x0201] = value
        setup_cpu.execute(1)
        assert setup_cpu.idx == value
        assert setup_cpu.clock.total_clock_cycles == 2
        assert setup_cpu.ps['zero_flag'] == zero_flag
        assert setup_cpu.ps['negative_flag'] == neg_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_ldx_zero_page(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.memory[0x0200] = 0xa6  # LDX instruction
        setup_cpu.memory[0x0201] = 0x8e
        setup_cpu.memory[0x8e] = value
        setup_cpu.execute(1)
        assert setup_cpu.idx == value
        assert setup_cpu.clock.total_clock_cycles == 3
        assert setup_cpu.ps['zero_flag'] == zero_flag
        assert setup_cpu.ps['negative_flag'] == neg_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_ldx_zero_page_y(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.memory[0x0200] = 0xb6  # LDX instruction
        setup_cpu.memory[0x0201] = 0x8e
        setup_cpu.memory[0x8e + 0x04] = value
        setup_cpu.idy = 0x04
        setup_cpu.execute(1)
        assert setup_cpu.idx == value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['zero_flag'] == zero_flag
        assert setup_cpu.ps['negative_flag'] == neg_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_ldx_absolute(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.memory[0x0200] = 0xae  # LDX instruction
        setup_cpu.memory[0x0201] = 0x69
        setup_cpu.memory[0x0202] = 0x42
        setup_cpu.memory[0x4269] = value
        setup_cpu.execute(1)
        assert setup_cpu.idx == value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['zero_flag'] == zero_flag
        assert setup_cpu.ps['negative_flag'] == neg_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_ldx_absolute_y_no_page_crossed(self, setup_cpu, value, neg_flag, zero_flag):
        setup_cpu.memory[0x0200] = 0xbe  # LDX instruction
        setup_cpu.memory[0x0201] = 0xaa
        setup_cpu.memory[0x0202] = 0xbb
        setup_cpu.idy = 0x01
        setup_cpu.memory[0xbbaa + 0x01] = value
        setup_cpu.execute(1)
        assert setup_cpu.idx == value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['zero_flag'] == zero_flag
        assert setup_cpu.ps['negative_flag'] == neg_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_ldx_absolute_y_page_crossed(self, setup_cpu, value, neg_flag, zero_flag):
        setup_cpu.memory[0x0200] = 0xbe  # LDX instruction
        setup_cpu.memory[0x0201] = 0xfa
        setup_cpu.memory[0x0202] = 0xaa
        setup_cpu.idy = 0xff
        setup_cpu.memory[0xaafa + 0xff] = value
        setup_cpu.execute(1)
        assert setup_cpu.idx == value
        assert setup_cpu.clock.total_clock_cycles == 5
        assert setup_cpu.ps['zero_flag'] == zero_flag
        assert setup_cpu.ps['negative_flag'] == neg_flag


@pytest.mark.usefixtures('setup_cpu')
class TestLDY:

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_ldy_immediate(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.memory[0x0200] = 0xa0  # LDY instruction
        setup_cpu.memory[0x0201] = value
        setup_cpu.execute(1)
        assert setup_cpu.idy == value
        assert setup_cpu.clock.total_clock_cycles == 2
        assert setup_cpu.ps['zero_flag'] == zero_flag
        assert setup_cpu.ps['negative_flag'] == neg_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_ldy_zero_page(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.memory[0x0200] = 0xa4  # LDY instruction
        setup_cpu.memory[0x0201] = 0x11
        setup_cpu.memory[0x11] = value
        setup_cpu.execute(1)
        assert setup_cpu.idy == value
        assert setup_cpu.clock.total_clock_cycles == 3
        assert setup_cpu.ps['zero_flag'] == zero_flag
        assert setup_cpu.ps['negative_flag'] == neg_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_ldy_zero_page_x(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.memory[0x0200] = 0xb4  # LDY instruction
        setup_cpu.memory[0x0201] = 0x50
        setup_cpu.memory[0x50 + 0x29] = value
        setup_cpu.idx = 0x29
        setup_cpu.execute(1)
        assert setup_cpu.idy == value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['zero_flag'] == zero_flag
        assert setup_cpu.ps['negative_flag'] == neg_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_ldy_absolute(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.memory[0x0200] = 0xac  # LDY instruction
        setup_cpu.memory[0x0201] = 0x50
        setup_cpu.memory[0x0202] = 0xaa
        setup_cpu.memory[0xaa50] = value
        setup_cpu.execute(1)
        assert setup_cpu.idy == value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['zero_flag'] == zero_flag
        assert setup_cpu.ps['negative_flag'] == neg_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_ldy_absolute_x_no_page_crossed(self, setup_cpu, value, neg_flag, zero_flag):
        setup_cpu.memory[0x0200] = 0xbc  # LDY instruction
        setup_cpu.memory[0x0201] = 0x50
        setup_cpu.memory[0x0202] = 0xaa
        setup_cpu.memory[0xaa50 + 0x20] = value
        setup_cpu.idx = 0x20
        setup_cpu.execute(1)
        assert setup_cpu.idy == value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['zero_flag'] == zero_flag
        assert setup_cpu.ps['negative_flag'] == neg_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_ldy_absolute_x_page_crossed(self, setup_cpu, value, neg_flag, zero_flag):
        setup_cpu.memory[0x0200] = 0xbc  # LDY instruction
        setup_cpu.memory[0x0201] = 0x50
        setup_cpu.memory[0x0202] = 0xaa
        setup_cpu.memory[0xaa50 + 0xff] = value
        setup_cpu.idx = 0xff
        setup_cpu.execute(1)
        assert setup_cpu.idy == value
        assert setup_cpu.clock.total_clock_cycles == 5
        assert setup_cpu.ps['zero_flag'] == zero_flag
        assert setup_cpu.ps['negative_flag'] == neg_flag
