# Fault Handling with OpenModelica

## Overview
This repository provides an **agentic framework for fault handling** using OpenModelica models and Python scripts to orchestrate simulations, inject anomalies, and analyze system responses.

## Features
- **Agentic Fault Injection**: Automate introduction of anomalies into Modelica models (e.g., component malfunctions).
- **Hybrid Simulation**: Combine OpenModelica simulations with Python-based data processing and visualization.
- **Data-Driven Analysis**: Predefined datasets and configuration files for reproducible experiments.
- **Modular Model Library**: Separate Modelica components (Source, Sink, Plant, Mixer) to build varied system topologies.

## Getting Started

### Prerequisites
- **OpenModelica** v1.13 or later ([Installation Guide](https://openmodelica.org/)).
- **Python 3.8+** ([Python Official Site](https://www.python.org/)).

### Installation
```bash
# Clone the repository
git clone https://github.com/JavalVyas2000/fault_handling_openmodelica.git
cd fault_handling_openmodelica

# (Optional) create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install Python dependencies
pip install -r requirements.txt
```

> **Note:** If `requirements.txt` is not provided, install necessary packages manually, e.g., `pandas`, `numpy`, `matplotlib`.

## Project Structure
```
├── code/            # Python scripts for simulation control and analysis
│   ├── mixer_sim.py
│   ├── trial.py
│   ├── utils.py
│   └── visualize.py
├── data/
│   └── ds1/         # Sample datasets and simulation configurations
│       ├── ds1_hybrid_s.csv
│       └── sim_setup.json
├── models/          # Modelica component classes
│   ├── Source.mo
│   ├── Sink.mo
│   ├── Plant.mo
│   └── Mixer.mo
├── crew/            # Configuration files for CrewAI orchestration
├── .gitignore
└── README.md        # This file
```

## Usage

### Run a Simple Simulation
```bash
python code/trial.py
```
Executes a predefined scenario and logs OpenModelica outputs.

### Invoke Modelica via Python
```bash
python code/mixer_sim.py
```
Uses `mixer_call.mos` to load and simulate the `Mixer.mo` model with fault injections.

### Visualize Results
```bash
python code/visualize.py --input simulation.csv
```
Generates plots of system behavior over time.

### Utilities
Additional helper functions for parsing CSVs and orchestrating simulations are available in `code/utils.py`.

## Data Configuration
- **`ds1_hybrid_s.csv`**: Time-series dataset for hybrid model validation.
- **`sim_setup.json`**: JSON file specifying simulation parameters (e.g., start/end times, step size).

## Model Library
The `models/` directory contains modular Modelica classes:
- **Source.mo**: Defines input flow or heat source block.
- **Sink.mo**: Represents output or heat sink.
- **Plant.mo**: Encapsulates core process dynamics.
- **Mixer.mo**: Combines multiple streams for mixing tasks.

These components enable building complex pipelines for fault-handling experiments.

## Contributing
We welcome contributions! Please:
- Follow Markdown best practices for documentation.
- Submit clear pull requests based on project structure and coding standards.

## License
*No license specified.* Please contact the author to discuss usage and redistribution permissions.

## Contact
For questions, feedback, or collaboration inquiries, reach out to:

**Javal Vyas**  
Email: j.vyas24@imperial.ac.uk  
LinkedIn: [Javal Vyas](https://www.linkedin.com/in/javal-vyas/)
