#!/usr/bin/env bash

if [[ "$LMOD_SYSTEM_NAME" == "perlmutter" ]]; then
    module load python/3.13
fi

source .venv/bin/activate

mkdir -p data/larnd-sim

run() {
    input=$1; shift
    name=$(basename "$input" .hdf5)
    output="data/larnd-sim/$name.LARND.hdf5"
    rm -f "$output"
    python larnd-sim/cli/simulate_pixels.py fsd --rand_seed 1 \
        --input_filename "$input" \
        --output_filename "$output"
}

for input in data/edep-sim/*.hdf5; do
    run "$input"
done

