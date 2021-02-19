import numpy as np

import cpu6502.instructions


class DEC(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xc6': self.zero_page,
            '0xd6': self.zero_page_x,
            '0xce': self.absolute,
            '0xde': self.absolute_x
        }

    def zero_page(self):
        pass

    def zero_page_x(self):
        pass

    def absolute(self):
        pass

    def absolute_x(self):
        pass


class DEX(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xca': self.implied
        }

    def implied(self):
        pass


class DEY(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x88': self.implied
        }

    def implied(self):
        pass
