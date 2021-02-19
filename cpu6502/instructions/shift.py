import numpy as np

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
        self.cpu.ps['carry_flag'] = (self.cpu.acc >> 7)
        self.cpu.acc = np.ubyte(self.cpu.acc << 1)
        ~self.cpu.clock
        self.cpu.ps['zero_flag'] = self.cpu.acc == 0
        self.cpu.ps['negative_flag'] = (self.cpu.acc >> 7) == 1

    def zero_page(self):
        address = super(ASL, self).zero_page()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['carry_flag'] = (value >> 7)
        final_value = np.ubyte(value << 1)
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0
        self.cpu.ps['negative_flag'] = (final_value >> 7) == 1

    def zero_page_x(self):
        address = super(ASL, self).zero_page_x()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['carry_flag'] = (value >> 7)
        final_value = np.ubyte(value << 1)
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0
        self.cpu.ps['negative_flag'] = (final_value >> 7) == 1

    def absolute(self):
        address = super(ASL, self).absolute()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['carry_flag'] = (value >> 7)
        final_value = np.ubyte(value << 1)
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0
        self.cpu.ps['negative_flag'] = (final_value >> 7) == 1

    def absolute_x(self):
        address = super(ASL, self).absolute_x()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['carry_flag'] = (value >> 7)
        final_value = np.ubyte(value << 1)
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0
        self.cpu.ps['negative_flag'] = (final_value >> 7) == 1


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

    def finalise(self):
        self.cpu.ps['negative_flag'] = False

    def accumulator(self):
        self.cpu.ps['carry_flag'] = self.cpu.acc % 2
        self.cpu.acc = np.ubyte(self.cpu.acc >> 1)
        ~self.cpu.clock
        self.cpu.ps['zero_flag'] = self.cpu.acc == 0

    def zero_page(self):
        address = super(LSR, self).zero_page()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['carry_flag'] = value % 2
        final_value = np.ubyte(value >> 1)
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0

    def zero_page_x(self):
        address = super(LSR, self).zero_page_x()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['carry_flag'] = value % 2
        final_value = np.ubyte(value >> 1)
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0

    def absolute(self):
        address = super(LSR, self).absolute()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['carry_flag'] = value % 2
        final_value = np.ubyte(value >> 1)
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0

    def absolute_x(self):
        address = super(LSR, self).absolute_x()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['carry_flag'] = value % 2
        final_value = np.ubyte(value >> 1)
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0


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
        carry_flag_value = self.cpu.ps['carry_flag']
        self.cpu.ps['carry_flag'] = (self.cpu.acc >> 7)
        self.cpu.acc = np.ubyte((self.cpu.acc << 1) + carry_flag_value)
        ~self.cpu.clock
        self.cpu.ps['zero_flag'] = self.cpu.acc == 0
        self.cpu.ps['negative_flag'] = (self.cpu.acc >> 7) == 1

    def zero_page(self):
        address = super(ROL, self).zero_page()
        value = int(self.cpu.read_byte(address), base=0)
        carry_flag_value = self.cpu.ps['carry_flag']
        self.cpu.ps['carry_flag'] = (value >> 7)
        final_value = np.ubyte((value << 1) + carry_flag_value)
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0
        self.cpu.ps['negative_flag'] = (final_value >> 7) == 1

    def zero_page_x(self):
        address = super(ROL, self).zero_page_x()
        value = int(self.cpu.read_byte(address), base=0)
        carry_flag_value = self.cpu.ps['carry_flag']
        self.cpu.ps['carry_flag'] = (value >> 7)
        final_value = np.ubyte((value << 1) + carry_flag_value)
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0
        self.cpu.ps['negative_flag'] = (final_value >> 7) == 1

    def absolute(self):
        address = super(ROL, self).absolute()
        value = int(self.cpu.read_byte(address), base=0)
        carry_flag_value = self.cpu.ps['carry_flag']
        self.cpu.ps['carry_flag'] = (value >> 7)
        final_value = np.ubyte((value << 1) + carry_flag_value)
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0
        self.cpu.ps['negative_flag'] = (final_value >> 7) == 1

    def absolute_x(self):
        address = super(ROL, self).absolute_x()
        value = int(self.cpu.read_byte(address), base=0)
        carry_flag_value = self.cpu.ps['carry_flag']
        self.cpu.ps['carry_flag'] = (value >> 7)
        final_value = np.ubyte((value << 1) + carry_flag_value)
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0
        self.cpu.ps['negative_flag'] = (final_value >> 7) == 1


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
        carry_flag_value = self.cpu.ps['carry_flag']
        self.cpu.ps['carry_flag'] = self.cpu.acc % 2
        self.cpu.acc = np.ubyte((self.cpu.acc >> 1) + (carry_flag_value << 7))
        ~self.cpu.clock
        self.cpu.ps['zero_flag'] = self.cpu.acc == 0
        self.cpu.ps['negative_flag'] = (self.cpu.acc >> 7) == 1

    def zero_page(self):
        address = super(ROR, self).zero_page()
        value = int(self.cpu.read_byte(address), base=0)
        carry_flag_value = self.cpu.ps['carry_flag']
        self.cpu.ps['carry_flag'] = value % 2
        final_value = np.ubyte((value >> 1) + (carry_flag_value << 7))
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0
        self.cpu.ps['negative_flag'] = (final_value >> 7) == 1

    def zero_page_x(self):
        address = super(ROR, self).zero_page_x()
        value = int(self.cpu.read_byte(address), base=0)
        carry_flag_value = self.cpu.ps['carry_flag']
        self.cpu.ps['carry_flag'] = value % 2
        final_value = np.ubyte((value >> 1) + (carry_flag_value << 7))
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0
        self.cpu.ps['negative_flag'] = (final_value >> 7) == 1

    def absolute(self):
        address = super(ROR, self).absolute()
        value = int(self.cpu.read_byte(address), base=0)
        carry_flag_value = self.cpu.ps['carry_flag']
        self.cpu.ps['carry_flag'] = value % 2
        final_value = np.ubyte((value >> 1) + (carry_flag_value << 7))
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0
        self.cpu.ps['negative_flag'] = (final_value >> 7) == 1

    def absolute_x(self):
        address = super(ROR, self).absolute_x()
        value = int(self.cpu.read_byte(address), base=0)
        carry_flag_value = self.cpu.ps['carry_flag']
        self.cpu.ps['carry_flag'] = value % 2
        final_value = np.ubyte((value >> 1) + (carry_flag_value << 7))
        ~self.cpu.clock
        self.cpu.write_byte(address, final_value)
        self.cpu.ps['zero_flag'] = final_value == 0
        self.cpu.ps['negative_flag'] = (final_value >> 7) == 1
