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
        address = super(INC, self).zero_page()
        value = int(self.cpu.read_byte(address), base=0)
        final_value = np.ubyte(value + 1)
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0
        self.cpu.ps['negative_flag'] = (final_value >> 7) == 1

    def zero_page_x(self):
        address = super(INC, self).zero_page_x()
        value = int(self.cpu.read_byte(address), base=0)
        final_value = np.ubyte(value + 1)
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0
        self.cpu.ps['negative_flag'] = (final_value >> 7) == 1

    def absolute(self):
        address = super(INC, self).absolute()
        value = int(self.cpu.read_byte(address), base=0)
        final_value = np.ubyte(value + 1)
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0
        self.cpu.ps['negative_flag'] = (final_value >> 7) == 1

    def absolute_x(self):
        address = super(INC, self).absolute_x()
        value = int(self.cpu.read_byte(address), base=0)
        final_value = np.ubyte(value + 1)
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0
        self.cpu.ps['negative_flag'] = (final_value >> 7) == 1
        ~self.cpu.clock


class INX(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xe8': self.implied
        }

    def implied(self):
        final_value = np.ubyte(self.cpu.idx + 1)
        ~self.cpu.clock
        self.cpu.idx = final_value
        self.cpu.ps['zero_flag'] = final_value == 0
        self.cpu.ps['negative_flag'] = (final_value >> 7) == 1


class INY(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xc8': self.implied
        }

    def implied(self):
        final_value = np.ubyte(self.cpu.idy + 1)
        ~self.cpu.clock
        self.cpu.idy = final_value
        self.cpu.ps['zero_flag'] = final_value == 0
        self.cpu.ps['negative_flag'] = (final_value >> 7) == 1
