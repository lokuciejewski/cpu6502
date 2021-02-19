import cpu6502.instructions


class BCC(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x90': self.relative
        }

    def relative(self):
        if not self.cpu.ps['carry_flag']:
            offset = int(self.cpu.fetch_byte(), base=0)
            target_address = self.cpu.pc + offset
            ~self.cpu.clock
            if (target_address >> 8) != (self.cpu.pc >> 8):
                ~self.cpu.clock
            self.cpu.pc = target_address
        else:
            self.cpu.pc = self.cpu.pc + 1
            ~self.cpu.clock


class BCS(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xb0': self.relative
        }

    def relative(self):
        if self.cpu.ps['carry_flag']:
            offset = int(self.cpu.fetch_byte(), base=0)
            target_address = self.cpu.pc + offset
            ~self.cpu.clock
            if (target_address >> 8) != (self.cpu.pc >> 8):
                ~self.cpu.clock
            self.cpu.pc = target_address
        else:
            self.cpu.pc = self.cpu.pc + 1
            ~self.cpu.clock


class BEQ(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xf0': self.relative
        }

    def relative(self):
        if self.cpu.ps['zero_flag']:
            offset = int(self.cpu.fetch_byte(), base=0)
            target_address = self.cpu.pc + offset
            ~self.cpu.clock
            if (target_address >> 8) != (self.cpu.pc >> 8):
                ~self.cpu.clock
            self.cpu.pc = target_address
        else:
            self.cpu.pc = self.cpu.pc + 1
            ~self.cpu.clock


class BMI(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x30': self.relative
        }

    def relative(self):
        if self.cpu.ps['negative_flag']:
            offset = int(self.cpu.fetch_byte(), base=0)
            target_address = self.cpu.pc + offset
            ~self.cpu.clock
            if (target_address >> 8) != (self.cpu.pc >> 8):
                ~self.cpu.clock
            self.cpu.pc = target_address
        else:
            self.cpu.pc = self.cpu.pc + 1
            ~self.cpu.clock


class BNE(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xd0': self.relative
        }

    def relative(self):
        if not self.cpu.ps['zero_flag']:
            offset = int(self.cpu.fetch_byte(), base=0)
            target_address = self.cpu.pc + offset
            ~self.cpu.clock
            if (target_address >> 8) != (self.cpu.pc >> 8):
                ~self.cpu.clock
            self.cpu.pc = target_address
        else:
            self.cpu.pc = self.cpu.pc + 1
            ~self.cpu.clock


class BPL(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x10': self.relative
        }

    def relative(self):
        if not self.cpu.ps['negative_flag']:
            offset = int(self.cpu.fetch_byte(), base=0)
            target_address = self.cpu.pc + offset
            ~self.cpu.clock
            if (target_address >> 8) != (self.cpu.pc >> 8):
                ~self.cpu.clock
            self.cpu.pc = target_address
        else:
            self.cpu.pc = self.cpu.pc + 1
            ~self.cpu.clock


class BVC(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x50': self.relative
        }

    def relative(self):
        if not self.cpu.ps['overflow_flag']:
            offset = int(self.cpu.fetch_byte(), base=0)
            target_address = self.cpu.pc + offset
            ~self.cpu.clock
            if (target_address >> 8) != (self.cpu.pc >> 8):
                ~self.cpu.clock
            self.cpu.pc = target_address
        else:
            self.cpu.pc = self.cpu.pc + 1
            ~self.cpu.clock


class BVS(cpu6502.instructions.AbstractInstruction):
    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x70': self.relative
        }

    def relative(self):
        if self.cpu.ps['overflow_flag']:
            offset = int(self.cpu.fetch_byte(), base=0)
            target_address = self.cpu.pc + offset
            ~self.cpu.clock
            if (target_address >> 8) != (self.cpu.pc >> 8):
                ~self.cpu.clock
            self.cpu.pc = target_address
        else:
            self.cpu.pc = self.cpu.pc + 1
            ~self.cpu.clock
