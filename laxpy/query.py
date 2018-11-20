# will hold functions for querying cell indices from a .las/x pair
from laspy.file import File
import os.path
import ntpath
from laxpy import file, tree

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

    def query_cell(self, cell_index):
        """
        Returns the point of a given cell index.

        :param cell_index:
        :return:
        """

        point_indices = self.parser.create_indices(cell_index)
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
