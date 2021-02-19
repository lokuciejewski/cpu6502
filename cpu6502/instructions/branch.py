import cpu6502.instructions


class BCC(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x90': self.relative
        }

    def relative(self):
        pass


class BCS(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xb0': self.relative
        }

    def relative(self):
        pass


class BEQ(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xf0': self.relative
        }

    def relative(self):
        pass


class BMI(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x30': self.relative
        }

    def relative(self):
        pass


class BNE(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xd0': self.relative
        }

    def relative(self):
        pass


class BPL(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x10': self.relative
        }

    def relative(self):
        pass


class BVC(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x50': self.relative
        }

    def relative(self):
        pass


class BVS(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x70': self.relative
        }

    def relative(self):
        pass
