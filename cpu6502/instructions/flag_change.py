import cpu6502.instructions


class CLC(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x18': self.implied
        }

    def implied(self):
        self.cpu.ps['carry_flag'] = False
        ~self.cpu.clock


class CLD(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xd8': self.implied
        }

    def implied(self):
        self.cpu.ps['decimal_flag'] = False
        ~self.cpu.clock


class CLI(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x58': self.implied
        }

    def implied(self):
        self.cpu.ps['interrupt_flag'] = False
        ~self.cpu.clock


class CLV(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xb8': self.implied
        }

    def implied(self):
        self.cpu.ps['overflow_flag'] = False
        ~self.cpu.clock


class SEC(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x38': self.implied
        }

    def implied(self):
        self.cpu.ps['carry_flag'] = True
        ~self.cpu.clock


class SED(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xf8': self.implied
        }

    def implied(self):
        self.cpu.ps['decimal_flag'] = True
        ~self.cpu.clock


class SEI(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x78': self.implied
        }

    def implied(self):
        self.cpu.ps['interrupt_flag'] = True
        ~self.cpu.clock
