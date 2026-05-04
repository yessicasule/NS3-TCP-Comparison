# NS-3 TCP Simulation Execution Guide

## Quick Reference

### 1. Build Simulation
```bash
cd ~/ns3-workspace/ns-3
./ns3 configure --enable-tests
./ns3 build
```

### 2. Run Single Protocol Simulation
```bash
# Run TCP Reno
./ns3 run tcp_comparison --CmdLine="--nNodes=15 --simTime=60 --protocol=TcpReno"

# Run TCP NewReno
./ns3 run tcp_comparison --CmdLine="--nNodes=15 --simTime=60 --protocol=TcpNewReno"

# Run TCP Cubic
./ns3 run tcp_comparison --CmdLine="--nNodes=15 --simTime=60 --protocol=TcpCubic"
```

### 3. Run All Three Protocols (Batch Script)
Create `run_all_simulations.sh`:

```bash
#!/bin/bash
echo "Starting TCP Comparison Simulations..."

cd ~/ns3-workspace/ns-3

# Run each protocol
for protocol in TcpReno TcpNewReno TcpCubic; do
    echo "Running $protocol..."
    ./ns3 run tcp_comparison --CmdLine="--nNodes=15 --simTime=60 --protocol=$protocol"
    echo "$protocol completed\n"
done

echo "All simulations completed!"
```

Run with:
```bash
chmod +x run_all_simulations.sh
./run_all_simulations.sh
```

## Detailed Steps

### Step 1: Verify Setup
```bash
cd ~/ns3-workspace/ns-3

# Test build
./ns3 run hello-simulator
# Output: Hello Simulator
```

### Step 2: Copy Simulation File (if needed)
```bash
cp ~/NS3-TCP-Comparison/ns3-scripts/tcp_comparison.cc examples/tcp/
```

### Step 3: Run Individual Simulations

#### Protocol 1: TCP Reno
```bash
./ns3 run tcp_comparison --CmdLine="--protocol=TcpReno --nNodes=15 --simTime=60 --logging=1"
```

**Output files:**
- `tcp-reno-0-0.pcap` - Packet capture
- `TcpReno-metrics.txt` - Metrics summary
- `flowmon-results.xml` - Detailed flow monitor data

#### Protocol 2: TCP NewReno
```bash
./ns3 run tcp_comparison --CmdLine="--protocol=TcpNewReno --nNodes=15 --simTime=60 --logging=1"
```

#### Protocol 3: TCP Cubic
```bash
./ns3 run tcp_comparison --CmdLine="--protocol=TcpCubic --nNodes=15 --simTime=60 --logging=1"
```

### Step 4: Collect Output Files
```bash
# Create data directory
mkdir -p ~/NS3-TCP-Comparison/data

# Copy metrics files
cp ~/ns3-workspace/ns-3/*-metrics.txt ~/NS3-TCP-Comparison/data/
cp ~/ns3-workspace/ns-3/flowmon-results.xml ~/NS3-TCP-Comparison/data/

# Verify
ls -la ~/NS3-TCP-Comparison/data/
```

### Step 5: Generate Analysis Graphs (on Windows)
```bash
# Copy data to Windows machine or run:
python3 ~/NS3-TCP-Comparison/python-analysis/plot_graphs.py
```

## Expected Output Timeline

| Step | Duration | Output |
|------|----------|--------|
| Run TCP Reno | 2-3 min | *-reno-metrics.txt, PCAP |
| Run TCP NewReno | 2-3 min | *-newreno-metrics.txt, PCAP |
| Run TCP Cubic | 2-3 min | *-cubic-metrics.txt, PCAP |
| **Total** | **6-10 min** | **3 metrics + 3 PCAP files** |

## Interpreting Output

### Metrics File Format
```
Protocol,Throughput(Mbps),Delay(ms),Loss(%),PDR(%)
TcpReno,87.5,42,2.0,98.0
```

### Console Output
```
=== AVERAGE METRICS FOR TcpReno ===
Average Throughput = 87.5 Mbps
Average Delay = 0.042 s
Packet Loss Ratio = 0.02
PDR = 0.98 (98%)
```

### PCAP Analysis (optional)
```bash
# View packet capture with Wireshark or tshark
tshark -r tcp-reno-0-0.pcap | head -20

# Count packets per flow
tshark -r tcp-reno-0-0.pcap -q -z io,phs
```

## Troubleshooting

### Simulation Hangs
```bash
# Check system resources
free -h
top -b -n1 | head -n 15

# Reduce simulation parameters
./ns3 run tcp_comparison --CmdLine="--nNodes=5 --simTime=30"
```

### Missing Output Files
```bash
# Verify build succeeded
./ns3 build -j2

# Check permissions
chmod 755 .

# Re-run with explicit paths
./ns3 run tcp_comparison --CmdLine="--protocol=TcpReno" 2>&1 | tee simulation.log
```

### NS-3 Errors
```bash
# Clean rebuild
./ns3 clean
./ns3 configure --enable-tests --enable-examples
./ns3 build -j4
```

## Performance Tips

### Speed Up Simulations
```bash
# Use parallel jobs during build
./ns3 build -j8

# Reduce simulation time for testing
./ns3 run tcp_comparison --CmdLine="--simTime=20 --nNodes=5"
```

### Monitor Resources
```bash
# In separate terminal
watch -n 1 'free -h && echo "---" && ps aux | grep tcp_comparison'
```

## Next Steps

1. ✓ Run all three protocol simulations
2. ✓ Collect output files
3. → Transfer data to Windows
4. → Generate graphs using Python
5. → Create report with analysis

---

**Estimated Time**: 15-20 minutes for complete simulation run
