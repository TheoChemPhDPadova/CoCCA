<img src="img/CoCCA.png" align="right" width="150" height="166"/>

# CoCCA
**Co**mputational **C**hemistry **C**alculations **A**ssistant

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub issues](https://img.shields.io/github/issues/TheoChemPhDPadova/CoCCA)](https://img.shields.io/github/issues/TheoChemPhDPadova/CoCCA)
[![GitHub version](https://img.shields.io/github/v/tag/TheoChemPhDPadova/CoCCA)](https://img.shields.io/github/v/tag/TheoChemPhDPadova/CoCCA)

## Table of contents
  - [Setup](#setup)
  - [Modules](#modules)
    - [Trajectory Manipulation](#trajectory-manipulation)
      - [Resizer](#resizer)
      - [Analyzer/Freezer](#analyzer/freezer)
      - [Slicer](#slicer)
      - [TRJ 2 Synchronous Transit-Guided Quasi-Newton](#TRJ-2-QST2/QST3)
    - [PDB Tools](#pdb-tools)
      - [Proximity Analysis](#proximity-analysis)
      - [Catalytic Pocket Selector](#catalytic-pocket-selector)
    - [Molecular properties and vibrations](#molecular-properties-and-vibrations)
    - [Others](#others)
      - [Constrain Generator](#constrain-generator)
  - [Quick Mode](#quick-mode)

## Setup
- Clone the repository and keep it safe wherever you want!
- Download the required repositories with
```
pip install -r requirements.txt --user
```
- Add an alias to your *.bashrc* like (optional):
```
alias cocca="python3 PATH-TO-COCCA/main.py"
```

## Modules
### Trajectory Manipulation
---
#### **Resizer**
This tool allows you to extend or reduce a trajectory by increasing or decreasing the number of images in it using a linear interpolation approach.

#### **Analyzer/Freezer**
Trajectory analysis detects the displacement magnitude of every atom : this provides an easy way to understand which atoms are frozen along the trajectory (e.g. backbone atoms) and which ones are the key fragments for the considered reaction. This tool also allows you to constrain specific atoms and create a new trajectory useful for a constrained NEB analysis.

#### **Slicer**
This tool helps you to cut a trajectory formed by several structures into a smaller one with a limited number of images/snapshots.

#### **TRJ 2 QST2/QST3**
Useful tool to select two structures (from a trajectory) just before and after the transition state: an input file for a Synchronous Transit-Guided Quasi-Newton calculation (QST2) for Gaussian will be created. If a guess of the transition state is also selected, the calculation automatically turns into a QST3.
### PDB Tools
---
#### **Proximity Analysis**
Useful for .pdb analysis or large molecules inspection. Search what is nearby a selected amino acid, residue or atom in a spherical region. The distance threshold for the search is in ångström. The charge of the amino acids is calculated at physiologic pH.

#### **Catalytic Pocket Selector**
Used to select a portion of a protein (from a .pdb file) for further analysis. The selection is made by choosing the residues. This utility is particularly useful when you want to extract the catalytic pocket or parts of particular interest from a protein that will be analyzed later with high accuracy quantum mechanic methods (e.g. DFT). The two endings of all the selected chains of residues can be capped with ACE/NME residues or with a atom marker.

### Molecular properties and vibrations
---
This module contains several utilities to calculate molecular properties (% composition, center of mass, moment of inertia tensor), plot IR spectra (with gaussian/lorentzian broadening) and generate linear interpolated structures between two given limit geometries.

### Others
---
#### **Constrain Generator**
It is used to quickly generate input for Quantum Computational software suite (ORCA, XTB, Gaussian) where one or more atoms are being constrained. This is particularly useful for large molecules.
When asked to select the atom indices, insert one or more atom number separed by a space. Also ranges are allowed (e.g.: 110-125, from atom 110 to 125). The enumeration starts from 1.

## Quick Mode
The quick mode simply works by calling the main script (main.py) with the name of the file that should be loaded as the argument.
```
python3 main.py <filename.out/.interp/.xyz>
```

### Supported files:
| EXTENSION | Description |
| ----------- | ----------- |
| .OUT | AMS/ADF, ORCA, Gaussian output files |
| .INTERP | ORCA interpolation file from a NEB analysis |
| .XYZ | Cartesian XYZ: requires an additional **load** directive ```python3 main.py load <filename.xyz> <filename2.xyz> ...``` used to load multiple XYZ structures |
