import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestBRK:

    @pytest.mark.parametrize('pc_fst, pc_snd', [(0x0, 0x0), (0x0, 0x1), (0x02, 0x0), (0x0, 0xff), (0xff, 0xee), (0xff, 0xfa)])
    @pytest.mark.parametrize('ps, bin_ps', [({
                                                 'carry_flag': True,
                                                 'zero_flag': True,
                                                 'interrupt_disable': False,
                                                 'decimal_mode': True,
                                                 'break_command': False,
                                                 'overflow_flag': False,
                                                 'negative_flag': True
                                             }, 0b01101001),
                                            ({
                                                 'carry_flag': False,
                                                 'zero_flag': False,
                                                 'interrupt_disable': False,
                                                 'decimal_mode': False,
                                                 'break_command': False,
                                                 'overflow_flag': False,
                                                 'negative_flag': False
                                             }, 0b00000000),
                                            ({
                                                 'carry_flag': True,
                                                 'zero_flag': True,
                                                 'interrupt_disable': True,
                                                 'decimal_mode': True,
                                                 'break_command': False,
                                                 'overflow_flag': True,
                                                 'negative_flag': True
                                             }, 0b01111011)])
    @pytest.mark.parametrize('iv_fst, iv_snd', (0x00, 0x00), (0xa1, 0x44), (0xff, 0x0f))
    def test_brk_implied(self, setup_cpu, pc_fst, pc_snd, ps, bin_ps, iv_fst, iv_snd):
        pc = pc_snd + (pc_fst << 8)
        setup_cpu.memory[pc] = 0x0  # BRK instruction
        setup_cpu.memory[0xfffe] = iv_snd
        setup_cpu.memory[0xffff] = iv_fst  # IRQ interrupt vector
        setup_cpu.ps = ps
        setup_cpu.pc = pc
        setup_cpu.execute(1)
        assert setup_cpu.memory[setup_cpu.sp] == bin_ps
        assert setup_cpu.memory[setup_cpu.sp + 1] == pc_snd
        assert setup_cpu.memory[setup_cpu.sp + 2] == pc_fst
        assert setup_cpu.ps['break_flag']
        assert setup_cpu.clock.total_clock_cycles == 7


@pytest.mark.usefixtures('setup_cpu')
class TestNOP:

    @pytest.mark.parametrize('pc', [0x0000, 0x0001, 0x0fff, 0xffff])
    def test_nop_implied(self, setup_cpu, pc):
        setup_cpu.pc = pc
        setup_cpu.memory[setup_cpu.pc] = 0xea  # NOP instruction
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + 2
        assert setup_cpu.clock.total_clock_cycles == 2


@pytest.mark.usefixtures('setup_cpu')
class TestRTI:

    @pytest.mark.parametrize('pc_fst, pc_snd',
                             [(0x0, 0x0), (0x0, 0x1), (0x02, 0x0), (0x0, 0xff), (0xff, 0xee), (0xff, 0xfa)])
    @pytest.mark.parametrize('ps, bin_ps', [({
                                                 'carry_flag': True,
                                                 'zero_flag': True,
                                                 'interrupt_disable': False,
                                                 'decimal_mode': True,
                                                 'break_command': False,
                                                 'overflow_flag': False,
                                                 'negative_flag': True
                                             }, 0b01101001),
                                            ({
                                                 'carry_flag': False,
                                                 'zero_flag': False,
                                                 'interrupt_disable': False,
                                                 'decimal_mode': False,
                                                 'break_command': False,
                                                 'overflow_flag': False,
                                                 'negative_flag': False
                                             }, 0b00000000),
                                            ({
                                                 'carry_flag': True,
                                                 'zero_flag': True,
                                                 'interrupt_disable': True,
                                                 'decimal_mode': True,
                                                 'break_command': False,
                                                 'overflow_flag': True,
                                                 'negative_flag': True
                                             }, 0b01111011)])
    def test_rti_implied(self, setup_cpu, pc_fst, pc_snd, ps, bin_ps):
        setup_cpu.memory[0x0200] = 0x40  # RTI instruction
        setup_cpu.sp = 0x60
        setup_cpu.memory[0x60] = bin_ps
        setup_cpu.memory[0x59] = pc_snd
        setup_cpu.memory[0x58] = pc_fst
        expected_pc = pc_snd + (pc_fst << 8)
        setup_cpu.execute(1)
        assert setup_cpu.pc == expected_pc
        assert setup_cpu.ps == ps
        assert setup_cpu.clock.total_clock_cycles == 6
