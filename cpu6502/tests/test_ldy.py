import pytest


class TestLDX:

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    def test_ldx_immediate(self, setup_cpu, value, zero_flag, neg_flag):
        setup_cpu.memory[0x0200] = 0xa0  # LDX instruction
        setup_cpu.memory[0x0201] = value
        setup_cpu.execute(1)
        assert setup_cpu.ldy == value
        assert setup_cpu.clock.total_clock_cycles == 2
        assert setup_cpu.ps['zero_flag'] == zero_flag
        assert setup_cpu.ps['negative_flag'] == neg_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    @pytest.mark.parametrize('zp_address', [0x0, 0x1, 0xff])
    def test_ldx_zero_page(self, setup_cpu, value, zero_flag, neg_flag, zp_address):
        setup_cpu.memory[0x0200] = 0xa4  # LDX instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.memory[zp_address] = value
        setup_cpu.execute(1)
        assert setup_cpu.ldy == value
        assert setup_cpu.clock.total_clock_cycles == 3
        assert setup_cpu.ps['zero_flag'] == zero_flag
        assert setup_cpu.ps['negative_flag'] == neg_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    @pytest.mark.parametrize('zp_address', [0x0, 0x1, 0xef])
    @pytest.mark.parametrize('idx', [0x0, 0x1, 0x10])
    def test_ldx_zero_page_y(self, setup_cpu, value, zero_flag, neg_flag, zp_address, idx):
        setup_cpu.memory[0x0200] = 0xb4  # LDX instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.memory[zp_address + idx] = value
        setup_cpu.idy = idx
        setup_cpu.execute(1)
        assert setup_cpu.ldy == value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['zero_flag'] == zero_flag
        assert setup_cpu.ps['negative_flag'] == neg_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x00, 0x01), (0x01, 0xfe), (0xfa, 0xa1)])
    def test_ldx_absolute(self, setup_cpu, value, zero_flag, neg_flag, address_snd, address_fst):
        setup_cpu.memory[0x0200] = 0xac  # LDX instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address] = value
        setup_cpu.execute(1)
        assert setup_cpu.ldy == value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['zero_flag'] == zero_flag
        assert setup_cpu.ps['negative_flag'] == neg_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x00, 0x01), (0x01, 0xac), (0xfa, 0xa1)])
    @pytest.mark.parametrize('idx', [0x0, 0x1, 0x10])
    def test_ldx_absolute_y_no_page_crossed(self, setup_cpu, value, neg_flag, zero_flag, address_snd, address_fst, idx):
        setup_cpu.memory[0x0200] = 0xbc  # LDX instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idx] = value
        setup_cpu.execute(1)
        assert setup_cpu.ldy == value
        assert setup_cpu.clock.total_clock_cycles == 4
        assert setup_cpu.ps['zero_flag'] == zero_flag
        assert setup_cpu.ps['negative_flag'] == neg_flag

    @pytest.mark.parametrize('value, zero_flag, neg_flag', [(0x1, False, False),
                                                            (0x20, False, False),
                                                            (0xff, False, True),
                                                            (0x0, True, False)])
    @pytest.mark.parametrize('address_fst, address_snd', [(0x00, 0xff), (0x01, 0xfe), (0xfa, 0xf1)])
    @pytest.mark.parametrize('idx', [0x0f, 0x10])
    def test_ldx_absolute_y_page_crossed(self, setup_cpu, value, neg_flag, zero_flag, address_snd, address_fst, idx):
        setup_cpu.memory[0x0200] = 0xbc  # LDX instruction
        setup_cpu.memory[0x0201] = address_snd
        setup_cpu.memory[0x0202] = address_fst
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address + idx] = value
        setup_cpu.execute(1)
        assert setup_cpu.ldy == value
        assert setup_cpu.clock.total_clock_cycles == 5
        assert setup_cpu.ps['zero_flag'] == zero_flag
        assert setup_cpu.ps['negative_flag'] == neg_flag


