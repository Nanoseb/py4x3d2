from mpi4py import MPI
import numpy as np
import adios2

import src.convert_stl as convert_stl
import src.embed_stl as embed_stl

def run(stl_file):

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
        
    # Convert STL to voxel array
    voxels = convert_stl.convert(stl_file)

    print(f"Model dimensions: {voxels.L}")
    print(f"Model scale: {voxels.scale}")
    print(f"Voxel size: {1 / voxels.scale}")
    print(f"Voxel count: {voxels.n}")
    print(f"Bounding box: {voxels.shift} : {voxels.shift + voxels.L}")
    
    # Embed voxels into an IBM field
    mesh_n = [50, 100, 200]
    # mesh_l = [39.6, 92.4, 236]
    mesh_l = [40, 80, 160]
    shift = [0, 10, 0]
    ibm = embed_stl.embed(voxels, mesh_n, mesh_l, shift)

    # Write voxel array using ADIOS2
    nx = ibm.shape[0]
    ny = ibm.shape[1]
    nz = ibm.shape[2]

    shape = [nx, ny, nz]
    start = [0, 0, 0]
    count = [nx, ny, nz]

    with adios2.open("test.bp", "w", comm) as fh:
        for _ in range(0, 1):
            fh.write("vol", ibm, shape, start, count)


if __name__ == "__main__":
    run("/Users/paulbartholomew/DATA/mesh/stl/test_single_foil.stl")
