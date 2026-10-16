#!/usr/bin/env python3

from pathlib import Path
from traceback import print_exc

import numpy as np

INDIR = "data/larnd-sim"
OUTDIR = "waveforms"

# 2x2 module 0/1/3
NPIX_X = 7 * 10 * 2
NPIX_Y = 7 * 10 * 4
NPIX_TOT = NPIX_X * NPIX_Y

# Pixel directly northeast of tile center
PIXEL_ID = int((NPIX_TOT / 2) - (NPIX_X / 2))

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

def color(code, text):
    return f"{code}{text}{RESET}"

def dump_waveform(
    name: str, f: np.lib.npyio.NpzFile, pixel_id: int = PIXEL_ID, sigtype="near"
):
    assert sigtype in ["near", "far", 'farOnly']
    if sigtype == 'near':
        signals, pixels = f["signals_near"], f["pixels_near"]
    elif sigtype == 'far':
        signals, pixels = f["signals_ff_plus"], f["pixels_near"]
    elif sigtype == 'farOnly':
        signals, pixels = f["signals_ff_only"], f["pixels_ff_only"]

    if sigtype == "far":
        assert np.all(f["mask_ff_plus"]) and (
            f["mask_ff_plus"].shape == f["pixels_near"].shape
        )

    i = np.nonzero(pixels == pixel_id)[0][0]
    wvfm = signals[i, :]
    # end_tick is the index of the first padding value
    try:
        end_tick = max(np.nonzero(~np.isclose(wvfm, 0))[0]) + 1
    except:
        end_tick = wvfm.shape[0] - 1
    end_tick = min(end_tick, wvfm.shape[0] - 1)
    wvfm = wvfm[: end_tick + 1]
    if end_tick != wvfm.shape[0] - 1:
        assert wvfm[-1] == 0
    np.savetxt(f"{OUTDIR}/{name}.pix{pixel_id}.txt", wvfm, fmt="%.6f")


def main():
    Path(OUTDIR).mkdir(parents=True, exist_ok=True)

    for h5f in sorted(Path(INDIR).glob("*.LARND.hdf5")):
        if Path(f"{h5f}_signals/signals.00.1.npz").exists():
            f = np.load(f"{h5f}_signals/signals.00.1.npz")
            sigtypes = ['near', 'far', 'farOnly']
        else:
            f = np.load(f"{h5f}_signals/nf_signals.00.1.npz")
            sigtypes = ['near', 'far']
        for sigtype in sigtypes:
            name = Path(h5f.stem).stem + '_' + sigtype
            try:
                dump_waveform(name, f, sigtype=sigtype)
                print(color(GREEN, f"Dumped {name}"))
            except:
                print(color(RED, f"Failed on {name}"))
                print_exc()


if __name__ == "__main__":
    main()
