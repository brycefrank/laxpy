from laxpy import *
import unittest
import os

data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
test_las = os.path.join(data_dir, 'test.las')
test_lax = os.path.join(data_dir, 'test.lax')

class LAXParserTestCase(unittest.TestCase):
    def setUp(self):
        self.test_parser = file.LAXParser(test_lax)

    def test_cells(self):
        self.assertEqual(len(self.test_parser.cells), 39)

    def test_create_indices(self):
        self.test_parser.create_point_indices(14)

class LAXTreeTestCase(unittest.TestCase):
    def setUp(self):
        self.test_tree = tree.LAXTree(file.LAXParser(test_lax))

    def test_tree_level_sizes(self):
        self.assertListEqual(self.test_tree.tree_level_sizes, [1, 4, 16, 64, 256, 1024])

    def test_level_edges(self):
        self.assertDictEqual(self.test_tree.level_edges, {1: (1, 4), 2: (5, 20), 3: (21, 84), 4: (85, 340), 5: (341, 1364), 6: (1365, 5460)})

    def test_get_cell_level_edges(self):
        self.assertEqual(self.test_tree.get_cell_level_edges(14), (2, (5, 20)))

    def test_get_parent_cell(self):
        self.assertEqual(self.test_tree.get_parent_cell(14), 3)

    def test_trace_back(self):
        self.assertListEqual(self.test_tree.trace_back(14), [(3,2), (0,3)])
