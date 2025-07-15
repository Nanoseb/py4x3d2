""" src/embed_voxels.py

Module to embed voxels representing a geometry as an IBM field array.
"""

import numpy as np

def embed(voxels, mesh_n, mesh_l, shift=[0, 0, 0]):
    """Embeds the voxel data as an IBM within a mesh."""

    nx = mesh_n[0]
    ny = mesh_n[1]
    nz = mesh_n[2]

    dx = mesh_l[0] / (nx - 1)
    dy = mesh_l[1] / (ny - 1)
    dz = mesh_l[2] / (nz - 1)

    ibm = np.zeros([nz, ny, nx])
    nxyz = np.prod(mesh_n)
    ctr = 0
    workfrac = 0
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                x = i * dx - shift[0]
                y = j * dy - shift[1]
                z = k * dz - shift[2]

                if voxels.query([x, y, z]) > 0:
                    ibm[k,j,i] = 0.0
                else:
                    ibm[k,j,i] = 1.0

                if ctr > (workfrac / 100.0) * nxyz:
                    print(f"{workfrac}%")
                    workfrac += 10
                ctr += 1

    return ibm
