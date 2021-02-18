import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestPHA:

    @pytest.mark.parametrize('acc', [0x0, 0x1, 0xfe, 0xff, 0x20])
    @pytest.mark.parametrize('sp', [0x1, 0xfe, 0xff, 0x10])
    def test_pha_implied(self, setup_cpu, acc, sp):
        setup_cpu.sp = sp
        setup_cpu.acc = acc
        setup_cpu.memory[0x0200] = 0x48  # PHA instruction
        setup_cpu.execute(1)
        assert setup_cpu.sp == sp - 1
        assert setup_cpu.memory[sp + 0x0100] == setup_cpu.acc
        assert setup_cpu.clock.total_clock_cycles == 3


@pytest.mark.usefixtures('setup_cpu')
class TestPHP:

    @pytest.mark.parametrize('ps', [{
        'carry_flag': True,
        'zero_flag': True,
        'interrupt_disable': False,
        'decimal_mode': True,
        'break_command': False,
        'overflow_flag': False,
        'negative_flag': True
    },
        {
            'carry_flag': False,
            'zero_flag': False,
            'interrupt_disable': False,
            'decimal_mode': False,
            'break_command': False,
            'overflow_flag': False,
            'negative_flag': False
        }, {
            'carry_flag': True,
            'zero_flag': True,
            'interrupt_disable': True,
            'decimal_mode': True,
            'break_command': True,
            'overflow_flag': True,
            'negative_flag': True
        }])
    @pytest.mark.parametrize('sp', [0x1, 0xfe, 0xff, 0x10])
    def test_php_implied(self, setup_cpu, sp, ps):
        setup_cpu.sp = sp
        setup_cpu.ps = ps
        setup_cpu.memory[0x0200] = 0x08  # PHP instruction
        setup_cpu.execute(1)
        assert setup_cpu.sp == sp - 1
        assert setup_cpu.memory[sp + 0x0100] == setup_cpu.convert_ps_to_binary()


@pytest.mark.usefixtures('setup_cpu')
class TestPLA:

    @pytest.mark.parametrize('value', [0x0, 0x1, 0xfe, 0xff, 0x20])
    @pytest.mark.parametrize('sp', [0x1, 0x00, 0xfe, 0x10])
    def test_pla_implied(self, setup_cpu, sp, value):
        setup_cpu.sp = sp
        setup_cpu.memory[sp + 0x0100] = value
        setup_cpu.memory[0x0200] = 0x68  # PLA instruction
        setup_cpu.execute(1)
        assert setup_cpu.sp == sp + 1
        assert setup_cpu.acc == value
        assert setup_cpu.clock.total_clock_cycles == 4


@pytest.mark.usefixtures('setup_cpu')
class TestPLP:

    @pytest.mark.parametrize('result, bin_ps', [({
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
                                                     'break_command': True,
                                                     'overflow_flag': True,
                                                     'negative_flag': True
                                                 }, 0b01111111)])
    @pytest.mark.parametrize('sp', [0x1, 0x00, 0xfe, 0x10])
    def test_plp_implied(self, setup_cpu, bin_ps, result, sp):
        setup_cpu.memory[0x0200] = 0x28  # PLP instruction
        setup_cpu.sp = sp
        setup_cpu.memory[sp + 0x100] = bin_ps
        setup_cpu.execute(1)
        assert setup_cpu.sp == sp + 1
        assert setup_cpu.ps == result
        assert setup_cpu.clock.total_clock_cycles == 4
