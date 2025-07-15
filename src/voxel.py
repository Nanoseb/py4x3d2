""" src/voxel.py

Class definition of voxels.
"""

import numpy as np

class Voxels:
    def __init__(self, vol, scale, shift):
        self.vol = vol
        self.scale = scale
        self.shift = shift

        self.n = vol.shape
        self.L = self.n / self.scale
        
    def _xyz(self, xyz):
        """Get the relative spatial coordinate.

        Note this assumes that the coordinate ordering matches the stl-to-voxel layout [z,y,x].
        """
        
        return xyz - self.shift

    def _ijk(self, xyz):
        """Converts a spatial [x,y,z] coordinate into voxel indices."""

        xyz_rel = self._xyz(np.flip(xyz)) # Flip coordinates as stl-to-voxel stores [z,y,x] data

        # XXX: np.floor(x) rounds DOWN, not towards zero - this is the behaviour that we want as it
        #      prevents points that are -ve in relative space from being rounded into the object.
        ijk = np.floor(xyz_rel * self.scale).astype(int)

        return ijk
        
    def query(self, xyz):
        """Obtains the voxel value at coordinates [xyz]."""

        def fix_boundary_intersection(xyz, ijk):
            xyz_rel = self._xyz(np.flip(xyz)) # Flip coordinates as stl-to-voxel stores [z,y,x] data
            if np.any(xyz_rel == self.L):
                for i in range(3):
                    if (xyz_rel[i] == self.L[i]):
                        ijk[i] -= 1
                return self.vol[ijk[0], ijk[1], ijk[2]]
            else:
                return 0

        ijk = self._ijk(xyz)
        if np.any(ijk < 0) or np.any(ijk > self.n):
            return 0
        elif np.any(ijk == self.n):
            return fix_boundary_intersection(xyz, ijk)
        else:
            return self.vol[ijk[0], ijk[1], ijk[2]]

        
