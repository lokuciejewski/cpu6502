import cpu6502.instructions


class JMP(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x4c': self.absolute,
            '0x6c': self.indirect
        }

    def absolute(self):
        address = super(JMP, self).absolute()
        self.cpu.pc = address

    def indirect(self):
        address = int(self.cpu.fetch_word(), base=0)
        target_address = self.cpu.read_word(address)
        self.cpu.pc = int(target_address, base=0)


class JSR(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x20': self.absolute
        }

    def absolute(self):
        target_address = super(JSR, self).absolute()
        self.cpu.push_word_on_stack(self.cpu.pc - 1)
        self.cpu.pc = target_address


class RTS(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x60': self.implied
        }

    def implied(self):
        return_point = self.cpu.pull_word_from_stack()
        self.cpu.pc = int(return_point, base=0) + 1  # To compensate for 1 pc increment
        ~self.cpu.clock
