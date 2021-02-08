import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestJMP:

    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x1), (0x0, 0x1), (0xff, 0xff), (0xff, 0xfe)])
    def test_jmp_absolute(self, setup_cpu, address_fst, address_snd):
        setup_cpu.memory[0x200] = 0x4c  # JMP instruction
        setup_cpu.memory[0x201] = address_snd
        setup_cpu.memory[0x202] = address_fst
        setup_cpu.execute(1)
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        assert setup_cpu.pc == address
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x1), (0x0, 0x1), (0xff, 0xfe), (0xff, 0x00)])
    @pytest.mark.parametrize('jmp_address_fst, jmp_address_snd', [(0xff, 0x01), (0x01, 0xff), (0x10, 0x01)])
    def test_jmp_indirect(self, setup_cpu, address_fst, address_snd, jmp_address_snd, jmp_address_fst):
        setup_cpu.memory[0x200] = 0x6c  # JMP instruction
        setup_cpu.memory[0x201] = address_snd
        setup_cpu.memory[0x202] = address_fst
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        setup_cpu.memory[address] = jmp_address_snd
        setup_cpu.memory[address + 1] = jmp_address_fst
        jmp_address = jmp_address_snd + (jmp_address_fst << 8)
        setup_cpu.execute(1)
        assert setup_cpu.pc == jmp_address
        assert setup_cpu.clock.total_clock_cycles == 5
