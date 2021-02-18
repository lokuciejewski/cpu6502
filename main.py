from unittest.mock import patch

from cpu6502.cpu import CPU
from cpu6502.memory import Memory

if __name__ == '__main__':
    cpu = CPU(speed_mhz=1)
    memory = Memory()
    memory[0xfffc] = 0x00
    memory[0xfffd] = 0x02
    memory[0x0200] = 0xa9  # LDA 0x10
    memory[0x0201] = 0x10
    memory[0x0202] = 0xe9  # SBC 0x01
    memory[0x0203] = 0x04

    with patch.object(CPU, 'initialise_memory'):
        cpu.memory = memory
        cpu.reset()
        print(cpu)

    while True:
        input()
        cpu.execute(1)
        print(cpu)
