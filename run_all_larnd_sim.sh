#!/usr/bin/env bash

# Run me from inside a clone of the larnd-sim repo, in a virtual env in which
# larnd-sim has been installed, on a machine with a GPU.

run() {
    name=$1; shift
    rm -f "output/chg_inject/$name.LARND.hdf5"
    python cli/simulate_pixels.py fsd --rand_seed 1 \
        --input_filename "input/chg_inject/$name.hdf5" \
        --output_filename "output/chg_inject/$name.LARND.hdf5"
}

run parallel_mip
