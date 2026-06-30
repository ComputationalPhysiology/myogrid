# MyoGrid

A multiscale mathematical modeling framework for simulating sarcomere arrays in cardiomyocytes. 

MyoGrid bridges the gap between biological structure and macroscopic force production. It allows researchers to model 2D arrays of connected sarcomeres (myofibrils in parallel, sarcomeres in series) using either dynamic Ordinary Differential Equations (ODEs) or steady-state algebraic solvers. 

A core feature of MyoGrid is the ability to simulate **heterogeneous populations** (e.g., mixing Wild-Type and Mutant sarcomeres within the same tissue grid) to analyze how localized structural deficits—such as reduced thick filament length or altered passive stiffness—affect global contractile performance.

---

## 🏗️ Repository Structure

* **`src/myogrid/`**: The core Python package containing the physics engines and modeling classes.
* **`demos/`**: Standalone scripts demonstrating how to initialize arrays, run simulations, and generate plots.
* **`pyproject.toml`**: The build configuration file for installing the package.

---

## ⚙️ Installation

To run the simulations and demos, you need to install `myogrid` as a local Python package. We recommend using an editable install so that any changes you make to the source code are instantly reflected without needing to reinstall.

1. Open your terminal and navigate to the root directory of this repository (where `pyproject.toml` is located).
2. Run the following command:
   ```bash
   pip install -e .
