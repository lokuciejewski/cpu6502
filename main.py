from unittest.mock import patch

from cpu6502.cpu import CPU
from cpu6502.memory import Memory

if __name__ == '__main__':
    cpu = CPU(speed_mhz=1)
    memory = Memory()
    memory.load_binary_file('cpu6502/tests/6502_functional_test.bin', start_offset=0xa)

    with patch.object(CPU, 'initialise_memory'):
        cpu.memory = memory
        cpu.reset()
        cpu.pc = 0x400
        print(cpu)

    pc_ver = cpu.pc
    while True:
        cpu.execute(1)
        print(cpu)
        if pc_ver == cpu.pc:
            input('Program Counter may be trapped!')
        pc_ver = cpu.pc