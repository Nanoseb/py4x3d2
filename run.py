import numpy as np
import adios2

import src.convert_stl as convert_stl
import src.embed_stl as embed_stl

def run(stl_file):

    # Convert STL to voxel array
    voxels = convert_stl.convert(stl_file)

    print(f"Model dimensions: {voxels.L}")
    print(f"Model scale: {voxels.scale}")
    print(f"Voxel size: {1 / voxels.scale}")
    print(f"Voxel count: {voxels.n}")
    print(f"Bounding box: {voxels.bounding_box()}")
    
    # Embed voxels into an IBM field
    # mesh_n = [350, 950, 215]
    mesh_n = [697, 1878, 429]
    # mesh_l = [39.6, 92.4, 236]
    # mesh_l = [72, 160, 32]
    # mesh_l = [60, 162, 37]
    mesh_l = [60.11421911, 161.97202797,  37. ]
    shift = [0, 0, 0]
    ibm = embed_stl.embed(voxels, mesh_n, mesh_l, shift)

    shift = [-13.244, 29.2215, 0]
    ibm2 = embed_stl.embed(voxels, mesh_n, mesh_l, shift)

    ibm = ibm2 * ibm
    
    # Write voxel array using ADIOS2
    nx = ibm.shape[0]
    ny = ibm.shape[1]
    nz = ibm.shape[2]

    shape = [nx, ny, nz]
    start = [0, 0, 0]
    count = [nx, ny, nz]

    with adios2.Stream("ibm.bp", "w") as fh:
        fh.write("iibm", 1)
        for _ in range(0, 1):
            fh.write("ep1", ibm, shape, start, count)


if __name__ == "__main__":
    #run("/Users/paulbartholomew/DATA/mesh/stl/test_single_foil.stl")
    run("front_foil.stl")
