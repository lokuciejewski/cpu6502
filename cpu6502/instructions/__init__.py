from abc import abstractmethod

import numpy as np


class AbstractInstruction:
    """
    Abstract class which all instructions should inherit from. It needs to be in __init__.py in order to be accessed
    without any circular import errors.
    """

    @abstractmethod
    def __init__(self, cpu):
        """
        Method to specify events that happen for every type of addressing before the instruction is executed
        :param cpu: CPU: Cpu object which the instructions will be executed on
        """
        self.opcodes = {}
        self.cpu = cpu
        self.cpu.ps['reserved'] = True
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
        self.cpu.ps['reserved'] = True
        pass

    # All addressing modes pushed here for easier and faster testing

    def immediate(self):
        return int(self.cpu.fetch_byte(), base=0)

    def zero_page(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        return zp_address

    def zero_page_x(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        ~self.cpu.clock
        return np.ubyte(zp_address + self.cpu.idx)

    def zero_page_y(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        ~self.cpu.clock
        return np.ubyte(zp_address + self.cpu.idy)

    def absolute(self):
        address = int(self.cpu.fetch_word(), base=0)
        return address

    def absolute_x(self):
        address = int(self.cpu.fetch_word(), base=0)
        if (address >> 8) != ((address + self.cpu.idx) >> 8):
            ~self.cpu.clock
        return address + self.cpu.idx

    def absolute_y(self):
        address = int(self.cpu.fetch_word(), base=0)
        if (address >> 8) != ((address + self.cpu.idy) >> 8):
            ~self.cpu.clock
        return address + self.cpu.idy

    def indexed_indirect(self):
        zp_address = np.ubyte(int(self.cpu.fetch_byte(), base=0) + self.cpu.idx)
        ~self.cpu.clock
        address = int(self.cpu.read_word(zp_address), base=0)
        return address

    def indirect_indexed(self):
        zp_address = int(self.cpu.fetch_byte(), base=0)
        address = int(self.cpu.read_word(zp_address), base=0) + self.cpu.idy
        if (address >> 8) != ((address + self.cpu.idy) >> 8):
            ~self.cpu.clock
        return address

    def implied(self):
        # Too many different methods to generalise
        pass
