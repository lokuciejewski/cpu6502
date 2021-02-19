import cpu6502.instructions


class BRK(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x00': self.implied
        }

    def implied(self):
        pass


class NOP(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xea': self.implied
        }

    def implied(self):
        self.cpu.pc += 1
        ~self.cpu.clock


class RTI(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x40': self.implied
        }

    def implied(self):
        pass
