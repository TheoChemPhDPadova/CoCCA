<img src="img/CoCCA.png" align="right" />

# CoCCA
**Co**mputational **C**hemistry **C**alculations **A**ssistant

## Table of contents
  - [Setup](#setup)
  - [Modules](#modules)
    - [Trajectory Manipulation](#trajectory-manipulation)
      - [Resizer](#resizer)
      - [Analyzer/Freezer](#analyzer/freezer)
      - [Slicer](#slicer)
      - [TRJ 2 QST2/QST3](#TRJ-2-QST2/QST3)
    - [PDB Tools](#pdb-tools)
      - [Neighbor Finder](#neighbor-finder)
      - [Catalytic Pocket Selector](#neighbor-finder)
    - [Others](#others)
      - [Constrain Generator](#constrain-generator)
  - [Quick Mode](#quick-mode)
      - [General Output from QM-Suite](#General-Output-from-QM-Suite-(ADF,-ORCA,-Gaussian))
      - [NEB Visualizer](#NEB-Visualizer)

## Setup
- Clone the repository and keep it safe wherever you want!
- Add an alias to your *.bashrc* like:

```
alias cocca="python3 PATH-TO-COCCA/main.py"
```

## Modules
### Trajectory Manipulation
---
#### **Resizer**
This tool allows you to extend or reduce a trajectory by increasing or decreasing the number of images in it using a linear interpolation approach.

#### **Analyzer/Freezer**
Trajectory analysis detects the displacement magnitude of every atom: this provides an easy way to understand which atoms are frozen along the trajectory (backbone) and which ones are the key fragments for the considered reaction. This tool also allows you to constrain specific atoms and create a new trajectory useful for a constrained NEB analysis.

#### **Slicer**
This tool helps you to cut a trajectory formed by several structures into a smaller number of images/snapshots.

#### **TRJ 2 QST2/QST3**
Useful tool to select two structures (from a trajectory) just before and after the transition state: an input file for a Synchronous Transit-Guided Quasi-Newton calculation (QST2) for Gaussian will be created. If a guess of the transition state is also selected, the calculation automatically turns into a QST3.
### PDB Tools
---
#### **Neighbor Finder**
Useful only for .pdb analysis or large molecules inspection. Search what is nearby a selected amino acid or residue in a spherical region. The distance threshold for the search must be in ångström. The charge of the amino acids is calculated at physiologic pH.

#### **Catalytic Pocket Selector**
TBD

### Others
---
#### **Constrain Generator**
It is used to quickly generate input for Quantum Computational software suite (ORCA, XTB, Gaussian) where one or more atoms are being constrained. This is particularly useful for large molecules.
When asked to select the atom indices, insert one or more atom number separed by a space. Also ranges are allowed (e.g.: 110-125, from atom 110 to 125). The enumeration starts from 1.

## Quick Mode

### General Output from QM-Suite (ADF, ORCA, Gaussian)

### NEB Visualizer (ORCA)
