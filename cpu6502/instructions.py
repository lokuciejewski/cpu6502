import json
from abc import abstractmethod


class Instructions:

    def __init__(self, cpu, filepath: str):
        self.opcodes = {}
        self.internal_assignment = {
            'LDA': LDA,
            'LDX': LDX,
            'LDY': LDY,
            'STA': STA,
            'STX': STX,
            'STY': STY,
            'TAX': TAX,
            'TAY': TAY,
            'TXA': TXA,
            'TYA': TYA,
            'JMP': JMP,
            'JSR': JSR,
            'RTS': RTS,
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


"""LOAD/STORE instructions"""


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
        if (address >> 8) != ((address + self.cpu.idy) >> 8):
            ~self.cpu.clock
        self.cpu.acc = int(self.cpu.read_byte(address), base=0)


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
        self.cpu.ps['negative_flag'] = self.cpu.idx > 0b01111111  # Set negative flag if bit 7 of acc is set

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
        address = int(self.cpu.read_word(self.cpu.pc), base=0)
        self.cpu.idx = int(self.cpu.read_byte(address), base=0)

    def absolute_y(self):
        address = int(self.cpu.read_word(self.cpu.pc), base=0)
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
        self.cpu.ps['negative_flag'] = self.cpu.idy > 0b01111111  # Set negative flag if bit 7 of acc is set

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
        address = int(self.cpu.read_word(self.cpu.pc), base=0)
        self.cpu.idy = int(self.cpu.read_byte(address), base=0)

    def absolute_x(self):
        address = int(self.cpu.read_word(self.cpu.pc), base=0)
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
        zp_address = int(self.cpu.read_byte(self.cpu.pc), base=0) + self.cpu.idx
        ~self.cpu.clock
        address = int(self.cpu.read_word(zp_address), base=0)
        self.cpu.write_byte(address=address, value=self.cpu.acc)

    def indirect_indexed(self):
        zp_address = int(self.cpu.read_byte(self.cpu.pc), base=0)
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


"""REGISTER TRANSFER instructions"""


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
        self.cpu.ps['negative_flag'] = self.cpu.idx > 0b01111111  # Set negative flag if bit 7 of acc is set


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
        self.cpu.ps['negative_flag'] = self.cpu.idy > 0b01111111  # Set negative flag if bit 7 of acc is set


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
        self.cpu.ps['negative_flag'] = self.cpu.acc > 0b01111111  # Set negative flag if bit 7 of acc is set


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
        self.cpu.ps['negative_flag'] = self.cpu.acc > 0b01111111  # Set negative flag if bit 7 of acc is set


"""JUMPS AND CALLS"""


class JMP(AbstractInstruction):

    def __init__(self, cpu):
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
        return_point = self.cpu.pop_word_from_stack()
        self.cpu.pc = int(return_point, base=0) + 1  # To compensate for 1 pc increment
        ~self.cpu.clock


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
