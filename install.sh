#!/usr/bin/env bash

if [[ "$LMOD_SYSTEM_NAME" == "perlmutter" ]]; then
    module load python/3.13
fi

python -m venv .venv
source .venv/bin/activate

# If we don't have CUDA, just install cupy-cuda12x so that larnd-sim's setup.py
# doesn't try to build cupy from soure.
if [[ -z "$CUDA_HOME" ]]; then
    pip install cupy-cuda12x
    export SKIP_CUPY_INSTALL=1
fi

git clone --depth 1 -b save-wvfm-202608 https://github.com/DUNE/larnd-sim
cd larnd-sim || (echo "Could not clone repo"; exit)
pip install -e .

# For plotting the traces
pip install jupyter matplotlib
