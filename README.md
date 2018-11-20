Relax with `laxpy`. Let it handle your spatial queries for you!

laxpy is a way to read and write `.lax` files generated from `lasindex` in Python. I have ambitions to merge this into
the `laspy` codebase, but for now this standalone package can handle spatial queries in conjuction with `laspy` and 
presence of `.lax` files that match the name of the `.las` file you are interested in querying.


## Release Status

Current Release: 0.0.1

Status: `laxpy` is currently under development.


**laxpy is in a development phase** with version 0.1.0 planned for December, 2018

## Example

```{python}
from laxpy import IndexedLAS

my_las = IndexedLAS('my_las.las')

# Return all points in the quad tree cell with index 14
my_las.query_cell(14)

## FORTHCOMING ##
my_las.query_bounding_box()
my_las.query_polygon()
#etc.
```