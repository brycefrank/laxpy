import laspy
import numpy as np
import matplotlib.pyplot as plt

las1 = laspy.file.File('data/44123F3324.las')

# Interval boundaries
bounds = [16051576, 16319487, 16389438, 16534740, 17358089, 17358138, 19935977, 19948902, 19954656, 19972198, 20248035, 20259370]

# We want to convert these boundaries to all of the indices so we can use it as a numpy index

def generate_indices_from_edges():
    indices = []
    i=0
    while i < len(bounds):
        indices.append(np.arange(bounds[i], bounds[i+1]+1))
        i+=2

    return np.concatenate(indices)

query_inds = generate_indices_from_edges()

print(len(las1.points[query_inds]))

#plt.scatter(las1.x[query_inds], las1.y[query_inds])
#plt.show()
