#!/usr/bin/env python3

# Units: cm, usec
# Axes: x=drift, y=vertical, z=beam

import h5py
import numpy as np
import numpy.typing as npt

SEGMENTS_DTYPE = np.dtype(
    [
        ("event_id", "u4"),
        ("vertex_id", "u8"),
        ("segment_id", "u4"),
        ("z_end", "f4"),
        ("traj_id", "i4"),
        ("file_traj_id", "u4"),
        ("tran_diff", "f4"),
        ("z_start", "f4"),
        ("x_end", "f4"),
        ("y_end", "f4"),
        ("n_electrons", "u4"),
        ("pdg_id", "i4"),
        ("x_start", "f4"),
        ("y_start", "f4"),
        ("t_start", "f8"),
        ("t0_start", "f8"),
        ("t0_end", "f8"),
        ("t0", "f8"),
        ("dx", "f4"),
        ("long_diff", "f4"),
        ("pixel_plane", "i4"),
        ("t", "f8"),
        ("t_end", "f8"),
        ("dEdx", "f4"),
        ("dE", "f4"),
        ("dE_secondary", "f4"),
        ("y", "f4"),
        ("x", "f4"),
        ("z", "f4"),
        ("n_photons", "f4"),
    ],
    align=True,
)

Vec3 = tuple[float, float, float]

def make_segments(xyz_start: Vec3,
                  xyz_end: Vec3,
                  dEdx: float,
                  max_seg_len: float=0.1):
    start = np.asarray(xyz_start)
    end = np.asarray(xyz_end)

    dxyz = end - start
    tot_len = np.sqrt(np.dot(dxyz, dxyz))
    n_seg = int(np.ceil(tot_len / max_seg_len))
    dx = tot_len / n_seg

    result: npt.NDArray[np.void] = np.zeros(  # 'astype' needed for ty to shut up
        (n_seg,), dtype=SEGMENTS_DTYPE
    ).astype(SEGMENTS_DTYPE)

    ids = np.array(range(n_seg))
    result["segment_id"] = ids

    for i, c in enumerate(["x", "y", "z"]):
        result[f"{c}_start"] = start[i] + ids * dxyz[i] / n_seg
        result[f"{c}_end"] = result[f"{c}_start"] + dxyz[i] / n_seg
        result[f"{c}"] = (result[f"{c}_start"] + result[f"{c}_end"]) / 2

    result["dx"] = dx
    result["dE"] = dEdx * dx
    result["dEdx"] = dEdx

    return result


def write_segments(fname: str, arglist: list[tuple], **kwargs):
    segments = [make_segments(*args, **kwargs) for args in arglist]
    segments = np.concatenate(segments)
    # ensure unique consecutive IDs
    segments["segment_id"] = np.array(range(segments.shape[0]))

    with h5py.File(fname, "w") as f:
        f.create_dataset("segments", data=segments)
