import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestJSR:

    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x1), (0x20, 0x1), (0xff, 0xfd), (0xff, 0xfe)])
    @pytest.mark.parametrize('start_address_fst, start_address_snd',
                             [(0x0, 0x3), (0x20, 0x1), (0xff, 0xfd), (0xff, 0xfc)])
    def test_jsr_absolute(self, setup_cpu, address_fst, address_snd, start_address_fst, start_address_snd):
        start_address = start_address_snd + (start_address_fst << 8)
        setup_cpu.pc = start_address
        setup_cpu.memory[start_address] = 0x20  # JSR instruction
        setup_cpu.memory[start_address + 1] = address_snd
        setup_cpu.memory[start_address + 2] = address_fst
        setup_cpu.execute(1)
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        assert setup_cpu.pc == address
        stored_address = setup_cpu.memory[setup_cpu.sp + 2] + (setup_cpu.memory[setup_cpu.sp + 1] << 8)
        assert stored_address == start_address + 2  # To compensate for the word reading
        assert setup_cpu.clock.total_clock_cycles == 6



