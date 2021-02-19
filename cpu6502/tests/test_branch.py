import pytest


@pytest.mark.usefixtures('setup_cpu')
class TestBCC:

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0x105, 0xff00, 0xfe12])
    @pytest.mark.parametrize('offset', [0x1, 0x5, 0x10])
    def test_bcc_no_page_crossed_successful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0x90  # BCC instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['carry_flag'] = False
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + offset
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0x105, 0xff00, 0xfe12])
    @pytest.mark.parametrize('offset', [0xff, 0xfe])
    def test_bcc_page_crossed_successful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0x90  # BCC instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['carry_flag'] = False
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + offset
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0xfe12])
    @pytest.mark.parametrize('offset', [0xff, 0x01])
    def test_bcc_unsuccessful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0x90  # BCC instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['carry_flag'] = True
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + 2
        assert setup_cpu.clock.total_clock_cycles == 2


@pytest.mark.usefixtures('setup_cpu')
class TestBCS:

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0x105, 0xff00, 0xfe12])
    @pytest.mark.parametrize('offset', [0x1, 0x5, 0x10])
    def test_bcs_no_page_crossed_successful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0xb0  # BCS instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['carry_flag'] = True
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + offset
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0x105, 0xff00, 0xfe12])
    @pytest.mark.parametrize('offset', [0xff, 0xfe])
    def test_bcs_page_crossed_successful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0xb0  # BCS instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['carry_flag'] = True
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + offset
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0xfe12])
    @pytest.mark.parametrize('offset', [0xff, 0x01])
    def test_bcs_unsuccessful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0xb0  # BCS instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['carry_flag'] = False
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + 2
        assert setup_cpu.clock.total_clock_cycles == 2


@pytest.mark.usefixtures('setup_cpu')
class TestBEQ:

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0x105, 0xff00, 0xfe12])
    @pytest.mark.parametrize('offset', [0x1, 0x5, 0x10])
    def test_beq_no_page_crossed_successful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0xf0  # BEQ instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['zero_flag'] = True
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + offset
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0x105, 0xff00, 0xfe12])
    @pytest.mark.parametrize('offset', [0xff, 0xfe])
    def test_beq_page_crossed_successful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0xf0  # BEQ instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['zero_flag'] = True
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + offset
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0xfe12])
    @pytest.mark.parametrize('offset', [0xff, 0x01])
    def test_beq_unsuccessful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0xf0  # BEQ instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['zero_flag'] = False
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + 2
        assert setup_cpu.clock.total_clock_cycles == 2


@pytest.mark.usefixtures('setup_cpu')
class TestBMI:

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0x105, 0xff00, 0xfe12])
    @pytest.mark.parametrize('offset', [0x1, 0x5, 0x10])
    def test_bmi_no_page_crossed_successful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0xe0  # BMI instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['negative_flag'] = True
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + offset
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0x105, 0xff00, 0xfe12])
    @pytest.mark.parametrize('offset', [0xff, 0xfe])
    def test_bmi_page_crossed_successful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0xe0  # BMI instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['negative_flag'] = True
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + offset
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0xfe12])
    @pytest.mark.parametrize('offset', [0xff, 0x01])
    def test_bmi_unsuccessful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0xe0  # BMI instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['negative_flag'] = False
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + 2
        assert setup_cpu.clock.total_clock_cycles == 2


@pytest.mark.usefixtures('setup_cpu')
class TestBNE:

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0x105, 0xff00, 0xfe12])
    @pytest.mark.parametrize('offset', [0x1, 0x5, 0x10])
    def test_bne_no_page_crossed_successful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0xd0  # BNE instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['zero_flag'] = False
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + offset
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0x105, 0xff00, 0xfe12])
    @pytest.mark.parametrize('offset', [0xff, 0xfe])
    def test_bne_page_crossed_successful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0xd0  # BNE instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['zero_flag'] = False
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + offset
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0xfe12])
    @pytest.mark.parametrize('offset', [0xff, 0x01])
    def test_bne_unsuccessful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0xd0  # BNE instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['zero_flag'] = True
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + 2
        assert setup_cpu.clock.total_clock_cycles == 2


@pytest.mark.usefixtures('setup_cpu')
class TestBPL:

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0x105, 0xff00, 0xfe12])
    @pytest.mark.parametrize('offset', [0x1, 0x5, 0x10])
    def test_bpl_no_page_crossed_successful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0x10  # BPL instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['negative_flag'] = False
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + offset
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0x105, 0xff00, 0xfe12])
    @pytest.mark.parametrize('offset', [0xff, 0xfe])
    def test_bpl_page_crossed_successful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0x10  # BPL instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['negative_flag'] = False
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + offset
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0xfe12])
    @pytest.mark.parametrize('offset', [0xff, 0x01])
    def test_bpl_unsuccessful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0x10  # BPL instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['negative_flag'] = True
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + 2
        assert setup_cpu.clock.total_clock_cycles == 2


@pytest.mark.usefixtures('setup_cpu')
class TestBVC:

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0x105, 0xff00, 0xfe12])
    @pytest.mark.parametrize('offset', [0x1, 0x5, 0x10])
    def test_bvc_no_page_crossed_successful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0x50  # BVC instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['overflow_flag'] = False
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + offset
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0x105, 0xff00, 0xfe12])
    @pytest.mark.parametrize('offset', [0xff, 0xfe])
    def test_bvc_page_crossed_successful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0x50  # BVC instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['overflow_flag'] = False
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + offset
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0xfe12])
    @pytest.mark.parametrize('offset', [0xff, 0x01])
    def test_bvc_unsuccessful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0x50  # BVC instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['overflow_flag'] = True
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + 2
        assert setup_cpu.clock.total_clock_cycles == 2


@pytest.mark.usefixtures('setup_cpu')
class TestBVS:

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0x105, 0xff00, 0xfe12])
    @pytest.mark.parametrize('offset', [0x1, 0x5, 0x10])
    def test_bvs_no_page_crossed_successful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0x70  # BVS instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['overflow_flag'] = True
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + offset
        assert setup_cpu.clock.total_clock_cycles == 3

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0x105, 0xff00, 0xfe12])
    @pytest.mark.parametrize('offset', [0xff, 0xfe])
    def test_bvs_page_crossed_successful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0x70  # BVS instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['overflow_flag'] = True
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + offset
        assert setup_cpu.clock.total_clock_cycles == 4

    @pytest.mark.parametrize('pc', [0x0, 0x1, 0xfe12])
    @pytest.mark.parametrize('offset', [0xff, 0x01])
    def test_bvs_unsuccessful(self, setup_cpu, pc, offset):
        setup_cpu.memory[0x0200] = 0x70  # BVS instruction
        setup_cpu.memory[0x0201] = offset
        setup_cpu.pc = pc
        setup_cpu.ps['overflow_flag'] = False
        setup_cpu.execute(1)
        assert setup_cpu.pc == pc + 2
        assert setup_cpu.clock.total_clock_cycles == 2
