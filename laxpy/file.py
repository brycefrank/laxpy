import struct
import numpy as np
import os
import subprocess

class LAXParser:
    """
    Parses a `.lax` file and generates point index intervals.

    :param path: The path of the input `.lax` file.
    """
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
        raise NotImplementedError('To be implemented.')
        pass

    @property
    def cells(self):
        """
        :return: A dictionary of cell_index: [cell_intervals] key, value pairs.
        """

        # Index of first interval
        start_pos = 19

        cell_dict = {}

        n = self.parsed_bytes[17] # The number of intervals of the first cell
        for i in range(self.number_cells-1):
            cell_intervals = self.parsed_bytes[start_pos:start_pos + n * 2]
            cell_id = self.parsed_bytes[start_pos-3]
            cell_dict[cell_id] = cell_intervals

            start_pos = (start_pos + n*2 + 3)
            n = self.parsed_bytes[start_pos - 2]

        return cell_dict

    def create_point_indices(self, cell_index):
        """
        The values in the self.cells dictionary are the raw intervals. This function converts those raw intervals
        into a set of point indices that can be passed to the `laspy.file.File` memory map.

        :param cell_index: The cell index to generate point indices for.
        :return: An `ndarray` of indices of points associated with the cell specified by `cell_index`
        """

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
        if any(in_path):
            lasindex_binary = binary
            break
    else:
        raise(FileNotFoundError, "lasindex was not found on the system")

    prc = subprocess.Popen([lasindex_binary, "-i", path])
    prc.communicate()




