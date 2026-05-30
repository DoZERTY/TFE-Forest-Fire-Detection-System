# pyFWI Integration

This directory contains a modified version of the **pyFWI** library, originally developed by **Reid Sawtell**.

The code was integrated into this thesis project for the purpose of running and analyzing fire weather index (FWI) computations in C for performance comparison between the complete implementation and an optimized one.

## Original License

The original code is distributed under the **BSD 3-Clause License**.  
The license allows redistribution and use in source and binary forms, with or without modification, under the following conditions:

- The original copyright
  (c) 2010, Reid Sawtell, must be retained.
- Redistributions must include the full license text.
- The name of the original author may not be used to endorse derived products without prior written permission.

For full license details, see the [`LICENSE`](./pyFWI-1.0/LICENSE.txt) file included in this directory.

## Modifications

The following changes were made:
- Addition of `FWI.h` and `FWI.c` files implementing in c the optimized FWI.
- Addition of a Python wrapper (`TestC.py`) to test this optimized implementation and compare the result with the complete implementation.
- Python 3 plotting script added (`plot.py`) to plot the distribution of the error and the error versus expected FWI.
- Shell instructions for compiling and running test scenarios.

## Usage

To compile, run the tests and generate plots:
```bash
cd FWI/
./test.bash