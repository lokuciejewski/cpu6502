from unittest.mock import patch

from cpu6502.cpu import CPU
from cpu6502.memory import Memory

if __name__ == '__main__':
    cpu = CPU(speed_mhz=1)
    memory = Memory()
    memory[0xfffc] = 0x00
    memory[0xfffd] = 0x02
    memory[0x0200] = 0xa9
    memory[0x0201] = 0x10  # LDA 0x10 - 2
    memory[0x0202] = 0x20  # JSR 0x0300 - 3
    memory[0x0203] = 0x00
    memory[0x0204] = 0x03
    memory[0x0205] = 0xa9
    memory[0x0206] = 0x05  # LDA 0x05 - 6
    memory[0x0207] = 0xbb  # RES
    memory[0x0300] = 0xa9
    memory[0x0301] = 0x09  # LDA 0x09 - 4
    memory[0x0302] = 0x60  # RTS - 5

    with patch.object(CPU, 'initialise_memory'):
        cpu.memory = memory
        cpu.reset()
        print(cpu)

    while True:
        input()
        cpu.execute(1)
        print(cpu)

