import numpy as np

import cpu6502.instructions


class ADC(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x69': self.immediate,
            '0x65': self.zero_page,
            '0x75': self.zero_page_x,
            '0x6d': self.absolute,
            '0x7d': self.absolute_x,
            '0x79': self.absolute_y,
            '0x61': self.indexed_indirect,
            '0x71': self.indirect_indexed
        }

    def finalise(self):
        self.cpu.ps['zero_flag'] = self.cpu.acc == 0
        self.cpu.ps['negative_flag'] = bool(self.cpu.acc >> 7)

    def immediate(self):
        value = super(ADC, self).immediate()
        result = value + self.cpu.acc + self.cpu.ps['carry_flag']
        self.cpu.ps['carry_flag'] = result > 0xff
        self.cpu.ps['overflow_flag'] = ((value >> 7) == (self.cpu.acc >> 7)) != (np.ubyte(result) >> 7)
        self.cpu.acc = np.ubyte(result)

    def zero_page(self):
        address = super(ADC, self).zero_page()
        value = int(self.cpu.read_byte(address), base=0)
        result = value + self.cpu.acc + self.cpu.ps['carry_flag']
        self.cpu.ps['carry_flag'] = result > 0xff
        self.cpu.ps['overflow_flag'] = ((value >> 7) == (self.cpu.acc >> 7)) != (np.ubyte(result) >> 7)
        self.cpu.acc = np.ubyte(result)

    def zero_page_x(self):
        address = super(ADC, self).zero_page_x()
        value = int(self.cpu.read_byte(address), base=0)
        result = value + self.cpu.acc + self.cpu.ps['carry_flag']
        self.cpu.ps['carry_flag'] = result > 0xff
        self.cpu.ps['overflow_flag'] = ((value >> 7) == (self.cpu.acc >> 7)) != (np.ubyte(result) >> 7)
        self.cpu.acc = np.ubyte(result)

    def absolute(self):
        address = super(ADC, self).absolute()
        value = int(self.cpu.read_byte(address), base=0)
        result = value + self.cpu.acc + self.cpu.ps['carry_flag']
        self.cpu.ps['carry_flag'] = result > 0xff
        self.cpu.ps['overflow_flag'] = ((value >> 7) == (self.cpu.acc >> 7)) != (np.ubyte(result) >> 7)
        self.cpu.acc = np.ubyte(result)

    def absolute_x(self):
        address = super(ADC, self).absolute_x()
        value = int(self.cpu.read_byte(address), base=0)
        result = value + self.cpu.acc + self.cpu.ps['carry_flag']
        self.cpu.ps['carry_flag'] = result > 0xff
        self.cpu.ps['overflow_flag'] = ((value >> 7) == (self.cpu.acc >> 7)) != (np.ubyte(result) >> 7)
        self.cpu.acc = np.ubyte(result)

    def absolute_y(self):
        address = super(ADC, self).absolute_y()
        value = int(self.cpu.read_byte(address), base=0)
        result = value + self.cpu.acc + self.cpu.ps['carry_flag']
        self.cpu.ps['carry_flag'] = result > 0xff
        self.cpu.ps['overflow_flag'] = ((value >> 7) == (self.cpu.acc >> 7)) != (np.ubyte(result) >> 7)
        self.cpu.acc = np.ubyte(result)

    def indexed_indirect(self):
        address = super(ADC, self).indexed_indirect()
        value = int(self.cpu.read_byte(address), base=0)
        result = value + self.cpu.acc + self.cpu.ps['carry_flag']
        self.cpu.ps['carry_flag'] = result > 0xff
        self.cpu.ps['overflow_flag'] = ((value >> 7) == (self.cpu.acc >> 7)) != (np.ubyte(result) >> 7)
        self.cpu.acc = np.ubyte(result)

    def indirect_indexed(self):
        address = super(ADC, self).indirect_indexed()
        value = int(self.cpu.read_byte(address), base=0)
        result = value + self.cpu.acc + self.cpu.ps['carry_flag']
        self.cpu.ps['carry_flag'] = result > 0xff
        self.cpu.ps['overflow_flag'] = ((value >> 7) == (self.cpu.acc >> 7)) != (np.ubyte(result) >> 7)
        self.cpu.acc = np.ubyte(result)


