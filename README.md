<img src="img/CoCCA.png" align="right" />

# CoCCA
**Computational Chemistry Calculations Assistant**

## Table of contents
  - [Setup](#setup)
  - [Modules](#modules)
    - [Constrain Generator](#constrain-generator)
    - [Neighbor Finder](#neighbor-finder)
  - [Details](#details)
    - [General Structure](#general-structure)

## Setup
- Clone the repository and keep it safe wherever you want!
- Add an alias to your *.bashrc* like:

```
alias cocca="python3 PATH-TO-COCCA/main.py"
```

## Modules

### Constrain Generator
It is used to quickly generate input for Quantum Computational software suite (ORCA, XTB, Gaussian) where one or more atoms are being constrained. This is particularly useful for large molecules.
When asked to select the atom indices, insert one or more atom number separed by a space. Also ranges are allowed (e.g.: 110-125, from atom 110 to 125). The enumeration starts from 1.

### Neighbor Finder
Useful only for .pdb analysis or large molecules inspection. Search what is nearby a selected amino acid or residue in a spherical region. The distance threshold for the search must be in ångström. The charge of the amino acids is calculated at physiologic pH.

## Details

### General Structure
- **coor**: Importing coordinates library
- **utilities**: Collection of general functions that are useful for data analysis and manipualtion.
