import numpy as np


class Memory:
    MAX_SIZE = 1024 * 64  # memory can be accessed up to 0xFFFF

    def __init__(self):
        self.data = np.zeros(Memory.MAX_SIZE, dtype=np.ubyte)

    def __str__(self) -> str:
        res = ''
        for item in self.data:
            res += f'{hex(item)}\n'
        return res

    def __getitem__(self, item) -> np.ubyte:
        return self.data[item]

    def __setitem__(self, key: np.short, value: np.ubyte):
        self.data[key] = value

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
        self.data = np.fromfile(filepath, dtype=np.ubyte)
        offset_array = np.zeros(shape=start_offset, dtype=np.ubyte)
        self.data = np.append(offset_array, self.data)
        return True
