This repository contains a handful of simulated LArPix analog signals, as predicted by larnd-sim. The simulation, unless otherwise noted, is based on that of the Full Scale Demonstrator, whose v2d tiles have the same pixel pitch as v3. The full nominal HV is assumed, corresponding to a drift velocity of 1.6 mm/usec.

The following scenarios are covered:

- MIP track parallel to anode and 3cm away (i.e. short current pulse on pixel). Horizontal and slicing through the pixel's center.
- MIP track highly-inclined (85 degrees) to anode, 3-6cm away (i.e. long current pulse on pixel). Horizontal and symmetric about the pixel's center.
- Two anode-parallel MIP tracks on same pixel, closely spaced in time, with separation of 2, 5, and 10 usec (closer track 3cm from anode; horizontal and slicing through the pixel's center)
- MIP track clipping pixel (i.e. small pulse close to ~5000 ke- design self-trigger threshold): Parallel to anode, 45-degrees rotated in the "pixel" plane, 3cm away, shifted upward by 3/4 of a pitch.
- HIP track on pixel (i.e. pulse with higher peak current on pixel). Same geometry as first case (parallel MIP track).
- Shower on pixel (i.e. long pulse with lots of structure)

Waveform files, in text format, can be found in the `waveforms` folder. Each line corresponds to one LArPix clock tick (100 ns); the value on each line is the current on the pixel, in units of e-/usec. See `plots.ipynb` for the signal traces.

The "shower" waveform was taken from a separate study on simulated showers in the FSD Cube geometry at half-nominal HV. The others were generated as described below.

First, an edep-sim file was mocked up for each scenario. See `make_inputs.ipynb`.

Then, larnd-sim was run on each edep-sim file. The `FIXME` tag of larnd-sim was used; this tag contains modifications to make it dump the analog signals seen by the pixels. See `run_all_larnd_sim.sh`.

Finally, the signals were extracted and dumped to text. See `extract_signals.ipynb`. The pixel in question is the one immediately above the midpoint of the anode plane.
