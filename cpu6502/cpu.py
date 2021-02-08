import json
import sys
from abc import abstractmethod

from numpy import ushort, ubyte

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

    def reset(self) -> None:
        self.pc = 0xfffc
        self.sp = 0x0100
        self.acc = 0
        self.idx = 0
        self.idy = 0
        self.ps['interrupt_disable'] = True
        # transfer .X to stack
        self.ps['decimal_mode'] = False
        # check for cartridge
        # if .Z == 0 then no cartridge detected
        # set bit 5 (MCM) off, bit 3 (38 cols) off
        # initialise I/O
        # initialise memory
        self.memory = Memory()
        # set I/O vectors (0x0314...0x0333) to kernel defaults
        # set system IRQ to correct value and start
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
            if self.sp >= 0x01ff:
                raise IndexError
            self.memory[self.sp] = value
            ~self.clock
            self.sp += 1
            # One extra cycle for each push operation according to
            # https://wiki.nesdev.com/w/index.php/Cycle_counting
            ~self.clock
        except IndexError:
            print(f'Stack pointer ({self.sp}) is out of stack memory bounds (0x0100 - 0x01ff)')

    def push_word_on_stack(self, value: ushort):
        try:
            if self.sp >= 0x01fe:  # Can't write a word here if there is not enough space on the stack
                raise IndexError
            self.memory[self.sp] = value
            ~self.clock
            self.sp += 1
            self.memory[self.sp] = (value >> 8)
            ~self.clock
            self.sp += 1
            # One extra cycle for each push operation according to
            # https://wiki.nesdev.com/w/index.php/Cycle_counting
            ~self.clock
            if sys.byteorder == 'big':
                raise SystemError('This emulator only works on little endian systems')
        except IndexError:
            print(f'Stack pointer ({self.sp}) is out of stack memory bounds (0x0100 - 0x01ff)')

    def pop_byte_from_stack(self) -> hex:
        try:
            if self.sp <= 0x0100:
                raise IndexError
            data = self.memory[self.sp]
            ~self.clock
            self.sp -= 1
            # Two extra cycles for each pop operation according to
            # https://wiki.nesdev.com/w/index.php/Cycle_counting
            ~self.clock
            ~self.clock
            return hex(data)
        except IndexError:
            print(f'Stack pointer ({self.sp}) is out of stack memory bounds (0x0100 - 0x01ff)')

    def pop_word_from_stack(self) -> hex:
        try:
            if self.sp <= 0x0101:  # Can't pop a word from stack if there is only one byte on it
                raise IndexError
            ~self.clock
            self.sp -= 1
            data = (self.memory[self.sp] << 8)
            ~self.clock
            self.sp -= 1
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


class Instructions:

    def __init__(self, cpu: CPU, filepath: str):
        self.opcodes = {}
        self.internal_assignment = {
            'RES': RES,
            'LDA': LDA,
            'JSR': JSR,
            'RTS': RTS,
            'JMP': JMP
        }
        self.__parse_instruction_json(filepath)
        self.cpu = cpu

    def __parse_instruction_json(self, filepath: str):
        """
        Instructions json file downloaded from https://gist.github.com/kirbyUK/1a0797e19f54c1e35e67ce7b385b323e
        :param filepath: str: Path to the json file containing instruction set
        :return: None
        """
        with open(filepath) as file:
            contents = json.load(file)
            for instruction in contents:
                try:
                    opcode = f'0x{instruction["opcode"].strip("$").lower()}'
                    self.opcodes[opcode] = self.internal_assignment[instruction['name']]
                except KeyError:
                    pass
                    # print(f'Instruction not supported: {instruction["name"]}')

    def execute(self, opcode: str):
        instruction = self.opcodes[opcode](self.cpu)
        instruction.execute(opcode)
        instruction.finalise()


