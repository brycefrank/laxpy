import laspy

# Initialize a raw DataProvider
las = laspy.file.File('test.las')
manager = laspy.base.FileManager('test.las', mode='r')
data_provider = laspy.base.DataProvider('test.las', manager)

# Lets start from the top and work our way back

# First we get some dimension, X
print(manager.get_dimension('X'))

# This calls manager.get_dimension which
# 1. Checks if _pmap is bool, if so, then calls data_provider.point_map
# 2. creates a variable spec, which looks up the name ('X') in the point_format
print(manager.point_format.lookup['X'])

# This guy is a laspy.util.Spec object, and is used as an argument to the manager._get_dimension function
print(manager._get_dimension(manager.point_format.lookup['X']))

# Let's look at the internal manager._get_dimension really quick
# This just returns a call to data_provider._pmap['point'][spec.name], where spec is defined above as a function arg:

# So it seems the action is happening in the ._pmap, as expected. But the new discovery is that this spec guy is needed
# to use the _pmap. Perhaps this spec variable is some sort of memory address. Let's take a look.
from struct import unpack
def old_get_points(manager):
    if type(manager.point_refs) == bool:
        manager.build_point_refs()
    single_fmt = manager.point_format.pt_fmt_long[1:]
    fmtlen = len(single_fmt)
    big_fmt_string = "".join(["<", single_fmt*manager.header.point_records_count])
    pts = unpack(big_fmt_string, manager.data_provider._mmap[manager.header.data_offset:manager.data_provider._mmap.size()])
    return ((laspy.util.Point(manager, unpacked_list=pts[fmtlen * i:fmtlen * (i + 1)]) for i in range(manager.header.point_records_count)))

print(type(old_get_points(manager)))


