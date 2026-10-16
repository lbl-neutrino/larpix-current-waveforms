#!/usr/bin/env bash

if [[ "$LMOD_SYSTEM_NAME" == "perlmutter" ]]; then
    module load python/3.14-26.8.0
fi

source ../.venv/bin/activate

run() {
    input=$1; shift
    tag=$1; shift
    name=$(basename "$input" .hdf5)
    output="data/larnd-sim/$name.$tag.LARND.hdf5"
    log="logs/larnd-sim/$name.$tag.LARND.log"
    mkdir -p "$(dirname "$output")"
    mkdir -p "$(dirname "$log")"
    rm -f "$output"
    python ../larnd-sim/cli/simulate_pixels.py "2x2_ffe_$tag" --rand_seed 1 \
        --input_filename "$input" \
        --output_filename "$output" 2>&1 | tee "$log"
}

tags=(r3 r4)

for input in data/edep-sim/*.hdf5; do
    for tag in "${tags[@]}"; do
        run "$input" "$tag"
    done
done

