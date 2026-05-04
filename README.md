# NS-3 TCP Protocol Comparison Study
## Comparing TCP Reno vs TCP NewReno vs TCP Cubic

### 📊 Project Overview
This project simulates and compares three TCP congestion control algorithms using **NS-3 Network Simulator**:
- **TCP Reno** (standard TCP)
- **TCP NewReno** (improved recovery)
- **TCP Cubic** (modern algorithm)

### 🎯 Learning Objectives
1. Understand network simulation using NS-3
2. Compare TCP congestion control mechanisms
3. Analyze performance metrics through graphs
4. Write technical report with findings

### 📁 Project Structure
```
NS3-TCP-Comparison/
├── ns3-scripts/           # NS-3 simulation code (C++)
│   └── tcp_comparison.cc  # Main simulation script
├── python-analysis/       # Data visualization & analysis
│   ├── parse_pcap.py      # Parse NS-3 output files
│   ├── metrics.py         # Calculate metrics
│   └── plot_graphs.py     # Generate graphs
├── data/                  # Simulation output data
├── results/               # Generated graphs & plots
├── docs/                  # Documentation
│   ├── UBUNTU_SETUP.md    # Ubuntu/Linux setup guide
│   ├── SIMULATION_GUIDE.md # How to run simulation
│   └── REPORT_TEMPLATE.md # Report structure
└── README.md              # This file
```

### 📈 Performance Metrics
The simulation will measure:
- **Throughput** (Mbps) - Data sent successfully per second
- **Packet Delivery Ratio (PDR)** (%) - Successful packets / Total packets
- **End-to-End Delay** (ms) - Time from sender to receiver
- **Packet Loss** (%) - Failed packets / Total packets
- **RTT (Round-Trip Time)** (ms) - Network response time

### 🌐 Network Topology
```
Sender → Router1 ←→ Router2 → Receiver
                      (congested link)

Nodes: 10-20
Links: Point-to-Point with bandwidth constraints
Traffic: TCP flows sending large files
```

### 🔧 Tools & Requirements

**Windows (Today):**
- Python 3.8+ (matplotlib, numpy, pandas)

**Ubuntu/Linux (Tomorrow):**
- NS-3 (latest version)
- C++ compiler (g++)
- Python 3.8+

### 🚀 Quick Start

#### Windows Setup
```bash
# Install Python dependencies
pip install matplotlib numpy pandas scipy

# Run analysis on sample data
python python-analysis/plot_graphs.py
```

#### Ubuntu Setup (See UBUNTU_SETUP.md)
```bash
# Install NS-3
# Run simulation: ./ns3 run tcp_comparison
# Generate plots: python3 plot_graphs.py
```

### 📄 Expected Report Sections
1. **Introduction** - What are TCP congestion algorithms?
2. **Problem Statement** - Why compare these three?
3. **Methodology** - Simulation setup
4. **Results** - Graphs and metrics
5. **Analysis** - Which is better and why?
6. **Conclusion** - Key findings

### 📅 Timeline
- **Today (Windows)**: Project structure + Python tools ready
- **Tomorrow (Ubuntu)**: Run NS-3 simulation + collect data
- **Day 3**: Analyze results + write report

---
**Status**: Setup complete ✓ | Ready for Ubuntu deployment
