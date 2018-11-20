import struct
import laspy
import numpy as np
import os
import subprocess

class LAXParser:
    """A class for parsing a .lax file"""
    def __init__(self, path):
        stream = open(path, 'rb')
        self.parsed_bytes = []

        # TODO get rid of hard-coded positions?
        # TODO also the loops are silly
        self.bbox = []
        for i in range(9, 13):
            stream.seek(i*4)
            unpack = struct.unpack('f', stream.read(4))[0]
            self.bbox.append(unpack)

        stream.seek(15 * 4)
        self.number_cells = struct.unpack('I', stream.read(4))[0]

        for i in range(0, np.int(os.stat(path).st_size/4)):
            stream.seek(i*4)
            unpack = struct.unpack('I', stream.read(4))[0]
            self.parsed_bytes.append(unpack)

    def header(self):
        pass

    @property
    def cells(self):
        # starting position of intervals for first cell
        start_pos = 19 # Index of first interval

        cell_dict = {}
        n = self.parsed_bytes[17] # The number of intervals of the first cell
        for i in range(self.number_cells-1): #for now
            cell_intervals = self.parsed_bytes[start_pos:start_pos + n * 2]
            cell_id = self.parsed_bytes[start_pos-3]
            cell_dict[cell_id] = cell_intervals

            start_pos = (start_pos + n*2 + 3)
            n = self.parsed_bytes[start_pos - 2]

        return cell_dict

    def create_indices(self, cell_index):
        indices = []
        i = 0
        bounds = self.cells[cell_index]
        while i < len(bounds):
            indices.append(np.arange(bounds[i], bounds[i + 1] + 1))
            i += 2

        return np.concatenate(indices)

def init_lax(path):
    """
    Creates a .lax file for a specified .las file. A simple wrapper for lasindex CLI tool.
    :return:
    """

    # Mimicking laspy.base.read_compressed
    lasindex_names = ['lasindex']
    lasindex_binary = ''

    for binary in lasindex_names:
        in_path = [os.path.isfile(os.path.join(x, binary)) for x in os.environ['PATH'].split(os.pathsep)]
        print(in_path)
        if any(in_path):
            lasindex_binary = binary
            break
    else:
        raise(FileNotFoundError, "lasindex was not found on the system")

    prc = subprocess.Popen([lasindex_binary, "-i", path])
    prc.communicate()




