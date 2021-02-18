import cpu6502.instructions


class STA(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x85': self.zero_page,
            '0x95': self.zero_page_x,
            '0x8d': self.absolute,
            '0x9d': self.absolute_x,
            '0x99': self.absolute_y,
            '0x81': self.indexed_indirect,
            '0x91': self.indirect_indexed
        }

    def zero_page(self):
        zp_address = super(STA, self).zero_page()
        self.cpu.write_byte(address=zp_address, value=self.cpu.acc)

    def zero_page_x(self):
        zp_address = super(STA, self).zero_page_x()
        self.cpu.write_byte(address=zp_address, value=self.cpu.acc)

    def absolute(self):
        address = super(STA, self).absolute()
        self.cpu.write_byte(address=address, value=self.cpu.acc)

    def absolute_x(self):
        address = super(STA, self).absolute_x()
        self.cpu.write_byte(address=address, value=self.cpu.acc)
        ~self.cpu.clock

    def absolute_y(self):
        address = super(STA, self).absolute_y()
        self.cpu.write_byte(address=address, value=self.cpu.acc)
        ~self.cpu.clock

    def indexed_indirect(self):
        address = super(STA, self).indexed_indirect()
        self.cpu.write_byte(address=address, value=self.cpu.acc)

    def indirect_indexed(self):
        starting_clock = self.cpu.clock.total_clock_cycles
        address = super(STA, self).indirect_indexed()
        self.cpu.write_byte(address=address, value=self.cpu.acc)
        self.cpu.clock.total_clock_cycles = starting_clock + 5  # Done to ensure static 6 clock cycles


class STX(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x86': self.zero_page,
            '0x96': self.zero_page_y,
            '0x8e': self.absolute
        }

    def zero_page(self):
        zp_address = super(STX, self).zero_page()
        self.cpu.write_byte(address=zp_address, value=self.cpu.idx)

    def zero_page_y(self):
        zp_address = super(STX, self).zero_page_y()
        self.cpu.write_byte(address=zp_address, value=self.cpu.idx)

    def absolute(self):
        address = super(STX, self).absolute()
        self.cpu.write_byte(address=address, value=self.cpu.idx)


class STY(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x84': self.zero_page,
            '0x94': self.zero_page_x,
            '0x8c': self.absolute
        }

    def zero_page(self):
        zp_address = super(STY, self).zero_page()
        self.cpu.write_byte(address=zp_address, value=self.cpu.idy)

    def zero_page_x(self):
        zp_address = super(STY, self).zero_page_x()
        self.cpu.write_byte(address=zp_address, value=self.cpu.idy)

    def absolute(self):
        address = super(STY, self).absolute()
        self.cpu.write_byte(address=address, value=self.cpu.idy)
