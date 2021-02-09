import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestRTS:

    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x6), (0x20, 0x1), (0xff, 0xfd), (0xff, 0xfe)])
    @pytest.mark.parametrize('sp', [0x0101, 0x01fd, 0x01aa, 0x01fd])
    def test_rts_implied(self, setup_cpu, address_fst, address_snd, sp):
        setup_cpu.memory[0x200] = 0x60
        setup_cpu.sp = sp
        setup_cpu.memory[setup_cpu.sp + 2] = address_snd
        setup_cpu.memory[setup_cpu.sp + 1] = address_fst
        target_address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.execute(1)
        assert setup_cpu.pc == target_address + 1
        assert setup_cpu.sp == sp + 2
        assert setup_cpu.clock.total_clock_cycles == 6
