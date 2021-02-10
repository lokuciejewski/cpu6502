import sys
from time import sleep

from numpy import ushort, ubyte

from cpu6502.instructions import Instructions
from cpu6502.memory import Memory


class CPU(object):
    class Clock:
        """
        Internal class used for storing the remaining cycles of the operation
        """

        def __init__(self):
            self.cycles = True
            self.total_clock_cycles = 0

        def clock(self) -> None:
            """
            Method used to do one clock cycle, useful for debugging
            :return: None
            """
            self.cycles = not self.cycles
            self.total_clock_cycles += 1
            #sleep(0.001)

        def __invert__(self):
            """
            Operator overload for using ~clock instead of clock.clock()
            :return:
            """
            self.clock()

    def __init__(self):
        self.clock = CPU.Clock()
        self.pc = ushort()  # Program counter
        self.sp = ushort()  # Stack pointer
        self.acc = ubyte()  # Accumulator
        self.idx = ubyte()  # Index Register X
        self.idy = ubyte()  # Index Register Y
        # Processor status bits
        self.ps = {
            'carry_flag': bool(),
            'zero_flag': bool(),
            'interrupt_disable': bool(),
            'decimal_mode': bool(),
            'break_command': bool(),
            'overflow_flag': bool(),
            'negative_flag': bool()
        }
        self.memory = None
        self.io = None
        self.instructions = Instructions(self, filepath=r'C:\Users\grodo\Desktop\6502\6502_instructions.json')

    def __str__(self):
        return f'=============================\n' \
               f'||--- CPU 6502 emulator ---||\n' \
               f'=============================\n' \
               f' -> Clock state = {"H" if self.clock.cycles else "L"};' \
               f' Total clock cycles: {self.clock.total_clock_cycles}\n' \
               f' -> CPU registers:\n' \
               f'\t -> Program counter: {hex(self.pc)}\n' \
               f'\t -> Stack pointer: {hex(self.sp)}\n' \
               f'\t -> Top 10 stack values: {self.memory.get_stack(10)}\n' \
               f'\t -> Accumulator: {hex(self.acc)}; X index: {hex(self.idx)}; Y index: {hex(self.idy)}\n' \
               f' -> Processor status bits: {self.ps}\n' \
               f' -> 10 next bytes after program counter: {self.memory.get_values(self.pc, 10)}'

    def initialise_memory(self) -> None:
        self.memory = Memory()

    def reset(self) -> None:
        self.pc = 0xfffc
        ~self.clock
        self.sp = 0x01ff
        ~self.clock
        self.acc = 0
        self.idx = 0
        self.idy = 0
        self.ps['interrupt_disable'] = True
        # transfer .X to stack
        self.ps['decimal_mode'] = False
        # check for cartridge
        ~self.clock
        # if .Z == 0 then no cartridge detected
        # set bit 5 (MCM) off, bit 3 (38 cols) off
        # initialise I/O
        ~self.clock
        # initialise memory
        self.initialise_memory()
        ~self.clock
        # set I/O vectors (0x0314...0x0333) to kernel defaults
        # set system IRQ to correct value and start
        pc_address = self.fetch_word()
        self.pc = int(pc_address, base=0)
        self.ps['interrupt_disable'] = False
        print('=========== RESET ===========')

    def execute(self, number_of_instructions: int) -> None:
        for i in range(number_of_instructions):
            instruction = self.fetch_byte()
            try:
                self.instructions.execute(instruction)
            except KeyError:
                print(f'Instruction {instruction} not recognised. Skipping...')

    def fetch_byte(self) -> hex:
        try:
            data = self.memory[self.pc]
            self.pc += 1
            ~self.clock
            return hex(data)
        except IndexError:
            print(f'PC ({hex(self.pc)}) is out of memory bounds (0xffff)')

    def read_byte(self, address: hex) -> hex:
        try:
            data = self.memory[address]
            ~self.clock
            return hex(data)
        except IndexError:
            print(f'Address {address} is out of memory bounds (0xffff)')

    def write_byte(self, address: hex, value: ubyte):
        try:
            if 0x0100 <= address <= 0x01ff:  # Cannot write on stack
                raise IndexError
            self.memory[address] = value
            ~self.clock
        except IndexError:
            print(f'Address {address} is out of writable memory bounds (0x01ff - 0xffff)')

    def fetch_word(self) -> hex:
        # 6502 Cpu is little endian -> first byte is the least significant one
        try:
            data = self.memory[self.pc]
            self.pc += 1
            ~self.clock
            data |= (self.memory[self.pc] << 8)
            self.pc += 1
            ~self.clock
            if sys.byteorder == 'big':
                raise SystemError('This emulator only works on little endian systems')
            return hex(data)
        except IndexError:
            print(f'PC ({hex(self.pc)}) is out of memory bounds (0xffff)')

    def read_word(self, address) -> hex:
        # 6502 Cpu is little endian -> first byte is the least significant one
        try:
            data = self.memory[address]
            ~self.clock
            data |= (self.memory[address + 1] << 8)
            ~self.clock
            if sys.byteorder == 'big':
                raise SystemError('This emulator only works on little endian systems')
            return hex(data)
        except IndexError:
            print(f'Word {address, address + 1} is out of memory bounds (0xffff)')

    def write_word(self, address: hex, value: ushort):
        # 6502 Cpu is little endian -> first byte is the least significant one
        try:
            if 0x0100 <= address <= 0x01ff:  # Cannot write on stack
                raise IndexError
            self.memory[address] = value
            ~self.clock
            self.memory[address + 1] = (value >> 8)
            ~self.clock
            if sys.byteorder == 'big':
                raise SystemError('This emulator only works on little endian systems')
        except IndexError:
            print(f'Word {address, address + 1} is out of writable memory bounds (0x01ff - 0xffff)')

    def push_byte_on_stack(self, value: ubyte):
        try:
            if self.sp <= 0x0100:
                raise IndexError
            self.memory[self.sp] = value
            ~self.clock
            self.sp -= 1
            # One extra cycle for each push operation according to
            # https://wiki.nesdev.com/w/index.php/Cycle_counting
            ~self.clock
        except IndexError:
            print(f'Stack pointer ({self.sp}) is out of stack memory bounds (0x0100 - 0x01ff)')

    def push_word_on_stack(self, value: ushort):
        try:
            if self.sp <= 0x0101:  # Can't write a word here if there is not enough space on the stack
                raise IndexError
            self.memory[self.sp] = value
            ~self.clock
            self.sp -= 1
            self.memory[self.sp] = (value >> 8)
            ~self.clock
            self.sp -= 1
            # One extra cycle for each push operation according to
            # https://wiki.nesdev.com/w/index.php/Cycle_counting
            ~self.clock
            if sys.byteorder == 'big':
                raise SystemError('This emulator only works on little endian systems')
        except IndexError:
            print(f'Stack pointer ({self.sp}) is out of stack memory bounds (0x0100 - 0x01ff)')

    def pop_byte_from_stack(self) -> hex:
        try:
            if self.sp >= 0x01ff:
                raise IndexError
            data = self.memory[self.sp]
            ~self.clock
            self.sp += 1
            # Two extra cycles for each pop operation according to
            # https://wiki.nesdev.com/w/index.php/Cycle_counting
            ~self.clock
            ~self.clock
            return hex(data)
        except IndexError:
            print(f'Stack pointer ({self.sp}) is out of stack memory bounds (0x0100 - 0x01ff)')

    def pop_word_from_stack(self) -> hex:
        try:
            if self.sp >= 0x01fe:  # Can't pop a word from stack if there is only one byte on it
                raise IndexError
            ~self.clock
            self.sp += 1
            data = (self.memory[self.sp] << 8)
            ~self.clock
            self.sp += 1
            data |= self.memory[self.sp]
            # Two extra cycles for each pop operation according to
            # https://wiki.nesdev.com/w/index.php/Cycle_counting
            ~self.clock
            ~self.clock
            if sys.byteorder == 'big':
                raise SystemError('This emulator only works on little endian systems')
            return hex(data)
        except IndexError:
            print('There is not enough data on the stack to read a word')
