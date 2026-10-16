#!/usr/bin/env python3

import os

os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"

from pathlib import Path

import numpy as np

from edep_gen import write_segments


def A(*a, **kw) -> np.ndarray:
    return np.array(a, **kw)


OUTDIR = "data/edep-sim"

TILE_CENTER = A(33.5, 0, 33.5) + A(30.58975) # 2x2.yaml + multi_tile_layout-2.4.16_v4.yaml
PITCH = 0.4434  # multi_tile_layout-2.4.16_v4.yaml

DENSITY_LAR = 1.40
DEDX_LOW = 2 * DENSITY_LAR
DEDX_HIGH = 6 * DENSITY_LAR


def gen_blip():
    mid = TILE_CENTER + A(-10, PITCH / 2, 4 * PITCH)
    delta = A(0.025, 0, 0)
    start, end = mid - delta, mid + delta
    write_segments(
        f"{OUTDIR}/blip_x10cm_z4p_l0.05_dEdx20.hdf5", [(start, end)], dEdx=20
    )


def gen_blip_nudged():
    mid = TILE_CENTER + A(-10, PITCH / 2, 4.25 * PITCH)
    delta = A(0.025, 0, 0)
    start, end = mid - delta, mid + delta
    write_segments(
        f"{OUTDIR}/blip_x10cm_z4.25p_l0.05_dEdx20.hdf5", [(start, end)], dEdx=20
    )

def gen_blip_nudged2():
    mid = TILE_CENTER + A(-10, PITCH / 2, 3.75 * PITCH)
    delta = A(0.025, 0, 0)
    start, end = mid - delta, mid + delta
    write_segments(
        f"{OUTDIR}/blip_x10cm_z3.75p_l0.05_dEdx20.hdf5", [(start, end)], dEdx=20
    )

def gen_blip_center():
    mid = TILE_CENTER
    delta = A(0.025, 0, 0)
    start, end = mid - delta, mid + delta
    write_segments(
        f"{OUTDIR}/blip_center.hdf5", [(start, end)], dEdx=20
    )


def main():
    Path(OUTDIR).mkdir(parents=True, exist_ok=True)

    gen_blip()
    gen_blip_nudged()
    gen_blip_nudged2()
    gen_blip_center()


if __name__ == "__main__":
    main()
