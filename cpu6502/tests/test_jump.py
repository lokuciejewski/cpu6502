import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestJMP:

    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x1), (0x20, 0x1), (0xff, 0xff), (0xff, 0xfe)])
    def test_jmp_absolute(self, setup_cpu, address_fst, address_snd):
        setup_cpu.memory[0x200] = 0x4c  # JMP instruction
        setup_cpu.memory[0x201] = address_snd
        setup_cpu.memory[0x202] = address_fst
        setup_cpu.execute(1)
        address = address_snd + (address_fst << 8)  # Little endian -> least significant byte first
        assert setup_cpu.pc == address
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('address_fst, address_snd', [(0x0, 0x1), (0x20, 0x1), (0xff, 0xfe), (0xff, 0x00)])
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
