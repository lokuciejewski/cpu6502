import cpu6502.instructions


class TAX(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xaa': self.implied
        }

    def implied(self):
        self.cpu.idx = self.cpu.acc
        ~self.cpu.clock

    def finalise(self):
        self.cpu.ps['zero_flag'] = (self.cpu.idx == 0)
        self.cpu.ps['negative_flag'] = (self.cpu.idx & 0b10000000 != 0)  # Set negative flag if bit 7 of acc is set


class TAY(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xa8': self.implied
        }

    def implied(self):
        self.cpu.idy = self.cpu.acc
        ~self.cpu.clock

    def finalise(self):
        self.cpu.ps['zero_flag'] = (self.cpu.idy == 0)
        self.cpu.ps['negative_flag'] = (self.cpu.idy & 0b10000000 != 0)  # Set negative flag if bit 7 of acc is set


class TXA(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x8a': self.implied
        }

    def implied(self):
        self.cpu.acc = self.cpu.idx
        ~self.cpu.clock

    def finalise(self):
        self.cpu.ps['zero_flag'] = (self.cpu.acc == 0)
        self.cpu.ps['negative_flag'] = (self.cpu.acc & 0b10000000 != 0)  # Set negative flag if bit 7 of acc is set


class TYA(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x98': self.implied
        }

    def implied(self):
        self.cpu.acc = self.cpu.idy
        ~self.cpu.clock

    def finalise(self):
        self.cpu.ps['zero_flag'] = (self.cpu.acc == 0)
        self.cpu.ps['negative_flag'] = (self.cpu.acc & 0b10000000 != 0)  # Set negative flag if bit 7 of acc is set


class TSX(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xba': self.implied
        }

    def implied(self):
        self.cpu.idx = self.cpu.sp
        ~self.cpu.clock

    def finalise(self):
        self.cpu.ps['zero_flag'] = (self.cpu.idx == 0)
        self.cpu.ps['negative_flag'] = (self.cpu.idx & 0b10000000 != 0)  # Set negative flag if bit 7 of acc is set


class TXS(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x9a': self.implied
        }

    def implied(self):
        self.cpu.sp = self.cpu.idx
        ~self.cpu.clock
