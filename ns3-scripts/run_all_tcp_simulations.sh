#!/bin/bash
# Automated script to run all three TCP protocol simulations
# Place this in: ~/ns3-workspace/ns-3/
# Run with: chmod +x run_all_tcp_simulations.sh && ./run_all_tcp_simulations.sh

echo "========================================"
echo "TCP Protocol Comparison - Full Simulation Suite"
echo "========================================"
echo ""

# Configuration
NS3_DIR="$(pwd)"
PROTOCOLS=("TcpReno" "TcpNewReno" "TcpCubic")
NNODES=15
SIMTIME=60
TOTAL_PROTOCOLS=${#PROTOCOLS[@]}

# Check if ns3 executable exists
if [ ! -f "./ns3" ]; then
    echo "ERROR: ns3 executable not found!"
    echo "Make sure you're in the NS-3 root directory"
    exit 1
fi

echo "Configuration:"
echo "  Directory: $NS3_DIR"
echo "  Protocols: ${PROTOCOLS[@]}"
echo "  Nodes: $NNODES"
echo "  Simulation Time: $SIMTIME seconds"
echo ""

# Function to run a simulation
run_simulation() {
    local protocol=$1
    local counter=$2
    
    echo "========================================"
    echo "[$counter/$TOTAL_PROTOCOLS] Running $protocol..."
    echo "========================================"
    
    START_TIME=$(date +%s)
    
    ./ns3 run tcp_comparison --CmdLine="--protocol=$protocol --nNodes=$NNODES --simTime=$SIMTIME"
    
    if [ $? -eq 0 ]; then
        END_TIME=$(date +%s)
        DURATION=$((END_TIME - START_TIME))
        echo "✓ $protocol completed in $DURATION seconds"
        echo "Output: ${protocol}-metrics.txt"
    else
        echo "✗ $protocol FAILED"
        return 1
    fi
    echo ""
}

# Run all simulations
SIMULATION_FAILED=0
for i in "${!PROTOCOLS[@]}"; do
    RUN_NUMBER=$((i + 1))
    run_simulation "${PROTOCOLS[$i]}" "$RUN_NUMBER"
    
    if [ $? -ne 0 ]; then
        SIMULATION_FAILED=1
    fi
done

# Verify output files
echo "========================================"
echo "Verification"
echo "========================================"

ALL_FILES_EXIST=true
for protocol in "${PROTOCOLS[@]}"; do
    METRICS_FILE="${protocol}-metrics.txt"
    
    if [ -f "$METRICS_FILE" ]; then
        SIZE=$(wc -c < "$METRICS_FILE")
        echo "✓ $METRICS_FILE exists ($SIZE bytes)"
    else
        echo "✗ $METRICS_FILE NOT FOUND"
        ALL_FILES_EXIST=false
    fi
done

echo ""

# Summary
if [ $SIMULATION_FAILED -eq 0 ] && [ "$ALL_FILES_EXIST" = true ]; then
    echo "========================================"
    echo "✓ ALL SIMULATIONS COMPLETED SUCCESSFULLY"
    echo "========================================"
    echo ""
    echo "Next steps:"
    echo "1. Copy metrics files to Windows:"
    echo "   mkdir -p ~/NS3-TCP-Comparison/data/"
    echo "   cp *-metrics.txt ~/NS3-TCP-Comparison/data/"
    echo ""
    echo "2. On Windows, run:"
    echo "   python d:\\luv\\NS3-TCP-Comparison\\python-analysis\\plot_graphs.py"
    echo ""
    echo "3. View results in:"
    echo "   d:\\luv\\NS3-TCP-Comparison\\results\\"
    echo ""
else
    echo "========================================"
    echo "✗ SIMULATIONS COMPLETED WITH ERRORS"
    echo "========================================"
    exit 1
fi
