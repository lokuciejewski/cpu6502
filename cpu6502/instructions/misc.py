import cpu6502.instructions


class BRK(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x00': self.implied
        }

    def implied(self):
        self.cpu.push_word_on_stack(self.cpu.pc)
        self.cpu.push_ps_on_stack()
        self.cpu.pc = int(self.cpu.read_word(0xfffe), base=0)
        self.cpu.ps['break_flag'] = True
        self.cpu.clock.total_clock_cycles -= 1  # Weird but needed to be done


class NOP(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xea': self.implied
        }

    def implied(self):
        self.cpu.pc += 1
        ~self.cpu.clock


class RTI(cpu6502.instructions.AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x40': self.implied
        }

    def implied(self):
        self.cpu.pull_ps_from_stack()
        self.cpu.pc = int(self.cpu.pull_word_from_stack(), base=0)
        self.cpu.clock.total_clock_cycles -= 2  # Weird but needed to be done