class SBC(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xe9': self.immediate,
            '0xe5': self.zero_page,
            '0xf5': self.zero_page_x,
            '0xed': self.absolute,
            '0xfd': self.absolute_x,
            '0xf9': self.absolute_y,
            '0xe1': self.indexed_indirect,
            '0xf1': self.indirect_indexed
        }

    def finalise(self):
        self.cpu.ps['zero_flag'] = self.cpu.acc == 0
        self.cpu.ps['negative_flag'] = bool(self.cpu.acc >> 7)

    def immediate(self):
        value = super(SBC, self).immediate()
        result = self.cpu.acc - value - (1 - self.cpu.ps['carry_flag'])
        self.cpu.ps['carry_flag'] = result > 0xff
        self.cpu.ps['overflow_flag'] = ((value >> 7) == (self.cpu.acc >> 7)) != (np.ubyte(result) >> 7)
        self.cpu.acc = np.ubyte(result)

    def zero_page(self):
        address = super(SBC, self).zero_page()
        value = int(self.cpu.read_byte(address), base=0)
        result = self.cpu.acc - value - (1 - self.cpu.ps['carry_flag'])
        self.cpu.ps['carry_flag'] = result > 0xff
        self.cpu.ps['overflow_flag'] = ((value >> 7) == (self.cpu.acc >> 7)) != (np.ubyte(result) >> 7)
        self.cpu.acc = np.ubyte(result)

    def zero_page_x(self):
        address = super(SBC, self).zero_page_x()
        value = int(self.cpu.read_byte(address), base=0)
        result = self.cpu.acc - value - (1 - self.cpu.ps['carry_flag'])
        self.cpu.ps['carry_flag'] = result > 0xff
        self.cpu.ps['overflow_flag'] = ((value >> 7) == (self.cpu.acc >> 7)) != (np.ubyte(result) >> 7)
        self.cpu.acc = np.ubyte(result)

    def absolute(self):
        address = super(SBC, self).absolute()
        value = int(self.cpu.read_byte(address), base=0)
        result = self.cpu.acc - value - (1 - self.cpu.ps['carry_flag'])
        self.cpu.ps['carry_flag'] = result > 0xff
        self.cpu.ps['overflow_flag'] = ((value >> 7) == (self.cpu.acc >> 7)) != (np.ubyte(result) >> 7)
        self.cpu.acc = np.ubyte(result)

    def absolute_x(self):
        address = super(SBC, self).absolute_x()
        value = int(self.cpu.read_byte(address), base=0)
        result = self.cpu.acc - value - (1 - self.cpu.ps['carry_flag'])
        self.cpu.ps['carry_flag'] = result > 0xff
        self.cpu.ps['overflow_flag'] = ((value >> 7) == (self.cpu.acc >> 7)) != (np.ubyte(result) >> 7)
        self.cpu.acc = np.ubyte(result)

    def absolute_y(self):
        address = super(SBC, self).absolute_y()
        value = int(self.cpu.read_byte(address), base=0)
        result = self.cpu.acc - value - (1 - self.cpu.ps['carry_flag'])
        self.cpu.ps['carry_flag'] = result > 0xff
        self.cpu.ps['overflow_flag'] = ((value >> 7) == (self.cpu.acc >> 7)) != (np.ubyte(result) >> 7)
        self.cpu.acc = np.ubyte(result)

    def indexed_indirect(self):
        address = super(SBC, self).indexed_indirect()
        value = int(self.cpu.read_byte(address), base=0)
        result = self.cpu.acc - value - (1 - self.cpu.ps['carry_flag'])
        self.cpu.ps['carry_flag'] = result > 0xff
        self.cpu.ps['overflow_flag'] = ((value >> 7) == (self.cpu.acc >> 7)) != (np.ubyte(result) >> 7)
        self.cpu.acc = np.ubyte(result)

    def indirect_indexed(self):
        address = super(SBC, self).indirect_indexed()
        value = int(self.cpu.read_byte(address), base=0)
        result = self.cpu.acc - value - (1 - self.cpu.ps['carry_flag'])
        self.cpu.ps['carry_flag'] = result > 0xff
        self.cpu.ps['overflow_flag'] = ((value >> 7) == (self.cpu.acc >> 7)) != (np.ubyte(result) >> 7)
        self.cpu.acc = np.ubyte(result)


