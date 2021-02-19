import json

from cpu6502.instructions.arithmetic import ADC, SBC, CMP, CPX, CPY
from cpu6502.instructions.branch import BCC, BCS, BEQ, BMI, BNE, BPL, BVC, BVS
from cpu6502.instructions.decrement import DEC, DEX, DEY
from cpu6502.instructions.flag_change import CLC, CLD, CLI, CLV, SEC, SED, SEI
from cpu6502.instructions.increment import INC, INX, INY
from cpu6502.instructions.jump import JMP, JSR, RTS
from cpu6502.instructions.load import LDA, LDX, LDY
from cpu6502.instructions.logical import AND, EOR, ORA, BIT
from cpu6502.instructions.misc import NOP, RES
from cpu6502.instructions.shift import ASL, LSR, ROL, ROR
from cpu6502.instructions.stack import PHA, PHP, PLA, PLP
from cpu6502.instructions.store import STA, STX, STY
from cpu6502.instructions.transfer import TAX, TAY, TXA, TYA, TSX, TXS


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
            'ADC': ADC,
            'SBC': SBC,
            'CMP': CMP,
            'CPX': CPX,
            'CPY': CPY,
            # INCREMENT AND DECREMENT
            'INC': INC,
            'INX': INX,
            'INY': INY,
            'DEC': DEC,
            'DEX': DEX,
            'DEY': DEY,
            # SHIFTS
            'ASL': ASL,
            'LSR': LSR,
            'ROL': ROL,
            'ROR': ROR,
            # BRANCHES
            'BCC': BCC,
            'BCS': BCS,
            'BEQ': BEQ,
            'BMI': BMI,
            'BNE': BNE,
            'BPL': BPL,
            'BVC': BVC,
            'BVS': BVS,
            # FLAG CHANGES
            'CLC': CLC,
            'CLD': CLD,
            'CLI': CLI,
            'CLV': CLV,
            'SEC': SEC,
            'SED': SED,
            'SEI': SEI,
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
