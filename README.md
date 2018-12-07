Relax with `laxpy`. Let it handle your spatial queries for you!

laxpy is a way to read and write `.lax` files generated from `lasindex` in Python. I have ambitions to merge this into
the `laspy` codebase, but for now this standalone package can handle spatial queries in conjuction with `laspy` and 
presence of `.lax` files that match the name of the `.las` file you are interested in querying.


## Release Status

Current Release: 0.0.2

Status: `laxpy` is currently under development.

**laxpy is in a development phase** with minimally working version (0.1.0) planned for December, 2018

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

```{python}
from laxpy import IndexedLAS

my_las = IndexedLAS('my_las.las')

# Return all points in the provided bounding box
my_las.query_bounding_box()
my_las.query_bounding_box((405000, 405300, 3276400, 3276450))

# IndexedLAS inherits from laspy.file.File
print(my_las.points)
```

