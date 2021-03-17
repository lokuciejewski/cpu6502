from unittest.mock import patch

from cpu6502.cpu import CPU
from cpu6502.memory import Memory
from time import sleep

if __name__ == '__main__':
    cpu = CPU(speed_mhz=0.002)
    memory = Memory()
    if not memory.load_binary_file('move_val_around.bin', start_offset=0x1):
        print('Memory not loaded!')

    with patch.object(CPU, 'initialise_memory'):
        cpu.memory = memory
        cpu.reset(memory=memory)
        cpu.pc = 0x0
        cpu.memory[0] = 0x4c
    input('Ready')
    pc_ver = cpu.pc
    while True:
        #print(cpu)
        print([hex(byte) for byte in (cpu.memory[i] for i in range(0x31, 0x40, 1))], end='\r')
        cpu.execute(1)
        if pc_ver == cpu.pc:
            print(cpu)
            input('Program Counter may be trapped!')
        if cpu.pc == 32768:
            print('Program finished')
            break
        pc_ver = cpu.pc
