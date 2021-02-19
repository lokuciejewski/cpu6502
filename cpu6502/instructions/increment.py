import numpy as np

import cpu6502.instructions


class INC(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xe6': self.zero_page,
            '0xf6': self.zero_page_x,
            '0xee': self.absolute,
            '0xfe': self.absolute_x
        }

    def zero_page(self):
        pass

    def zero_page_x(self):
        pass

    def absolute(self):
        pass

    def absolute_x(self):
        pass


class INX(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xe8': self.implied
        }

    def implied(self):
        pass


class INY(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xc8': self.implied
        }

    def implied(self):
        pass
