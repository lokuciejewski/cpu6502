import cpu6502.instructions


class PHA(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x48': self.implied
        }

    def implied(self):
        self.cpu.push_byte_on_stack(self.cpu.acc)


class PHP(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x08': self.implied
        }

    def implied(self):
        self.cpu.push_ps_on_stack()


class PLA(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x68': self.implied
        }

    def implied(self):
        self.cpu.acc = int(self.cpu.pull_byte_from_stack(), base=0)
        self.cpu.ps['zero_flag'] = self.cpu.acc == 0
        self.cpu.ps['negative_flag'] = (self.cpu.acc >> 7) == 1


class PLP(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x28': self.implied
        }

    def implied(self):
        self.cpu.pull_ps_from_stack()
