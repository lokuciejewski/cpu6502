from unittest.mock import patch

from cpu6502.cpu import CPU
from cpu6502.memory import Memory

if __name__ == '__main__':
    cpu = CPU(speed_mhz=1)
    memory = Memory()
    memory.load_binary_file('cpu6502/colours.bin', start_offset=0x0)

    with patch.object(CPU, 'initialise_memory'):
        cpu.memory = memory
        cpu.reset(memory=memory)
        cpu.pc = 0x0

    pc_ver = cpu.pc
    while True:
        print(cpu)
        cpu.execute(1)
        input()
        # cpu.io.refresh()
        if pc_ver == cpu.pc:
            print(cpu)
            input('Program Counter may be trapped!')
        if cpu.pc == 0xffff:
            print('Program finished')
            break
        pc_ver = cpu.pc
