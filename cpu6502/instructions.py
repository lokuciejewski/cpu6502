import json
from abc import abstractmethod


class Instructions:

    def __init__(self, cpu, filepath: str):
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
        self.cpu.acc = int(self.cpu.read_byte(address), base=0)


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
