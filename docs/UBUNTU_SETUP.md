# Ubuntu Setup Guide for NS-3 TCP Simulation

## Prerequisites
- Ubuntu 20.04 LTS or 22.04 LTS (recommended)
- At least 5GB disk space
- 4GB RAM minimum

## Step 1: Install Dependencies

```bash
sudo apt update
sudo apt upgrade -y

# Essential build tools
sudo apt install -y build-essential git python3 python3-dev python3-pip

# NS-3 dependencies
sudo apt install -y \
    gcc g++ pkg-config \
    gsl-bin libgsl-dev libgsl0-dev \
    python3-pygraphviz python3-yaml \
    libgtk-3-dev \
    sqlite3 libsqlite3-dev \
    libxml2 libxml2-dev \
    cmake libc6-dev \
    tcpdump

# Python for analysis
pip3 install matplotlib numpy pandas scipy seaborn
```

## Step 2: Download and Build NS-3

```bash
# Create workspace directory
mkdir -p ~/ns3-workspace
cd ~/ns3-workspace

# Clone NS-3 (version 3.36 or later recommended)
git clone https://github.com/nsnam/ns-3-dev-git.git ns-3
cd ns-3

# Configure
./ns3 configure --enable-tests --enable-examples

# Build (this takes 10-15 minutes)
./ns3 build -j4
```

**Build Verification:**
```bash
./ns3 run hello-simulator
# Should output: Hello Simulator
```

## Step 3: Copy Simulation Files

```bash
# Navigate to NS-3 examples directory
cd ~/ns3-workspace/ns-3/examples/tcp/

# Copy the TCP comparison script
cp /path/to/NS3-TCP-Comparison/ns3-scripts/tcp_comparison.cc .

# Alternatively, if on same machine:
cp ~/NS3-TCP-Comparison/ns3-scripts/tcp_comparison.cc .
```

## Step 4: Build and Run Simulation

```bash
# From ns-3 root directory
cd ~/ns3-workspace/ns-3

# Build the example
./ns3 build

# Run simulation with output
./ns3 run tcp_comparison --CmdLine="--logging=1"

# Expected runtime: 2-5 minutes depending on simulation parameters
```

## Step 5: Generate Output Files

The simulation creates:
- `tcp-reno.pcap` - Packet capture for TCP Reno
- `tcp-newreno.pcap` - Packet capture for TCP NewReno
- `tcp-cubic.pcap` - Packet capture for TCP Cubic
- `simulation-metrics.txt` - Raw metrics data

**Verify output:**
```bash
ls -la *.pcap
cat simulation-metrics.txt
```

## Step 6: Analyze with Python

```bash
# Copy Python analysis scripts
cp -r ~/NS3-TCP-Comparison/python-analysis/ .

# Run analysis
python3 python-analysis/metrics.py
python3 python-analysis/plot_graphs.py

# Check results
ls -la graphs/
```

## Troubleshooting

### Build Fails
```bash
# Clean and rebuild
./ns3 clean
./ns3 configure --enable-tests
./ns3 build -j2  # Use single job if memory limited
```

### Missing Dependencies
```bash
# Re-run dependency installation
sudo apt install -y $(cat dep-list.txt)
```

### PCAP Generation Issues
Ensure you have write permissions in current directory:
```bash
chmod 755 .
touch test.txt && rm test.txt
```

---

**Next Steps**: Once setup is complete, see SIMULATION_GUIDE.md for running the full experiment.
