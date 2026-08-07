#!/usr/bin/env python3

from pathlib import Path

import numpy as np

INDIR = "data/larnd-sim"
OUTDIR = "waveforms"

# Copied from /pscratch/sd/m/mkramer/test/larnd-sim.segFFE3/output/skim_more/prc16_r4_cutFix_saveSignals/showers.prc16_r4_cutFix_saveSignals.01.LARND.hdf5_signals/signals.14.npz
SHOWER_FILE = (
    "/global/cfs/cdirs/dune/www/data/2x2/people/mkramer/shower_signals_fsdcube.npz"
)


def dump_waveform(name: str, f: np.lib.npyio.NpzFile, pixel_id: int = 102527):
    signals, pixels = f["signals_near"], f["pixels_near"]
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
        name = Path(h5f.stem).stem
        f = np.load(f"{h5f}_signals/nf_signals.00.1.npz")
        dump_waveform(name, f)
        print(f"Dumped {name}")

    if not Path(SHOWER_FILE).exists():
        print(f"Skipping shower: Could not find {SHOWER_FILE}")
    else:
        f = np.load(SHOWER_FILE)
        dump_waveform("shower", f, pixel_id=1145)
        print("Dumped shower")


if __name__ == "__main__":
    main()
