import numpy as np

class LAXTree:
    """
    This class constructs the structure of the quadtree described by the `.lax` file.

    :param lax_parser: A `LAXParser` object.
    """
    def __init__(self, lax_parser):
        self.lax_parser = lax_parser
        self.max_index = np.max(list(self.lax_parser.cells.keys()))

    @property
    def tree_level_sizes(self):
        """
        :return: A list of level sizes, where size describes the number of potential cells contained in a given level.
        """
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
        """
        :return: A dictionary of level_index: (left_edge, right_edge) key, value pairs. An edge describes the index
        of a cell that is either the "left most" or "right most" cell in a given level, provided that the cell indices
        are written in order.
        """
        left_edge = np.cumsum(self.tree_level_sizes)
        right_edge = left_edge*4
        return {k + 1: v for k, v in enumerate(zip(left_edge, right_edge))}

    def get_cell_level_edges(self, cell_index):
        """
        :param cell_index: A cell_index to get the edges for.
        :return: A tuple (level_index, edges) that describes the left edge and right edge for a given `cell_index`.
        """
        for level_index, edges in self.level_edges.items():
            if cell_index >= edges[0] and cell_index <= edges[1]:
                return level_index, edges

    def get_parent_cell(self, cell_index):
        """
        :return: Returns the parent cell_index for an input `cell_index`.
        """
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
        :param cell_index: A cell_index to get the trace_back of.
        :return: A list of cell indices that represents the `cell_index`'s lineage.
        """
        trace = []
        while cell_index != 0:
            position = ((cell_index-1)%4)+1 # the position of this cell relative to its siblings (1, 2, 3 or 4)
            cell_index = self.get_parent_cell(cell_index)
            trace.append((cell_index, position))
        return trace

    def get_cell_bbox(self, cell_index):
        """
        Positions the cell in 2 dimensional space.

        :return: A length-4 tuple bounding box (minx, maxx, miny, maxy).
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

        return((minx, minx+(x_width*2), miny, miny + (y_width*2)))

    @property
    def cell_polygons(self):
        """
        :return: A dictionary of cell_index: polygon pairs where `polygon` is of type `shapely.geometry.Polygon`
        """
        from shapely.geometry import Polygon

        polygons = {}
        for cell_index in self.lax_parser.cells:
            minx, maxx, miny, maxy = self.get_cell_bbox(cell_index)
            polygon = Polygon([(minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny)])
            polygons[cell_index] = polygon

        return polygons

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

    def to_gdf(self, crs):
        """
        Exports the geometries to shapefile for debugging purposes.
        """
        import geopandas as gpd
        import pandas as pd

        df = pd.DataFrame({'bbox':list(self.cell_polygons.values()),'id': list(self.cell_polygons.keys())})
        gdf = gpd.GeoDataFrame(df)
        gdf = gdf.set_geometry('bbox')
        gdf.crs = crs

        return(gdf)



