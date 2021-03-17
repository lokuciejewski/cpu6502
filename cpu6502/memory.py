import RPi.GPIO as GPIO
import numpy as np
from time import sleep

class Memory:
    MAX_SIZE = 1024 * 34  # memory can be accessed up to 0xFFFF

    def __init__(self):
        self.address = [2, 3, 4, 17, 27, 22, 10, 9, 11, 0, 5, 6, 13, 19, 26]
        self.data = [25, 8, 7, 1, 12, 16, 20, 21]
        self.we = 23
        self.oe = 24
        self.ce = 18

        GPIO.setmode(GPIO.BCM)

        for bit in self.address:
            GPIO.setup(bit, GPIO.OUT)

        self._set_pins_in_input_mode()  # To read from the pins

        GPIO.setup(self.oe, GPIO.OUT)
        GPIO.setup(self.we, GPIO.OUT)
        GPIO.setup(self.ce, GPIO.OUT)

        GPIO.output(self.oe, 0)
        self.chip_select()
        self.set_read_state(True)
        self.chip_deselect()

    def _set_pins_in_output_mode(self):
        for bit in self.data:
            GPIO.setup(bit, GPIO.OUT)

    def _set_pins_in_input_mode(self):
        for bit in self.data:
            GPIO.setup(bit, GPIO.IN)
    
    def set_read_state(self, new_state: bool):
        sleep(1e-9)
        GPIO.output(self.we, new_state)
        if new_state:
            self._set_pins_in_input_mode()
        else:
            self._set_pins_in_output_mode()

    def chip_select(self):
        GPIO.output(self.ce, 0)

    def chip_deselect(self):
        for bit in self.address:
                GPIO.output(bit, 0)
        GPIO.output(self.ce, 1)

    def __str__(self) -> str:
        res = ''
        for item in self.data:
            res += f'{hex(item)}\n'
        return res

    def __getitem__(self, item) -> np.ubyte:
        address = self.convert_value_to_list(item, 15)
        # Set address lines
        for i, bit in enumerate(self.address):
            GPIO.output(bit, address[i])
        # Read data lines
        self.chip_select()
        self.set_read_state(True)
        data_to_read = 0
        for i, bit in enumerate(reversed(self.data)):
            data_to_read += (2**i) * GPIO.input(bit)
        self.chip_deselect()
        return data_to_read

    def __setitem__(self, key: np.short, value: np.ubyte):
        value = self.convert_value_to_list(value, 8)
        address = self.convert_value_to_list(key, 15)
        # Set address lines 
        for i, bit in enumerate(self.address):
            GPIO.output(bit, address[i])
        # Set data lines
        self.chip_select()
        self.set_read_state(False)
        for i, bit in enumerate(self.data):
            GPIO.output(bit, value[i])
        self.set_read_state(True)
        self.chip_deselect()

    def convert_value_to_list(self, value: int, length: int) -> list:
        result = bin(value)
        result = result.split('b')[1].zfill(length)
        return [int(bit) for bit in result]

    def get_values(self, address: np.ushort, n: int) -> list:
        """
        Method to return next n values starting from address
        :param address: np.ushort: Address of the first value
        :param n: int: Number of values to be added to the result
        :return: list: List of n values
        """
        return [hex(val) for val in self.data[address: address + n]]

    def get_stack(self, n: int) -> list:
        """
        Method to get all stack contents
        :param n: int: Number of values to be added to the list
        :return: list: List of all values on stack
        """
        return [hex(val) for val in self.data[0x01ff - n: 0x01ff]]

    def load_binary_file(self, filepath: str, start_offset: int) -> bool:
        """
        Method to load a binary file into the memory
        :param filepath: str: Path to the binary file
        :param start_offset: int: Starting offset (first byte where the memory is loaded to)
        :return: bool: True if successful, False otherwise
        """
        file_data = np.fromfile(filepath, dtype=np.ubyte)
        for i in range(len(file_data)):
            self[i] = file_data[i]
        sleep(0.1)
        for i in range(len(file_data)):
            if self[i] != file_data[i]:
                print(f'Write error on {hex(i)}')
                self[i] = file_data[i]
            else:
                print(f'{hex(i)} OK - {hex(file_data[i])}')
        self.chip_deselect()
        self.chip_select()
        return True
