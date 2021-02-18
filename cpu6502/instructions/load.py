import cpu6502.instructions


class LDA(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xa9': self.immediate,
            '0xa5': self.zero_page,
            '0xb5': self.zero_page_x,
            '0xad': self.absolute,
            '0xbd': self.absolute_x,
            '0xb9': self.absolute_y,
            '0xa1': self.indexed_indirect,
            '0xb1': self.indirect_indexed
        }

    def finalise(self):
        self.cpu.ps['zero_flag'] = (self.cpu.acc == 0)
        self.cpu.ps['negative_flag'] = (self.cpu.acc & 0b10000000 != 0)  # Set negative flag if bit 7 of acc is set

    def immediate(self):
        value = super(LDA, self).immediate()
        self.cpu.acc = value

    def zero_page(self):
        address = super(LDA, self).zero_page()
        self.cpu.acc = int(self.cpu.read_byte(address), base=0)

    def zero_page_x(self):
        address = super(LDA, self).zero_page_x()
        self.cpu.acc = int(self.cpu.read_byte(address), base=0)

    def absolute(self):
        address = super(LDA, self).absolute()
        self.cpu.acc = int(self.cpu.read_byte(address), base=0)

    def absolute_x(self):
        address = super(LDA, self).absolute_x()
        self.cpu.acc = int(self.cpu.read_byte(address), base=0)

    def absolute_y(self):
        address = super(LDA, self).absolute_y()
        self.cpu.acc = int(self.cpu.read_byte(address), base=0)

    def indexed_indirect(self):
        address = super(LDA, self).indexed_indirect()
        self.cpu.acc = int(self.cpu.read_byte(address), base=0)

    def indirect_indexed(self):
        address = super(LDA, self).indirect_indexed()
        self.cpu.acc = int(self.cpu.read_byte(address), base=0)


class LDX(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            "0xa2": self.immediate,
            "0xa6": self.zero_page,
            "0xb6": self.zero_page_y,
            "0xae": self.absolute,
            "0xbe": self.absolute_y
        }

    def finalise(self):
        self.cpu.ps['zero_flag'] = (self.cpu.idx == 0)
        self.cpu.ps['negative_flag'] = (self.cpu.idx & 0b10000000 != 0)  # Set negative flag if bit 7 of acc is set

    def immediate(self):
        value = super(LDX, self).immediate()
        self.cpu.idx = value

    def zero_page(self):
        address = super(LDX, self).zero_page()
        self.cpu.idx = int(self.cpu.read_byte(address), base=0)

    def zero_page_y(self):
        address = super(LDX, self).zero_page_y()
        self.cpu.idx = int(self.cpu.read_byte(address), base=0)

    def absolute(self):
        address = super(LDX, self).absolute()
        self.cpu.idx = int(self.cpu.read_byte(address), base=0)

    def absolute_y(self):
        address = super(LDX, self).absolute_y()
        self.cpu.idx = int(self.cpu.read_byte(address), base=0)


class LDY(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            "0xa0": self.immediate,
            "0xa4": self.zero_page,
            "0xb4": self.zero_page_x,
            "0xac": self.absolute,
            "0xbc": self.absolute_x
        }

    def finalise(self):
        self.cpu.ps['zero_flag'] = (self.cpu.idy == 0)
        self.cpu.ps['negative_flag'] = (self.cpu.idy & 0b10000000 != 0)  # Set negative flag if bit 7 of acc is set

    def immediate(self):
        value = super(LDY, self).immediate()
        self.cpu.idy = value

    def zero_page(self):
        address = super(LDY, self).zero_page()
        self.cpu.idy = int(self.cpu.read_byte(address), base=0)

    def zero_page_x(self):
        address = super(LDY, self).zero_page_x()
        self.cpu.idy = int(self.cpu.read_byte(address), base=0)

    def absolute(self):
        address = super(LDY, self).absolute()
        self.cpu.idy = int(self.cpu.read_byte(address), base=0)

    def absolute_x(self):
        address = super(LDY, self).absolute_x()
        self.cpu.idy = int(self.cpu.read_byte(address), base=0)