class CMP(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xc9': self.immediate,
            '0xc5': self.zero_page,
            '0xd5': self.zero_page_x,
            '0xcd': self.absolute,
            '0xdd': self.absolute_x,
            '0xd9': self.absolute_y,
            '0xc1': self.indexed_indirect,
            '0xd1': self.indirect_indexed
        }

    def immediate(self):
        value = super(CMP, self).immediate()
        self.cpu.ps['carry_flag'] = self.cpu.acc >= value
        self.cpu.ps['zero_flag'] = self.cpu.acc == value
        self.cpu.ps['negative_flag'] = ((self.cpu.acc - value) >> 7)

    def zero_page(self):
        address = super(CMP, self).zero_page()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['carry_flag'] = self.cpu.acc >= value
        self.cpu.ps['zero_flag'] = self.cpu.acc == value
        self.cpu.ps['negative_flag'] = ((self.cpu.acc - value) >> 7)

    def zero_page_x(self):
        address = super(CMP, self).zero_page_x()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['carry_flag'] = self.cpu.acc >= value
        self.cpu.ps['zero_flag'] = self.cpu.acc == value
        self.cpu.ps['negative_flag'] = ((self.cpu.acc - value) >> 7)

    def absolute(self):
        address = super(CMP, self).absolute()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['carry_flag'] = self.cpu.acc >= value
        self.cpu.ps['zero_flag'] = self.cpu.acc == value
        self.cpu.ps['negative_flag'] = ((self.cpu.acc - value) >> 7)

    def absolute_x(self):
        address = super(CMP, self).absolute_x()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['carry_flag'] = self.cpu.acc >= value
        self.cpu.ps['zero_flag'] = self.cpu.acc == value
        self.cpu.ps['negative_flag'] = ((self.cpu.acc - value) >> 7)

    def absolute_y(self):
        address = super(CMP, self).absolute_y()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['carry_flag'] = self.cpu.acc >= value
        self.cpu.ps['zero_flag'] = self.cpu.acc == value
        self.cpu.ps['negative_flag'] = ((self.cpu.acc - value) >> 7)

    def indexed_indirect(self):
        address = super(CMP, self).indexed_indirect()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['carry_flag'] = self.cpu.acc >= value
        self.cpu.ps['zero_flag'] = self.cpu.acc == value
        self.cpu.ps['negative_flag'] = ((self.cpu.acc - value) >> 7)

    def indirect_indexed(self):
        address = super(CMP, self).indirect_indexed()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['carry_flag'] = self.cpu.acc >= value
        self.cpu.ps['zero_flag'] = self.cpu.acc == value
        self.cpu.ps['negative_flag'] = ((self.cpu.acc - value) >> 7)


class CPX(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xe0': self.immediate,
            '0xe4': self.zero_page,
            '0xec': self.absolute
        }

    def immediate(self):
        value = super(CPX, self).immediate()
        self.cpu.ps['carry_flag'] = self.cpu.idx >= value
        self.cpu.ps['zero_flag'] = self.cpu.idx == value
        self.cpu.ps['negative_flag'] = ((self.cpu.idx - value) >> 7)

    def zero_page(self):
        address = super(CPX, self).zero_page()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['carry_flag'] = self.cpu.idx >= value
        self.cpu.ps['zero_flag'] = self.cpu.idx == value
        self.cpu.ps['negative_flag'] = ((self.cpu.idx - value) >> 7)

    def absolute(self):
        address = super(CPX, self).absolute()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['carry_flag'] = self.cpu.idx >= value
        self.cpu.ps['zero_flag'] = self.cpu.idx == value
        self.cpu.ps['negative_flag'] = ((self.cpu.idx - value) >> 7)


class CPY(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xc0': self.immediate,
            '0xc4': self.zero_page,
            '0xcc': self.absolute
        }

    def immediate(self):
        value = super(CPY, self).immediate()
        self.cpu.ps['carry_flag'] = self.cpu.idy >= value
        self.cpu.ps['zero_flag'] = self.cpu.idy == value
        self.cpu.ps['negative_flag'] = ((self.cpu.idy - value) >> 7)

    def zero_page(self):
        address = super(CPY, self).zero_page()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['carry_flag'] = self.cpu.idy >= value
        self.cpu.ps['zero_flag'] = self.cpu.idy == value
        self.cpu.ps['negative_flag'] = ((self.cpu.idy - value) >> 7)

    def absolute(self):
        address = super(CPY, self).absolute()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['carry_flag'] = self.cpu.idy >= value
        self.cpu.ps['zero_flag'] = self.cpu.idy == value
        self.cpu.ps['negative_flag'] = ((self.cpu.idy - value) >> 7)
