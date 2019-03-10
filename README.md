Relax with `laxpy`. Let it handle your spatial queries for you!

laxpy is a way to read and write `.lax` files generated from `lasindex` in Python. I have ambitions to merge this into
the `laspy` codebase, but for now this standalone package can handle spatial queries in conjuction with `laspy` and 
presence of `.lax` files that match the name of the `.las` file you are interested in querying.

### Why Index?

Indexing LiDAR data is only relevant if the entire file is not needed. This most frequently happens when LiDAR files need
to be clipped using some geometry smaller than the original file extent. Indexing allows loading smaller chunks
of the file into memory, rather than the whole thing, at the cost of some initial overhead.

Whether or not indexing ultimately increases computational efficiency depends on the clipping geometry, and the structure
and size of the LiDAR file.

## Release Status

Current Release: 0.1

Status: `laxpy` is in a minimally working condition.

## Installation

```{bash}
# via pip
pip install laxpy

# via GitHub
git clone https://github.com/brycefrank/laxpy.git
cd laxpy
pip install .
```

## Example

### Clipping a Polygon

`laxpy` clips a `shapely` polygon by adjusting the memory map (an internal mechanism in `laspy`) of the original reference object.
Long story short, this is done in place in the following manner:

```{python}
from laxpy import IndexedLAS

my_las = IndexedLAS('my_las.las')
my_las.map_polygon(my_shapely_polygon)

# Print the points within the polygon
print(my_las.points)
```

Note that an `IndexedLAS` object inherits directly from `laspy.file.File`, and all dimensions are available for querying,
including `.x`, `.y`, etc. etc.

