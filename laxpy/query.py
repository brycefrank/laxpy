# will hold functions for querying cell indices from a .las/x pair
from laspy.file import File
import os.path
import ntpath
from laxpy import file, tree
from numpy.lib.recfunctions import append_fields

class IndexedLAS(File):
    """
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

    def _scale_points(self, points):
        """
        Scales a set of queried points using the header offset and scale functions.

        :param points:
        :return: A set of scaled points.
        """

        x = ((points['point']['X'] * self.header.scale[0]) + self.header.offset[0])
        y = (points['point']['Y'] * self.header.scale[1]) + self.header.offset[1]
        z = (points['point']['Z'] * self.header.scale[2]) + self.header.offset[2]

        # Get list of columns that aren't X Y or Z
        avoid = ['X', 'Y', 'Z']
        other_columns = [column for column in points['point'].dtype.fields.keys() if column not in avoid]

        # TODO is there a way to avoid copying? Replace fields directly?
        out_points = points['point'][other_columns].copy()
        return append_fields(out_points, ('x', 'y', 'z'), (x, y, z))

    def query_cell(self, cell_index, scale=False):
        """
        Returns the point of a given cell index.

        :param cell_index:
        :param scale: Scale the output points using the header?
        :return:
        """

        point_indices = self.parser.create_indices(cell_index)

        if scale:
            return self._scale_points(self.points[point_indices])
        else:
            return self.points[point_indices]

    # TODO how to handle clipping? Leave it up to the user? Include pyfor's clipping function?
    def query_bounding_box(self):
        pass

    def query_polygon(self):
        pass

    def query_circle(self):
        pass

    def query_point(self):
        pass

    def other_func(self):
        pass
