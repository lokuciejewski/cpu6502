import json
from abc import abstractmethod

import numpy as np


class Instructions:

    def __init__(self, cpu, filepath: str):
        self.opcodes = {}
        self.internal_assignment = {
            # Instruction order taken from http://www.obelisk.me.uk/6502/instructions.html
            # LOAD AND STORE
            'LDA': LDA,
            'LDX': LDX,
            'LDY': LDY,
            'STA': STA,
            'STX': STX,
            'STY': STY,
            # TRANSFER
            'TAX': TAX,
            'TAY': TAY,
            'TXA': TXA,
            'TYA': TYA,
            'TSX': TSX,
            'TXS': TXS,
            # STACK OPERATIONS
            'PHA': PHA,
            'PHP': PHP,
            'PLA': PLA,
            'PLP': PLP,
            # LOGICAL OPERATIONS
            'AND': AND,
            'EOR': EOR,
            'ORA': ORA,
            'BIT': BIT,
            # ARITHMETIC OPERATIONS
            'ADC': CMP,
            'SBC': SBC,
            'CMP': CMP,
            'CPX': CPX,
            'CPY': CPY,
            # JUMP AND CALLS
            'JMP': JMP,
            'JSR': JSR,
            'RTS': RTS,
            # MISC
            'NOP': NOP,
            'RES': RES,
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
            not_supported = set()
            for instruction in contents:
                try:
                    opcode = f'0x{instruction["opcode"].strip("$").lower()}'
                    self.opcodes[opcode] = self.internal_assignment[instruction['name']]
                except KeyError:
                    not_supported.add(instruction['name'])
        print(f'Unsupported instructions ({len(not_supported)}): {not_supported}')

    def execute(self, opcode: str):
        instruction = self.opcodes[opcode](self.cpu)
        instruction.execute(opcode)
        instruction.finalise()


class AbstractInstruction:
    """
    Abstract class which all instructions should inherit from
    """

    @abstractmethod
    def __init__(self, cpu):
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

    # All addressing modes pushed here for easier and faster testing

    def immediate(self):
        return int(self.cpu.fetch_byte(), base=0)

    def zero_page(self):
        return int(self.cpu.fetch_byte(), base=0)

    def zero_page_x(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        return np.ubyte(zp_address + self.cpu.idx)

    def zero_page_y(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        return np.ubyte(zp_address + self.cpu.idy)

    def absolute(self):
        return int(self.cpu.fetch_word(), base=0)

    def absolute_x(self):
        address = int(self.cpu.fetch_word(), base=0)
        if (address >> 8) != ((address + self.cpu.idx) >> 8):
            ~self.cpu.clock
        return int(self.cpu.read_byte(address + self.cpu.idx), base=0)

    def absolute_y(self):
        address = int(self.cpu.fetch_word(), base=0)
        if (address >> 8) != ((address + self.cpu.idy) >> 8):
            ~self.cpu.clock
        return int(self.cpu.read_byte(address + self.cpu.idy), base=0)

    def indexed_indirect(self):
        zp_address = np.ubyte(int(self.cpu.fetch_byte(), base=0) + self.cpu.idx)
        ~self.cpu.clock
        address = int(self.cpu.read_word(zp_address), base=0)
        return int(self.cpu.read_byte(address), base=0)

    def indirect_indexed(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        address = int(self.cpu.read_word(zp_address), base=0) + self.cpu.idy
        if (address >> 8) != ((address + self.cpu.idy) >> 8):
            ~self.cpu.clock
        return int(self.cpu.read_byte(address), base=0)

    def implied(self):
        # Too many different methods to generalise
        pass


"""LOAD/STORE INSTRUCTIONS"""


class LDA(AbstractInstruction):

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
        value = super(LDA, self).zero_page_x()
        self.cpu.acc = value
        ~self.cpu.clock  # One additional clock needed

    def absolute(self):
        address = super(LDA, self).absolute()
        self.cpu.acc = int(self.cpu.read_byte(address), base=0)

    def absolute_x(self):
        value = super(LDA, self).absolute_x()
        self.cpu.acc = value

    def absolute_y(self):
        value = super(LDA, self).absolute_y()
        self.cpu.acc = value

    def indexed_indirect(self):
        value = super(LDA, self).indexed_indirect()
        self.cpu.acc = value

    def indirect_indexed(self):
        value = super(LDA, self).indirect_indexed()
        self.cpu.acc = value


class LDX(AbstractInstruction):

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
        self.cpu.idx = int(self.cpu.fetch_byte(), base=0)

    def zero_page(self):
        address = int(self.cpu.fetch_byte(), base=0)
        self.cpu.idx = int(self.cpu.read_byte(address), base=0)

    def zero_page_y(self):
        address = int(self.cpu.fetch_byte(), base=0)
        self.cpu.idx = int(self.cpu.read_byte(address + int(self.cpu.idy)), base=0)
        ~self.cpu.clock  # One additional clock needed

    def absolute(self):
        address = int(self.cpu.fetch_word(), base=0)
        self.cpu.idx = int(self.cpu.read_byte(address), base=0)

    def absolute_y(self):
        address = int(self.cpu.fetch_word(), base=0)
        if (address >> 8) != ((address + self.cpu.idy) >> 8):
            ~self.cpu.clock
        self.cpu.idx = int(self.cpu.read_byte(address + self.cpu.idy), base=0)


class LDY(AbstractInstruction):

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
        self.cpu.idy = int(self.cpu.fetch_byte(), base=0)

    def zero_page(self):
        address = int(self.cpu.fetch_byte(), base=0)
        self.cpu.idy = int(self.cpu.read_byte(address), base=0)

    def zero_page_x(self):
        address = int(self.cpu.fetch_byte(), base=0)
        self.cpu.idy = int(self.cpu.read_byte(address + int(self.cpu.idx)), base=0)
        ~self.cpu.clock  # One additional clock needed

    def absolute(self):
        address = int(self.cpu.fetch_word(), base=0)
        self.cpu.idy = int(self.cpu.read_byte(address), base=0)

    def absolute_x(self):
        address = int(self.cpu.fetch_word(), base=0)
        if (address >> 8) != ((address + self.cpu.idx) >> 8):
            ~self.cpu.clock
        self.cpu.idy = int(self.cpu.read_byte(address + self.cpu.idx), base=0)


class STA(AbstractInstruction):

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
        zp_address = int(self.cpu.fetch_byte(), base=0)
        self.cpu.write_byte(address=zp_address, value=self.cpu.acc)

    def zero_page_x(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        self.cpu.write_byte(address=zp_address + self.cpu.idx, value=self.cpu.acc)
        ~self.cpu.clock

    def absolute(self):
        target_address = int(self.cpu.fetch_word(), base=0)
        self.cpu.write_byte(address=target_address, value=self.cpu.acc)

    def absolute_x(self):
        target_address = int(self.cpu.fetch_word(), base=0)
        self.cpu.write_byte(address=target_address + self.cpu.idx, value=self.cpu.acc)
        ~self.cpu.clock

    def absolute_y(self):
        target_address = int(self.cpu.fetch_word(), base=0)
        self.cpu.write_byte(address=target_address + self.cpu.idy, value=self.cpu.acc)
        ~self.cpu.clock

    def indexed_indirect(self):
        zp_address = np.ubyte(int(self.cpu.fetch_byte(), base=0) + self.cpu.idx)
        ~self.cpu.clock
        address = int(self.cpu.read_word(zp_address), base=0)
        self.cpu.write_byte(address=address, value=self.cpu.acc)

    def indirect_indexed(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        address = int(self.cpu.read_word(zp_address), base=0) + self.cpu.idy
        ~self.cpu.clock
        self.cpu.write_byte(address=address, value=self.cpu.acc)


class STX(AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x86': self.zero_page,
            '0x96': self.zero_page_y,
            '0x8e': self.absolute
        }

    def zero_page(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        self.cpu.write_byte(address=zp_address, value=self.cpu.idx)

    def zero_page_y(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        self.cpu.write_byte(address=zp_address + self.cpu.idy, value=self.cpu.idx)
        ~self.cpu.clock

    def absolute(self):
        target_address = int(self.cpu.fetch_word(), base=0)
        self.cpu.write_byte(address=target_address, value=self.cpu.idx)


class STY(AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x84': self.zero_page,
            '0x94': self.zero_page_x,
            '0x8c': self.absolute
        }

    def zero_page(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        self.cpu.write_byte(address=zp_address, value=self.cpu.idy)

    def zero_page_x(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        self.cpu.write_byte(address=zp_address + self.cpu.idx, value=self.cpu.idy)
        ~self.cpu.clock

    def absolute(self):
        target_address = int(self.cpu.fetch_word(), base=0)
        self.cpu.write_byte(address=target_address, value=self.cpu.idy)


"""TRANSFER INSTRUCTIONS"""


class TAX(AbstractInstruction):

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


class TAY(AbstractInstruction):

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


class TXA(AbstractInstruction):

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


class TYA(AbstractInstruction):

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


class TSX(AbstractInstruction):

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


class TXS(AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x9a': self.implied
        }

    def implied(self):
        self.cpu.sp = self.cpu.idx
        ~self.cpu.clock


"""STACK OPERATIONS"""


class PHA(AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x48': self.implied
        }

    def implied(self):
        self.cpu.push_byte_on_stack(self.cpu.acc)


class PHP(AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x08': self.implied
        }

    def implied(self):
        bin_ps = self.cpu.convert_ps_to_binary()
        self.cpu.push_byte_on_stack(bin_ps)


class PLA(AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x68': self.implied
        }

    def implied(self):
        self.cpu.acc = int(self.cpu.pull_byte_from_stack(), base=0)


class PLP(AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x28': self.implied
        }

    def implied(self):
        self.cpu.convert_binary_to_ps()


"""LOGICAL OPERATIONS"""


class AND(AbstractInstruction):

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
        self.cpu.acc &= int(self.cpu.fetch_byte(), base=0)

    def zero_page(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        self.cpu.acc &= int(self.cpu.read_byte(zp_address), base=0)

    def zero_page_x(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        self.cpu.acc &= int(self.cpu.read_byte(np.ubyte(zp_address + self.cpu.idx)), base=0)
        ~self.cpu.clock

    def absolute(self):
        address = int(self.cpu.fetch_word(), base=0)
        self.cpu.acc &= int(self.cpu.read_byte(address), base=0)

    def absolute_x(self):
        address = int(self.cpu.fetch_word(), base=0)
        if (address >> 8) != ((address + self.cpu.idx) >> 8):
            ~self.cpu.clock
        self.cpu.acc &= int(self.cpu.read_byte(address + self.cpu.idx), base=0)

    def absolute_y(self):
        address = int(self.cpu.fetch_word(), base=0)
        if (address >> 8) != ((address + self.cpu.idy) >> 8):
            ~self.cpu.clock
        self.cpu.acc &= int(self.cpu.read_byte(address + self.cpu.idy), base=0)

    def indexed_indirect(self):
        zp_address = np.ubyte(int(self.cpu.fetch_byte(), base=0) + self.cpu.idx)
        ~self.cpu.clock
        address = int(self.cpu.read_word(zp_address), base=0)
        self.cpu.acc &= int(self.cpu.read_byte(address), base=0)

    def indirect_indexed(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        address = int(self.cpu.read_word(zp_address), base=0) + self.cpu.idy
        if (address >> 8) != ((address + self.cpu.idy) >> 8):
            ~self.cpu.clock
        self.cpu.acc &= int(self.cpu.read_byte(address), base=0)


class EOR(AbstractInstruction):

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
        self.cpu.acc ^= int(self.cpu.fetch_byte(), base=0)

    def zero_page(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        self.cpu.acc ^= int(self.cpu.read_byte(zp_address), base=0)

    def zero_page_x(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        self.cpu.acc ^= int(self.cpu.read_byte(np.ubyte(zp_address + self.cpu.idx)), base=0)
        ~self.cpu.clock

    def absolute(self):
        address = int(self.cpu.fetch_word(), base=0)
        self.cpu.acc ^= int(self.cpu.read_byte(address), base=0)

    def absolute_x(self):
        address = int(self.cpu.fetch_word(), base=0)
        if (address >> 8) != ((address + self.cpu.idx) >> 8):
            ~self.cpu.clock
        self.cpu.acc ^= int(self.cpu.read_byte(address + self.cpu.idx), base=0)

    def absolute_y(self):
        address = int(self.cpu.fetch_word(), base=0)
        if (address >> 8) != ((address + self.cpu.idy) >> 8):
            ~self.cpu.clock
        self.cpu.acc ^= int(self.cpu.read_byte(address + self.cpu.idy), base=0)

    def indexed_indirect(self):
        zp_address = np.ubyte(int(self.cpu.fetch_byte(), base=0) + self.cpu.idx)
        ~self.cpu.clock
        address = int(self.cpu.read_word(zp_address), base=0)
        self.cpu.acc ^= int(self.cpu.read_byte(address), base=0)

    def indirect_indexed(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        address = int(self.cpu.read_word(zp_address), base=0) + self.cpu.idy
        if (address >> 8) != ((address + self.cpu.idy) >> 8):
            ~self.cpu.clock
        self.cpu.acc ^= int(self.cpu.read_byte(address), base=0)


class ORA(AbstractInstruction):

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
        self.cpu.acc |= int(self.cpu.fetch_byte(), base=0)

    def zero_page(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        self.cpu.acc |= int(self.cpu.read_byte(zp_address), base=0)

    def zero_page_x(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        self.cpu.acc |= int(self.cpu.read_byte(np.ubyte(zp_address + self.cpu.idx)), base=0)
        ~self.cpu.clock

    def absolute(self):
        address = int(self.cpu.fetch_word(), base=0)
        self.cpu.acc |= int(self.cpu.read_byte(address), base=0)

    def absolute_x(self):
        address = int(self.cpu.fetch_word(), base=0)
        if (address >> 8) != ((address + self.cpu.idx) >> 8):
            ~self.cpu.clock
        self.cpu.acc |= int(self.cpu.read_byte(address + self.cpu.idx), base=0)

    def absolute_y(self):
        address = int(self.cpu.fetch_word(), base=0)
        if (address >> 8) != ((address + self.cpu.idy) >> 8):
            ~self.cpu.clock
        self.cpu.acc |= int(self.cpu.read_byte(address + self.cpu.idy), base=0)

    def indexed_indirect(self):
        zp_address = np.ubyte(int(self.cpu.fetch_byte(), base=0) + self.cpu.idx)
        ~self.cpu.clock
        address = int(self.cpu.read_word(zp_address), base=0)
        self.cpu.acc |= int(self.cpu.read_byte(address), base=0)

    def indirect_indexed(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        address = int(self.cpu.read_word(zp_address), base=0) + self.cpu.idy
        if (address >> 8) != ((address + self.cpu.idy) >> 8):
            ~self.cpu.clock
        self.cpu.acc |= int(self.cpu.read_byte(address), base=0)


class BIT(AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x24': self.zero_page,
            '0x2c': self.absolute
        }

    def zero_page(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        value = int(self.cpu.read_byte(zp_address), base=0)
        self.cpu.ps['zero_flag'] = ((value & self.cpu.acc) == 0)
        self.cpu.ps['overflow_flag'] = (value & 0b01000000)
        self.cpu.ps['negative_flag'] = (value & 0b10000000 != 0)

    def absolute(self):
        address = int(self.cpu.fetch_word(), base=0)
        value = int(self.cpu.read_byte(address), base=0)
        self.cpu.ps['zero_flag'] = ((value & self.cpu.acc) == 0)
        self.cpu.ps['overflow_flag'] = (value & 0b01000000)
        self.cpu.ps['negative_flag'] = (value & 0b10000000 != 0)


"""ARITHMETIC OPERATIONS"""


class ADC(AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x69': self.immediate,
            '0x65': self.zero_page,
            '0x75': self.zero_page_x,
            '0x6d': self.absolute,
            '0x7d': self.absolute_x,
            '0x79': self.absolute_y,
            '0x61': self.indirect_indexed,
            '0x71': self.indexed_indirect
        }

    def immediate(self):
        pass

    def zero_page(self):
        pass

    def zero_page_x(self):
        pass

    def absolute(self):
        pass

    def absolute_x(self):
        pass

    def absolute_y(self):
        pass

    def indexed_indirect(self):
        pass

    def indirect_indexed(self):
        pass


class SBC(AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xe9': self.immediate,
            '0xe5': self.zero_page,
            '0xf5': self.zero_page_x,
            '0xed': self.absolute,
            '0xfd': self.absolute_x,
            '0xf9': self.absolute_y,
            '0xe1': self.indirect_indexed,
            '0xf1': self.indexed_indirect
        }

    def immediate(self):
        pass

    def zero_page(self):
        pass

    def zero_page_x(self):
        pass

    def absolute(self):
        pass

    def absolute_x(self):
        pass

    def absolute_y(self):
        pass

    def indexed_indirect(self):
        pass

    def indirect_indexed(self):
        pass


class CMP(AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xc9': self.immediate,
            '0xc5': self.zero_page,
            '0xd5': self.zero_page_x,
            '0xcd': self.absolute,
            '0xdd': self.absolute_x,
            '0xd9': self.absolute_y,
            '0xc1': self.indirect_indexed,
            '0xd1': self.indexed_indirect
        }

    def immediate(self):
        pass

    def zero_page(self):
        pass

    def zero_page_x(self):
        pass

    def absolute(self):
        pass

    def absolute_x(self):
        pass

    def absolute_y(self):
        pass

    def indexed_indirect(self):
        pass

    def indirect_indexed(self):
        pass


class CPX(AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xe0': self.immediate,
            '0xe4': self.zero_page,
            '0xec': self.absolute
        }

    def immediate(self):
        pass

    def zero_page(self):
        pass

    def absolute(self):
        pass


class CPY(AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xc0': self.immediate,
            '0xc4': self.zero_page,
            '0xcc': self.absolute
        }

    def immediate(self):
        pass

    def zero_page(self):
        pass

    def absolute(self):
        pass


"""JUMPS AND CALLS"""


class JMP(AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x4c': self.absolute,
            '0x6c': self.indirect
        }

    def absolute(self):
        target_address = self.cpu.fetch_word()
        self.cpu.pc = int(target_address, base=0)

    def indirect(self):
        address = int(self.cpu.fetch_word(), base=0)
        target_address = self.cpu.read_word(address)
        self.cpu.pc = int(target_address, base=0)


class JSR(AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x20': self.absolute
        }

    def absolute(self):
        target_address = int(self.cpu.fetch_word(), base=0)
        self.cpu.push_word_on_stack(self.cpu.pc - 1)
        self.cpu.pc = target_address


class RTS(AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0x60': self.implied
        }

    def implied(self):
        return_point = self.cpu.pull_word_from_stack()
        self.cpu.pc = int(return_point, base=0) + 1  # To compensate for 1 pc increment
        ~self.cpu.clock


"""MISC"""


class NOP(AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xea': self.implied
        }

    def implied(self):
        self.cpu.pc += 1
        ~self.cpu.clock


class RES(AbstractInstruction):

    def __init__(self, cpu):
        super().__init__(cpu)
        self.opcodes = {
            '0xbb': self.implied
        }

    def implied(self):
        ~self.cpu.clock
        ~self.cpu.clock
        self.cpu.reset()
