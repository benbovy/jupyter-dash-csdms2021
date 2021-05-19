"""
Some utility functions.
"""

import numpy as np


def get_mesh_elements(dem):
    """Given a DEM as a xarray.DataArray, return triangle indices and vertices
    (as numpy arrays) that can be used to create a ipygany.PolyMesh.

    """
    x = dem.x
    y = dem.y
    nr = len(y)
    nc = len(x)

    triangle_indices = np.empty((nr - 1, nc - 1, 2, 3), dtype='uint32')

    r = np.arange(nr * nc).reshape(nr, nc)

    triangle_indices[:, :, 0, 0] = r[:-1, :-1]
    triangle_indices[:, :, 1, 0] = r[:-1, 1:]
    triangle_indices[:, :, 0, 1] = r[:-1, 1:]

    triangle_indices[:, :, 1, 1] = r[1:, 1:]
    triangle_indices[:, :, :, 2] = r[1:, :-1, None]

    triangle_indices.shape = (-1, 3)

    xx, yy = np.meshgrid(x, y, sparse=True)

    vertices = np.empty((nr, nc, 3))
    vertices[:, :, 0] = xx
    vertices[:, :, 1] = yy
    vertices[:, :, 2] = dem.values

    vertices = vertices.reshape(nr * nc, 3)

    return triangle_indices, vertices