import cpu6502.instructions


class NOP(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xea': self.implied
        }

    def implied(self):
        self.cpu.pc += 1
        ~self.cpu.clock


class RES(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xbb': self.implied
        }

    def implied(self):
        ~self.cpu.clock
        ~self.cpu.clock
        self.cpu.reset()
