#!/usr/bin/env python3

import os

os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"

from pathlib import Path

import numpy as np

from edep_gen import write_segments


def A(*a, **kw) -> np.ndarray:
    return np.array(a, **kw)


OUTDIR = "data/edep-sim"

MOD_CENTER = A(0, 0, 0)  # fsd.yaml
TILE_X = 47.1055  # multi_tile_layout-3.0.40_fsd_v3.yaml
PITCH = 0.372  # multi_tile_layout-3.0.40_fsd_v3.yaml

DENSITY_LAR = 1.40
DEDX_LOW = 2 * DENSITY_LAR
DEDX_HIGH = 6 * DENSITY_LAR


def gen_parallel(tag: str, dEdx: float):
    mid = MOD_CENTER + A(TILE_X - 3, PITCH / 2, 0)
    start = mid - A(0, 0, 3 * PITCH)
    end = mid + A(0, 0, 3 * PITCH)
    write_segments(f"{OUTDIR}/parallel_{tag}.hdf5",
                   [(start, end)],
                   dEdx=dEdx)


def gen_parallel_mip():
    gen_parallel('mip', DEDX_LOW)

def gen_parallel_hip():
    gen_parallel('hip', DEDX_HIGH)

def gen_inclined_mip():
    pass


def gen_double_parallel_mip(sep_mm: float):
    pass


def gen_clipping_mip():
    pass




def main():
    Path(OUTDIR).mkdir(parents=True, exist_ok=True)

    gen_parallel_mip()


if __name__ == "__main__":
    main()
