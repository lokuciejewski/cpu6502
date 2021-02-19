import cpu6502.instructions


class ASL(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x0a': self.accumulator,
            '0x06': self.zero_page,
            '0x16': self.zero_page_x,
            '0x0e': self.absolute,
            '0x1e': self.absolute_x
        }

    def accumulator(self):
        pass

    def zero_page(self):
        pass

    def zero_page_x(self):
        pass

    def absolute(self):
        pass

    def absolute_x(self):
        pass


class LSR(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x4a': self.accumulator,
            '0x46': self.zero_page,
            '0x56': self.zero_page_x,
            '0x4e': self.absolute,
            '0x5e': self.absolute_x
        }

    def accumulator(self):
        pass

    def zero_page(self):
        pass

    def zero_page_x(self):
        pass

    def absolute(self):
        pass

    def absolute_x(self):
        pass


class ROL(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x2a': self.accumulator,
            '0x26': self.zero_page,
            '0x36': self.zero_page_x,
            '0x2e': self.absolute,
            '0x3e': self.absolute_x
        }

    def accumulator(self):
        pass

    def zero_page(self):
        pass

    def zero_page_x(self):
        pass

    def absolute(self):
        pass

    def absolute_x(self):
        pass


class ROR(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x6a': self.accumulator,
            '0x66': self.zero_page,
            '0x76': self.zero_page_x,
            '0x6e': self.absolute,
            '0x7e': self.absolute_x
        }

    def accumulator(self):
        pass

    def zero_page(self):
        pass

    def zero_page_x(self):
        pass

    def absolute(self):
        pass

    def absolute_x(self):
        pass
