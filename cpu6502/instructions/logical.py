import cpu6502.instructions


class AND(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x29': self.immediate,
            '0x25': self.zero_page,
            '0x35': self.zero_page_x,
            '0x2d': self.absolute,
            '0x3d': self.absolute_x,
            '0x39': self.absolute_y,
            '0x21': self.indexed_indirect,
            '0x31': self.indirect_indexed
        }

    def finalise(self):
        self.cpu.ps['zero_flag'] = (self.cpu.acc == 0)
        self.cpu.ps['negative_flag'] = (self.cpu.acc & 0b10000000 != 0)  # Set negative flag if bit 7 of acc is set

    def immediate(self):
        value = super(AND, self).immediate()
        self.cpu.acc &= value

    def zero_page(self):
        zp_address = super(AND, self).zero_page()
        self.cpu.acc &= int(self.cpu.read_byte(zp_address), base=0)

    def zero_page_x(self):
        zp_address = super(AND, self).zero_page_x()
        self.cpu.acc &= int(self.cpu.read_byte(zp_address), base=0)

    def absolute(self):
        address = super(AND, self).absolute()
        self.cpu.acc &= int(self.cpu.read_byte(address), base=0)

    def absolute_x(self):
        address = super(AND, self).absolute_x()
        self.cpu.acc &= int(self.cpu.read_byte(address), base=0)

    def absolute_y(self):
        address = super(AND, self).absolute_y()
        self.cpu.acc &= int(self.cpu.read_byte(address), base=0)

    def indexed_indirect(self):
        address = super(AND, self).indexed_indirect()
        self.cpu.acc &= int(self.cpu.read_byte(address), base=0)

    def indirect_indexed(self):
        address = super(AND, self).indirect_indexed()
        self.cpu.acc &= int(self.cpu.read_byte(address), base=0)


class EOR(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x49': self.immediate,
            '0x45': self.zero_page,
            '0x55': self.zero_page_x,
            '0x4d': self.absolute,
            '0x5d': self.absolute_x,
            '0x59': self.absolute_y,
            '0x41': self.indexed_indirect,
            '0x51': self.indirect_indexed
        }

    def finalise(self):
        self.cpu.ps['zero_flag'] = (self.cpu.acc == 0)
        self.cpu.ps['negative_flag'] = (self.cpu.acc & 0b10000000 != 0)  # Set negative flag if bit 7 of acc is set

    def immediate(self):
        value = super(EOR, self).immediate()
        self.cpu.acc ^= value

    def zero_page(self):
        zp_address = super(EOR, self).zero_page()
        self.cpu.acc ^= int(self.cpu.read_byte(zp_address), base=0)

    def zero_page_x(self):
        zp_address = super(EOR, self).zero_page_x()
        self.cpu.acc ^= int(self.cpu.read_byte(zp_address), base=0)

    def absolute(self):
        address = super(EOR, self).absolute()
        self.cpu.acc ^= int(self.cpu.read_byte(address), base=0)

    def absolute_x(self):
        address = super(EOR, self).absolute_x()
        self.cpu.acc ^= int(self.cpu.read_byte(address), base=0)

    def absolute_y(self):
        address = super(EOR, self).absolute_y()
        self.cpu.acc ^= int(self.cpu.read_byte(address), base=0)

    def indexed_indirect(self):
        address = super(EOR, self).indexed_indirect()
        self.cpu.acc ^= int(self.cpu.read_byte(address), base=0)

    def indirect_indexed(self):
        address = super(EOR, self).indirect_indexed()
        self.cpu.acc ^= int(self.cpu.read_byte(address), base=0)


class ORA(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x09': self.immediate,
            '0x05': self.zero_page,
            '0x15': self.zero_page_x,
            '0x0d': self.absolute,
            '0x1d': self.absolute_x,
            '0x19': self.absolute_y,
            '0x01': self.indexed_indirect,
            '0x11': self.indirect_indexed
        }

    def finalise(self):
        self.cpu.ps['zero_flag'] = (self.cpu.acc == 0)
        self.cpu.ps['negative_flag'] = (self.cpu.acc & 0b10000000 != 0)  # Set negative flag if bit 7 of acc is set

    def immediate(self):
        value = super(ORA, self).immediate()
        self.cpu.acc |= value

    def zero_page(self):
        zp_address = super(ORA, self).zero_page()
        self.cpu.acc |= int(self.cpu.read_byte(zp_address), base=0)

    def zero_page_x(self):
        zp_address = super(ORA, self).zero_page_x()
        self.cpu.acc |= int(self.cpu.read_byte(zp_address), base=0)

    def absolute(self):
        address = super(ORA, self).absolute()
        self.cpu.acc |= int(self.cpu.read_byte(address), base=0)

    def absolute_x(self):
        address = super(ORA, self).absolute_x()
        self.cpu.acc |= int(self.cpu.read_byte(address), base=0)

    def absolute_y(self):
        address = super(ORA, self).absolute_y()
        self.cpu.acc |= int(self.cpu.read_byte(address), base=0)

    def indexed_indirect(self):
        address = super(ORA, self).indexed_indirect()
        self.cpu.acc |= int(self.cpu.read_byte(address), base=0)

    def indirect_indexed(self):
        address = super(ORA, self).indirect_indexed()
        self.cpu.acc |= int(self.cpu.read_byte(address), base=0)


class BIT(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x24': self.zero_page,
            '0x2c': self.absolute
        }

    def zero_page(self):
        zp_address = super(BIT, self).zero_page()
        value = int(self.cpu.read_byte(zp_address), base=0)
        self.cpu.ps['zero_flag'] = ((value & self.cpu.acc) == 0)
        self.cpu.ps['overflow_flag'] = (value & 0b01000000)
        self.cpu.ps['negative_flag'] = (value & 0b10000000 != 0)

    def absolute(self):
        address = super(BIT, self).absolute()
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['zero_flag'] = ((value & self.cpu.acc) == 0)
        self.cpu.ps['overflow_flag'] = (value & 0b01000000)
        self.cpu.ps['negative_flag'] = (value & 0b10000000 != 0)
