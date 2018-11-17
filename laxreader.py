import struct
import laspy
import numpy as np

lax_path = 'data/44123F3324.lax'

# Starting at 15 is removing the header information
def read_lax(lax_path):
    stream = open(lax_path, 'rb')
    ints = []
    for i in range(15, 20570):
        stream.seek(i*4)
        unpack = struct.unpack('I', stream.read(4))[0]
        ints.append(unpack)

    return np.array(ints)

# We need to "build" the structure of the lax file using the 3rd element of ints

ints = read_lax(lax_path)

# Number of intervals in first cell
n0 = ints[2]
n0_int_ind = 4

# starting position of intervals for first cell
i=0
start_pos = 4 # Index of first interval
n = ints[2] # The number of intervals

cell_dict = {}

while i < 477: #for now
    cell_intervals = ints[start_pos:start_pos + n * 2]
    cell_id = ints[start_pos-3]

    cell_dict[cell_id] = cell_intervals

    start_pos = (start_pos + n*2 + 3)
    n = ints[start_pos - 2]
    #start_pos = start_pos + n * 2
    #print(start_pos)
    #n = ints[start_pos - 2]
    i+=1

print(list(cell_dict.keys()))





