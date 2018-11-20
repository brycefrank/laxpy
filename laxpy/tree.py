import numpy as np

class LAXTree:
    """
    Really a proto-quadtree that can find the "path" of a given cell index to the root of the tree. This provides the \
    position of the cell in 2-dimensional space. An untested theory that this is how .lax indices are used.
    """
    def __init__(self, lax_parser):
        self.lax_parser = lax_parser
        self.max_index = np.max(list(self.lax_parser.cells.keys()))

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

    def plot(self):
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches


        fig, ax = plt.subplots(1)
        for i in self.lax_parser.cells.keys():
            bbox = self.get_cell_bbox(i)
            rect = patches.Rectangle((bbox[0], bbox[2]), (bbox[1] - bbox[0])*2, (bbox[3] - bbox[2])*2, edgecolor='black', facecolor='none', label=i)
            ax.annotate(i, (bbox[0], bbox[2]))
            ax.add_patch(rect)
        plt.xlim(self.lax_parser.bbox[0], self.lax_parser.bbox[1])
        plt.ylim(self.lax_parser.bbox[2], self.lax_parser.bbox[3])
        plt.show()
