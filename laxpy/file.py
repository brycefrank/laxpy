import struct
import laspy
import numpy as np

lax_path = 'data/44123F3324.lax'

class LAXParser:
    """A class for parsing a .lax file"""
    def __init__(self, path):
        stream = open(path, 'rb')
        self.parsed_bytes = []

        # TODO get rid of hard-coded positions?
        self.bbox = []
        for i in range(9, 13):
            stream.seek(i*4)
            unpack = struct.unpack('f', stream.read(4))[0]
            self.bbox.append(unpack)

        # 20570
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

    def create_indices(self, cell_index):
        indices = []
        i = 0
        bounds = self.cell_dict[cell_index]
        while i < len(bounds):
            indices.append(np.arange(bounds[i], bounds[i + 1] + 1))
            i += 2

        return np.concatenate(indices)


class IndexParser:
    """
    Really a proto-quadtree that can find the "path" of a given cell index to the root of the tree. This provides the \
    position of the cell in 2-dimensional space. An untested theory that this is how .lax indices are used.
    """
    def __init__(self, lax_parser):
        self.lax_parser = lax_parser
        self.max_index = np.max(list(self.lax_parser.cell_dict.keys()))

    @property
    def tree_level_sizes(self):
        level_sizes = []

        i=0
        while True:
            # TODO this returns one too many levels
            max_cells_level = 4**i
            level_sizes.append(max_cells_level)
            if max_cells_level > self.max_index:
                return(level_sizes)
            i+=1

    @property
    def level_edges(self):
        left_edge = np.cumsum(self.tree_level_sizes)
        right_edge = left_edge*4
        return {k + 1: v for k, v in enumerate(zip(left_edge, right_edge))}

    def get_cell_level_edges(self, cell_index):
        for level, edges in self.level_edges.items():
            if cell_index >= edges[0] and cell_index <= edges[1]:
                return level, edges

    def get_parent_cell(self, cell_index):
        cell_level, cell_edges = self.get_cell_level_edges(cell_index)
        lb = cell_edges[0]
        offset = (cell_index - lb) + 1
        parent_offset = np.ceil(offset / 4)

        try:
            parent_lb = self.level_edges[cell_level - 1][0]
            parent_index = (parent_lb + parent_offset) - 1
            return np.int(parent_index)
        except KeyError: # we are at the root
            return 0

    def trace_back(self, cell_index):
        """
        Finds the "path" of a cell index back to the root. Used to position the cell in geographic space (later)
        :param cell_index:
        :return:
        """
        trace = []
        while cell_index != 0:
            position = ((cell_index-1)%4)+1 # the position of this cell relative to its siblings (1, 2, 3 or 4)
            cell_index = self.get_parent_cell(cell_index)
            trace.append((cell_index, position))
        return trace

    def get_cell_bbox(self, cell_index):
        """
        Positions the cell in 2 dimensional space
        :return:
        """
        trace = self.trace_back(cell_index)

        # Get bounding box of .las file
        minx, maxx, miny, maxy = self.lax_parser.bbox

        # Compute the widths of the children
        x_width = (maxx - minx) / 2
        y_width = (maxy - miny) / 2

        for cell_index, position in reversed(trace):
            if position == 1:
                minx, miny = minx, miny
            elif position == 2:
                minx, miny = minx + x_width, miny
            elif position == 3:
                minx, miny = minx, miny + y_width
            elif position == 4:
                minx, miny = minx + x_width, miny + y_width

            x_width = x_width / 2
            y_width = y_width / 2

        return((minx, minx+x_width, miny, miny + y_width))

lax = LAXParser(lax_path)
proto_tree = IndexParser(lax)

print(lax.cell_dict.keys())

query_cell = 961

print(proto_tree.get_cell_bbox(query_cell))
inds = lax.create_indices(query_cell)

#import laspy
#las = laspy.file.File('data/44123F3324.las')
#print(las.points[inds])


def plot_lax(lax):
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    fig, ax = plt.subplots(1)
    for i in lax.cell_dict.keys():
        bbox = proto_tree.get_cell_bbox(i)
        rect = patches.Rectangle((bbox[0], bbox[2]), (bbox[1] - bbox[0])*2, (bbox[3] - bbox[2])*2, edgecolor='black', facecolor='none', label=i)
        ax.annotate(i, (bbox[0], bbox[2]))
        ax.add_patch(rect)
    plt.xlim(lax.bbox[0], lax.bbox[1])
    plt.ylim(lax.bbox[2], lax.bbox[3])
    plt.show()

