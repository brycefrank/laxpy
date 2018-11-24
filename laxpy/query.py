# will hold functions for querying cell indices from a .las/x pair
from laspy.file import File
import os.path
import ntpath
from laxpy import file, tree, clip
from shapely.geometry import Point, Polygon
import numpy as np

class IndexedLAS(File):
    """
    The main interface for interacting with indexed `.las` files. An `IndexedLAS` wraps a `laspy.file.File`
    and thereby has all of its functionality. When this class is initialized it checks if an existing `.lax` file that
    matches the name of the input `.las` file exists in the same directory. If not such file exists please use `lasindex`
    to create a matching `.lax` file.

    :param path: The path of a `.las` file to index.
    """

    def __init__(self, path):
        super().__init__(path)

        # Check if matching `.lax` file is present.
        parent_dir = os.path.join(os.path.abspath(os.path.join(self.filename, os.pardir)))
        las_name = os.path.splitext(ntpath.basename(self.filename))[0]
        self.lax_path = os.path.join(parent_dir, las_name + '.lax')

        if not os.path.isfile(self.lax_path):
            raise FileNotFoundError('A matching .lax file was not found.')

        # Parse the lax file and generate the tree
        self.parser = file.LAXParser(self.lax_path)
        self.tree = tree.LAXTree(self.parser)

    def _query_cell(self, cell_index):
        """
        Returns the points of a given cell index. This is generally used internally.

        :param cell_index: The index of a quadtree cell.
        :return:
        """

        # TODO if iterable then merge the intervals (may need a separate function)
        point_indices = self.parser.create_point_indices(cell_index)
        return self.points[point_indices]

    def query_polygon(self, q_polygon):
        point_indices = []
        for cell_index, polygon in self.tree.cell_polygons.items():
            if polygon.intersects(q_polygon):
                point_indices.append(self.parser.create_point_indices(cell_index))

        point_indices = np.unique(np.concatenate(point_indices))

        x_scale, y_scale, z_scale = self.header.scale
        x_off, y_off, z_off = self.header.offset

        x = (x_scale * self.points[point_indices]['point']['X']) + x_off
        y = (y_scale * self.points[point_indices]['point']['Y']) + y_off

        keep = clip.ray_trace(x, y, q_polygon)

        return self.points[point_indices[keep]]


    def query_bounding_box(self, bbox):
        """

        :param bbox: A an iterable of bounding box coordinates in the format (minx, maxx, miny, maxy).
        """

        minx, maxx, miny, maxy = bbox
        bbox_polygon = Polygon([(minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny)])
        return self.query_polygon(bbox_polygon)

    def query_point(self, x, y):
        # TODO could a point ever return more than one cell?
        point = Point(x, y)
        for cell_index, polygon in self.tree.cell_polygons.items():
            if polygon.contains(point):
                self._query_cell(cell_index)
