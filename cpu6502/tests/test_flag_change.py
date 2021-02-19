import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestCLC:

    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_clc_implied(self, setup_cpu, carry_flag):
        setup_cpu.memory[0x0200] = 0x18  # CLC instruction
        setup_cpu.ps['carry_flag'] = carry_flag
        setup_cpu.execute(1)
        assert not setup_cpu.ps['carry_flag']
        assert setup_cpu.clock.total_clock_cycles == 2


@pytest.mark.usefixtures('setup_cpu')
class TestCLD:

    @pytest.mark.parametrize('decimal_flag', [False, True])
    def test_cld_implied(self, setup_cpu, decimal_flag):
        setup_cpu.memory[0x0200] = 0xd8  # CLD instruction
        setup_cpu.ps['decimal_flag'] = decimal_flag
        setup_cpu.execute(1)
        assert not setup_cpu.ps['decimal_flag']
        assert setup_cpu.clock.total_clock_cycles == 2


@pytest.mark.usefixtures('setup_cpu')
class TestCLI:

    @pytest.mark.parametrize('interrupt_flag', [False, True])
    def test_cli_implied(self, setup_cpu, interrupt_flag):
        setup_cpu.memory[0x0200] = 0x58  # CLI instruction
        setup_cpu.ps['interrupt_flag'] = interrupt_flag
        setup_cpu.execute(1)
        assert not setup_cpu.ps['interrupt_flag']
        assert setup_cpu.clock.total_clock_cycles == 2


@pytest.mark.usefixtures('setup_cpu')
class TestCLV:

    @pytest.mark.parametrize('overflow_flag', [False, True])
    def test_clv_implied(self, setup_cpu, overflow_flag):
        setup_cpu.memory[0x0200] = 0xb8  # CLV instruction
        setup_cpu.ps['overflow_flag'] = overflow_flag
        setup_cpu.execute(1)
        assert not setup_cpu.ps['overflow_flag']
        assert setup_cpu.clock.total_clock_cycles == 2


@pytest.mark.usefixtures('setup_cpu')
class TestSEC:

    @pytest.mark.parametrize('carry_flag', [False, True])
    def test_sec_implied(self, setup_cpu, carry_flag):
        setup_cpu.memory[0x0200] = 0x38  # SEC instruction
        setup_cpu.ps['carry_flag'] = carry_flag
        setup_cpu.execute(1)
        assert setup_cpu.ps['carry_flag']
        assert setup_cpu.clock.total_clock_cycles == 2


@pytest.mark.usefixtures('setup_cpu')
class TestSED:

    @pytest.mark.parametrize('decimal_flag', [False, True])
    def test_sed_implied(self, setup_cpu, decimal_flag):
        setup_cpu.memory[0x0200] = 0xf8  # SED instruction
        setup_cpu.ps['decimal_flag'] = decimal_flag
        setup_cpu.execute(1)
        assert setup_cpu.ps['decimal_flag']
        assert setup_cpu.clock.total_clock_cycles == 2


@pytest.mark.usefixtures('setup_cpu')
class TestSEI:

    @pytest.mark.parametrize('interrupt_flag', [False, True])
    def test_cli_implied(self, setup_cpu, interrupt_flag):
        setup_cpu.memory[0x0200] = 0x78  # SEI instruction
        setup_cpu.ps['interrupt_flag'] = interrupt_flag
        setup_cpu.execute(1)
        assert setup_cpu.ps['interrupt_flag']
        assert setup_cpu.clock.total_clock_cycles == 2
