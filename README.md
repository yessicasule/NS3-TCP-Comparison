# NS-3 TCP Protocol Comparison Study
## Comparing TCP Reno vs TCP NewReno vs TCP Cubic

### Project Overview
This (IOT-ISE) project simulates and compares three TCP congestion control algorithms using **NS-3 Network Simulator**:
- **TCP Reno** (standard TCP)
- **TCP NewReno** (improved recovery)
- **TCP Cubic** (modern algorithm)

### 🎯 Learning Objectives
1. Understand network simulation using NS-3
2. Compare TCP congestion control mechanisms
3. Analyze performance metrics through graphs
4. Write technical report with findings

### Performance Metrics
The simulation will measure:
- **Throughput** (Mbps) - Data sent successfully per second
- **Packet Delivery Ratio (PDR)** (%) - Successful packets / Total packets
- **End-to-End Delay** (ms) - Time from sender to receiver
- **Packet Loss** (%) - Failed packets / Total packets
- **RTT (Round-Trip Time)** (ms) - Network response time

### Network Topology
```
Sender → Router1 ←→ Router2 → Receiver
                      (congested link)

Nodes: 10-20
Links: Point-to-Point with bandwidth constraints
Traffic: TCP flows sending large files
```
