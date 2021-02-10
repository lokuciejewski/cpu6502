from cpu6502 import cpu

if __name__ == '__main__':
    cpu = cpu.CPU(speed_mhz=1)
    cpu.reset()
    print(cpu)
    cpu.memory[0xfffc] = 0x4c
    cpu.memory[0xfffd] = 0x00
    cpu.memory[0xfffe] = 0x02  # JMP 0x0200 - 1
    cpu.memory[0x0200] = 0xa9
    cpu.memory[0x0201] = 0x10  # LDA 0x10 - 2
    cpu.memory[0x0202] = 0x20  # JSR 0x0300 - 3
    cpu.memory[0x0203] = 0x00
    cpu.memory[0x0204] = 0x03
    cpu.memory[0x0205] = 0xa9
    cpu.memory[0x0206] = 0x05  # LDA 0x05 - 6
    cpu.memory[0x0207] = 0xbb  # RES
    cpu.memory[0x0300] = 0xa9
    cpu.memory[0x0301] = 0x09  # LDA 0x09 - 4
    cpu.memory[0x0302] = 0x60  # RTS - 5

    while True:
        input()
        cpu.execute(1)
        print(cpu)

