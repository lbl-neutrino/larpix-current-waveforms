#!/usr/bin/env bash

if [[ "$LMOD_SYSTEM_NAME" == "perlmutter" ]]; then
    module load python/3.13
fi

source .venv/bin/activate

run() {
    input=$1; shift
    tag=$1; shift
    name=$(basename "$input" .hdf5)
    output="data/larnd-sim/$name.$tag.LARND.hdf5"
    log="logs/larnd-sim/$name.$tag.LARND.log"
    mkdir -p "$(dirname "$output")"
    mkdir -p "$(dirname "$log")"
    rm -f "$output"
    python larnd-sim/cli/simulate_pixels.py "fsd_cube_prc0_$tag" --rand_seed 1 \
        --input_filename "$input" \
        --output_filename "$output" 2>&1 | tee "$log"
}

tags=(r3_plane r3_box r4_plane r4_box)

for input in data/edep-sim/*.hdf5; do
    for tag in "${tags[@]}"; do
        run "$input" "$tag"
    done
done

