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


def gen_blip():
    mid = MOD_CENTER + A(TILE_X - 10, PITCH / 2, 4 * PITCH)
    delta = A(0.025, 0, 0)
    start, end = mid - delta, mid + delta
    write_segments(
        f"{OUTDIR}/blip_x10cm_z4p_l0.05_dEdx20.hdf5", [(start, end)], dEdx=20
    )


def main():
    Path(OUTDIR).mkdir(parents=True, exist_ok=True)

    gen_blip()


if __name__ == "__main__":
    main()
