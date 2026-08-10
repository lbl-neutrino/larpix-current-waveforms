#!/usr/bin/env python3

from pathlib import Path

import numpy as np

INDIR = "data/larnd-sim"
OUTDIR = "waveforms"


def dump_waveform(
    name: str, f: np.lib.npyio.NpzFile, pixel_id: int = 102528, sigtype="near"
):
    assert sigtype in ["near", "far"]
    signals = f["signals_near"] if sigtype == "near" else f["signals_ff_plus"]
    pixels = f["pixels_near"]
    if sigtype == "ff_plus":
        assert np.all(f["mask_ff_plus"]) and (
            f["mask_ff_plus"].shape == f["pixels_near"].shape
        )
    i = np.nonzero(pixels == pixel_id)[0][0]
    wvfm = signals[i, :]
    # end_tick is the index of the first padding value
    end_tick = max(np.nonzero(~np.isclose(wvfm, 0))[0]) + 1
    end_tick = min(end_tick, wvfm.shape[0] - 1)
    wvfm = wvfm[: end_tick + 1]
    if end_tick != wvfm.shape[0] - 1:
        assert wvfm[-1] == 0
    np.savetxt(f"{OUTDIR}/{name}.txt", wvfm, fmt="%.6f")


def main():
    Path(OUTDIR).mkdir(parents=True, exist_ok=True)

    for h5f in Path(INDIR).glob("*.LARND.hdf5"):
        f = np.load(f"{h5f}_signals/nf_signals.00.1.npz")
        for sigtype in ['near', 'far']:
            name = Path(h5f.stem).stem + '_' + sigtype
            dump_waveform(name, f, sigtype=sigtype)
            print(f"Dumped {name}")


if __name__ == "__main__":
    main()
