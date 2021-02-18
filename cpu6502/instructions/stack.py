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
        bin_ps = self.cpu.convert_ps_to_binary()
        self.cpu.push_byte_on_stack(bin_ps)


class PLA(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x68': self.implied
        }

    def implied(self):
        self.cpu.acc = int(self.cpu.pull_byte_from_stack(), base=0)


class PLP(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x28': self.implied
        }

    def implied(self):
        self.cpu.convert_binary_to_ps()
