import struct
import laspy
import numpy as np

lax_path = 'data/44123F3324.lax'

class LAXParser:
    """A class for parsing a .lax file"""
    def __init__(self, path):

        stream = open(path, 'rb')
        self.parsed_bytes = []

        for i in range(0, 20570):
            stream.seek(i*4)
            unpack = struct.unpack('I', stream.read(4))[0]
            self.parsed_bytes.append(unpack)

        self.number_cells = self.parsed_bytes[15]

    @property
    def cell_dict(self):
        # starting position of intervals for first cell
        start_pos = 19 # Index of first interval
        n = self.parsed_bytes[17] # The number of intervals

        cell_dict = {}
        for i in range(self.number_cells-1): #for now
            cell_intervals = self.parsed_bytes[start_pos:start_pos + n * 2]
            cell_id = self.parsed_bytes[start_pos-3]
            cell_dict[cell_id] = cell_intervals

            start_pos = (start_pos + n*2 + 3)
            n = self.parsed_bytes[start_pos - 2]

        return cell_dict

    def create_indices(self):
        print()

lax = LAXParser(lax_path)

a = np.array(list(lax.cell_dict.keys()))
a.sort()

print(a)



