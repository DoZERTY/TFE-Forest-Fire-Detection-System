# ForestFireDetection
This repository contains the work and source files associated with the Master's thesis of Dorian Schrobiltgen. The project builds upon the previous work conducted in [ForestMEv2-public](https://forge.uclouvain.be/nbrusselmans/forestmev2-public).

## Objective

The aim of this thesis is to design and evaluate a low-power, wireless sensor node capable of detecting the early signs of forest fires. The system combines gas sensing, RF communication and optimized embedded hardware/software to ensure early and reliable detection in forest environments, while minimizing the environmental impact of each end-node.

## Project Structure
The repository is devided into four main parts:
### Hardware
- **new_prototype/**: Contains PCB designs, schematics, and Bill of Material (BoM) for the new hardware prototype.
- **test_antenna/**: Designs and schematics related to PCBs used for antenna impedance testing.

### Measurements
- **Gas_sensor/**: Includes raw data, analysis script and plots related to $CO_2$ concentration profile testing.

- **Power_consumption/**: Detailed power consumption for the initial and new prototype.

- **RF_network/**: Results from RF performance tests performed using the antenna impedance testing PCBs

### Simulations
- **Analysis/**: A collection of Python scripts for power consumption modeling, supercapacitor sizing, and generation of plots used in the thesis report.
- **FWI/**: Contains the optimized C implementation of the Fire Weather Index (FWI), along with a repository (by Reid Sawtell in [pyFWI](https://github.com/buckinha/pyfwi)) used for validation.
- **LCA/**: Life Cycle Assessment files used to quantify the environmental impact of each end-node.

### Software
This directory contains the full STM32 projects used to program the boards. Each folder includes all necessary files to build, flash, and debug the corresponding prototype using **STM32CubeIDE**.
- **initial_prototype/**: Complete project and source code of the optimized software for the initial hardware prototype.
- **new_prototype/**: Complete project and source code of the optimized software for the new hardware prototype.
