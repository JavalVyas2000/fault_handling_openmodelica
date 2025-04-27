# FALCON: Fault-handling Agentic LLMs for Controlled Operations 🚀

## Overview
Welcome to **FALCON**, an exciting exploration of **fault handling and autonomous decision-making** using **OpenModelica** and **Large Language Models (LLMs)**! 🌟

FALCON investigates how LLM agents can interpret **different plant structure representations** (textual descriptions, OpenModelica code, P&IDs, and state graphs) and autonomously suggest fault recovery actions. The project evaluates LLMs' capabilities in understanding and acting upon diverse engineering artifacts, blending **control engineering**, **simulation**, and **AI reasoning**. 🦰🔧

## Features ✨
- **📜 Multi-Representation Input Handling**: Test LLM agents with diverse plant descriptions:
  - Natural language textual descriptions.
  - Raw OpenModelica code.
  - Engineering artifacts like **P&ID diagrams** and **state graphs** (vectorized forms).
- **🔄 Hybrid Simulation**: Combine OpenModelica simulations with Python-based orchestration.


## Getting Started 🚀

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

## Project Structure 🏗️
```
├── code/            # Python scripts for simulation control and analysis
│   ├── main.py
│   ├── mixer_sim.py
│   └── utils.py
├── models/          # Modelica component classes
│   ├── Source.mo
│   ├── Sink.mo
│   ├── Plant.mo
│   └── Mixer.mo
├── crew/            # CrewAI configuration files
├── logs/            # Log files for experiments
├── results/         # Result compilations
├── .gitignore
├── requirements.txt # List of Requirements
└── README.md        # This file
```

## Usage ⚙️

### 1. Run a Simple Simulation
```bash
python code/mixer_sim.py
```
Executes a predefined scenario and logs OpenModelica outputs.

### 2. Invoke Modelica via Python
```bash
python code/mixer_sim.py
```
Loads and simulates the `Mixer.mo` model with fault injections.

### 3. Visualize Results
```bash
python code/visualize.py --input simulation.csv
```
Generates plots of system behavior over time.

### 4. Utilities
Additional helper functions for parsing CSVs and orchestrating simulations are available in `code/utils.py`.

## Data Configuration 📈
- **`ds1_hybrid_s.csv`**: Time-series dataset for hybrid model validation.
- **`sim_setup.json`**: JSON file specifying simulation parameters (e.g., start/end times, step size).

## Model Library 🏭
The `models/` directory contains modular Modelica classes:
- **Source.mo**: Defines input flow or heat source block.
- **Sink.mo**: Represents output or heat sink.
- **Plant.mo**: Encapsulates core process dynamics.
- **Mixer.mo**: Combines multiple streams for mixing tasks.

These components enable building complex and flexible pipelines for fault-handling experiments.

## Results and Images 🖼️
You are encouraged to add your experimental results here! A good place would be:
- **After "Usage" Section**: Showcase simulation screenshots, LLM decisions from different representations (text, P&ID, OpenModelica).
- **Before "Contributing" Section**: Insert a "Gallery" or "Case Studies" section to highlight how the LLM agent handled different plants.

Example layout:

```markdown
## Case Studies 📚
### 1. Text-Based Fault Recovery
*Screenshot/Image + Short description*

### 2. P&ID-Based Fault Recovery
*Screenshot/Image + Short description*

### 3. OpenModelica Code-Based Recovery
*Screenshot/Image + Short description*
```

## Contributing 🤝
We welcome contributions! Please:
- Follow Markdown best practices for documentation.
- Submit clear pull requests based on project structure and coding standards.

## License 📄
*No license specified.* Please contact the author to discuss usage and redistribution permissions.

## Contact 📬
For questions, feedback, or collaboration inquiries, reach out to:

**Javal Vyas**  
Email: j.vyas24@imperial.ac.uk  
LinkedIn: [Javal Vyas](https://www.linkedin.com/in/javal-vyas/)
