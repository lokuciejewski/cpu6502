import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestLDA:

    @pytest.mark.parametrize('value', [0x1, 0x20, 0xff, 0x0, 0x12])
    def test_lda_immediate(self, setup_cpu, value):
        setup_cpu.memory[0x0200] = 0xa9  # LDA instruction
        setup_cpu.memory[0x0201] = value
        setup_cpu.execute(1)
        assert setup_cpu.acc == value
        assert setup_cpu.clock.total_clock_cycles == 2

    @pytest.mark.parametrize('zp_address', [0x01, 0x10, 0xfe, 0xff, 0xf1])
    @pytest.mark.parametrize('value', [0x01, 0x00, 0xfe, 0xff, 0xe1])
    def test_lda_zero_page(self, setup_cpu, zp_address, value):
        setup_cpu.memory[0x0200] = 0xa5  # LDA instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.memory[zp_address] = value
        setup_cpu.execute(1)
        assert setup_cpu.acc == value
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('zp_address', [0x01, 0x00, 0xfe, 0xff])
    @pytest.mark.parametrize('x_index_value', [0x01, 0xff, 0x10, 0xfe])
    @pytest.mark.parametrize('value', [0x01, 0x00, 0xfe, 0xff])
    def test_lda_zero_page_x(self, setup_cpu, zp_address, x_index_value, value):
        setup_cpu.memory[0x0200] = 0xb5  # LDA instruction
        setup_cpu.memory[0x0201] = zp_address
        setup_cpu.memory[zp_address + x_index_value] = value
        setup_cpu.idx = x_index_value
        setup_cpu.execute(1)
        assert setup_cpu.acc == value
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('address_fst, address_snd', [(0x00, 0x01), (0xff, 0xff), (0x00, 0x00), (0xfa, 0xa1)])
    @pytest.mark.parametrize('value', [0x10, 0xff, 0x00, 0x01])
    def test_lda_absolute(self, setup_cpu, address_fst, address_snd, value):
        setup_cpu.memory[0x0200] = 0xad  # LDA instruction
        setup_cpu.memory[0x0201] = address_fst
        setup_cpu.memory[0x0202] = address_snd
        address = address_fst + (address_snd << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address] = value
        setup_cpu.execute(1)
        assert setup_cpu.acc == value
        assert setup_cpu.clock.total_clock_cycles == 4