class AbstractInstruction:
    """
    Abstract class which all instructions should inherit from
    """

    @abstractmethod
    def __init__(self, cpu: CPU):
        """
        Method to specify events that happen for every type of addressing before the instruction is executed
        :param cpu: CPU: Cpu object which the instructions will be executed on
        """
        self.opcodes = {}
        self.cpu = cpu
        pass

    def execute(self, opcode: str):
        """
        Method that executes the method chosen by opcode
        :param opcode: str: Opcode of the specific instruction (instruction + addressing)
        :return: None
        """
        self.opcodes[opcode]()

    def finalise(self):
        """
        Method to specify events that happen for every type of addressing after the instruction is executed
        :return: None
        """
        pass


class RES(AbstractInstruction):

    def __init__(self, cpu: CPU):
        super().__init__(cpu)
        self.opcodes = {
            '0xbb': self.implied
        }

    def implied(self):
        ~self.cpu.clock
        ~self.cpu.clock
        self.cpu.reset()


class LDA(AbstractInstruction):

    def __init__(self, cpu: CPU):
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
        self.cpu.ps['negative_flag'] = self.cpu.acc > 0b01111111  # Set negative flag if bit 7 of acc is set

    def immediate(self):
        self.cpu.acc = int(self.cpu.fetch_byte(), base=0)

    def zero_page(self):
        address = int(self.cpu.fetch_byte(), base=0)
        self.cpu.acc = int(self.cpu.read_byte(address), base=0)

    def zero_page_x(self):
        address = int(self.cpu.fetch_byte(), base=0)
        self.cpu.acc = int(self.cpu.read_byte(address + int(self.cpu.idx)), base=0)
        ~self.cpu.clock  # One additional clock needed

    def absolute(self):
        address = int(self.cpu.read_word(self.cpu.pc), base=0)
        self.cpu.acc = int(self.cpu.read_byte(address), base=0)

    def absolute_x(self):
        address = int(self.cpu.read_word(self.cpu.pc), base=0)
        if (address >> 8) != ((address + self.cpu.idx) >> 8):
            ~self.cpu.clock
        self.cpu.acc = int(self.cpu.read_byte(address + self.cpu.idx), base=0)

    def absolute_y(self):
        address = int(self.cpu.read_word(self.cpu.pc), base=0)
        if (address >> 8) != ((address + self.cpu.idy) >> 8):
            ~self.cpu.clock
        self.cpu.acc = int(self.cpu.read_byte(address + self.cpu.idy), base=0)

    def indexed_indirect(self):
        zp_address = int(self.cpu.read_byte(self.cpu.pc), base=0) + self.cpu.idx
        ~self.cpu.clock
        address = int(self.cpu.read_word(zp_address), base=0)
        self.cpu.acc = int(self.cpu.read_byte(address), base=0)

    def indirect_indexed(self):
        zp_address = int(self.cpu.read_byte(self.cpu.pc), base=0)
        address = int(self.cpu.read_word(zp_address), base=0) + self.cpu.idy
        self.cpu.acc = int(self.cpu.read_byte(address), base=0)


class JSR(AbstractInstruction):

    def __init__(self, cpu: CPU):
        super().__init__(cpu)
        self.opcodes = {
            '0x20': self.absolute
        }

    def absolute(self):
        self.cpu.push_word_on_stack(self.cpu.pc)
        self.cpu.pc = int(self.cpu.read_word(self.cpu.pc), base=0)


class RTS(AbstractInstruction):

    def __init__(self, cpu: CPU):
        super().__init__(cpu)
        self.opcodes = {
            '0x60': self.implied
        }

    def implied(self):
        return_point = self.cpu.pop_word_from_stack()
        self.cpu.pc = int(return_point, base=0) + 2  # To skip the 2 bytes after JSR
        ~self.cpu.clock


class JMP(AbstractInstruction):

    def __init__(self, cpu: CPU):
        super().__init__(cpu)
        self.opcodes = {
            '0x4c': self.absolute,
            '0x6c': self.indirect
        }

    def absolute(self):
        target_address = self.cpu.read_word(self.cpu.pc)
        self.cpu.pc = int(target_address, base=0)

    def indirect(self):
        address = int(self.cpu.read_word(self.cpu.pc), base=0)
        target_address = self.cpu.read_word(address)
        self.cpu.pc = int(target_address, base=0)
