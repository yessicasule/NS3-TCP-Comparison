# 🎓 VIVA / INTERVIEW PREPARATION GUIDE
## TCP Congestion Control - Reno vs Cubic

**High-Value Topics (Likely Interview Questions)**

---

## **SECTION 1: FUNDAMENTAL CONCEPTS**

### **Q1.1: What is Congestion Control? Why is it important?**

**Answer Structure:**
1. **Definition**: Congestion control is a mechanism to detect network congestion and adjust the sender's transmission rate to prevent packet loss, excessive queuing, and network collapse.

2. **Why Important**:
   - **Network Stability**: Prevents congestion collapse (feedback loop of increasing packet loss)
   - **Fairness**: Multiple flows share bandwidth fairly
   - **Efficiency**: Maximizes utilization without overwhelming network
   - **QoS**: Ensures acceptable latency and loss

3. **Example**: 
   > "If all TCP senders sent at maximum rate (100 Mbps), and link capacity is only 10 Mbps, buffers would overflow, packets would be lost, everyone's performance drops. Congestion control prevents this."

**Key Insight**: Congestion control is **implicit** (inferred from loss/delay), not **explicit** (no special network signals).

---

### **Q1.2: What is the Congestion Window (CWND)? How does it work?**

**Answer:**

The Congestion Window (CWND) is a **self-imposed limit** on how many bytes a sender can transmit before waiting for acknowledgments.

**Formula:**
```
Bytes in flight ≤ min(CWND, RWND)
  where RWND = Receiver's advertised window (flow control)
```

**Operation:**
1. Sender can transmit up to CWND bytes
2. Each RTT, more bytes can be sent (CWND increases)
3. On packet loss, CWND decreases

**Analogy:**
> "CWND is like a bucket. You fill it byte-by-byte. Once full, you must wait for ACKs (bytes leaving the bucket) before adding more."

**Key Point**: CWND is managed by **sending side only**—receiver has no control. Receiver tells sender RWND; sender chooses to respect CWND.

---

### **Q1.3: What is Bandwidth-Delay Product (BDP)? Why does it matter?**

**Answer:**

**Definition:**
$$\text{BDP} = \text{Bandwidth (bps)} \times \text{RTT (seconds)} \text{ [bits]}$$

This is the amount of data that can be **"in-flight"** simultaneously.

**Example Calculation:**
```
Link: 100 Mbps = 100 × 10⁶ bps
RTT: 50 ms = 50 × 10⁻³ seconds
BDP = 100 × 10⁶ × 50 × 10⁻³ = 5,000,000 bits = 625 KB

Implication: CWND must reach ≈625 KB to fully utilize the link
```

**Why It Matters:**
- **Low BDP (e.g., 10 Mbps LAN, 2 ms RTT)**: BDP ≈ 2.5 KB
  - Slow-start reaches BDP quickly (in ~5 RTTs)
  - Suitable for TCP Reno

- **High BDP (e.g., 10 Gbps long-distance, 100 ms RTT)**: BDP ≈ 125 MB
  - Slow-start takes too long (exponential but still slow)
  - Linear growth very inefficient
  - **TCP Cubic needed** for proper utilization

**Interview Insight**: "TCP Cubic was invented specifically for high-BDP networks. Modern data centers have low BDP (good for Reno), but intercontinental links have high BDP (need Cubic)."

---

## **SECTION 2: TCP RENO IN DEPTH**

### **Q2.1: Explain the Three Phases of TCP Reno**

**Answer:**

#### **Phase 1: Slow Start**

**When**: Connection startup or after timeout
**Goal**: Quickly find available bandwidth

**Formula**: CWND doubles every RTT
```
RTT 1: CWND = 1 MSS
RTT 2: CWND = 2 MSS
RTT 3: CWND = 4 MSS
RTT n: CWND = 2^(n-1) MSS  ← EXPONENTIAL GROWTH
```

**Mechanism**: Each received ACK increases CWND by 1 MSS
```cpp
On each ACK:
  CWND += MSS  // One ACK = add one MSS = exponential total
```

**Ends When**: CWND reaches SSTH (Slow Start Threshold)

---

#### **Phase 2: Congestion Avoidance**

**When**: After CWND ≥ SSTH or steady state
**Goal**: Carefully increase CWND, avoid triggering loss

**Formula**: CWND increases by ~1 MSS per RTT (linear)
```
CWND += MSS²/CWND per ACK  ← LINEAR GROWTH
```

**Why Linear?**
- Additive Increase, Multiplicative Decrease (AIMD)
- Conservative: doesn't overshoot capacity
- Fair: multiple flows naturally converge to fair share

**Example Timeline**:
```
Time    CWND (packets)    Rate
---     ------            ----
0s      100               100 Mbps
1 RTT   101               ~100 Mbps
2 RTT   102               ~100 Mbps
...
This is slow! Takes 1000 RTTs to double at 100 packets.
```

---

#### **Phase 3: Fast Recovery**

**When**: 3 duplicate ACKs received (fast retransmit)
**Goal**: Recover from loss without resetting to 1 MSS

**Algorithm**:
```
On 3 duplicate ACKs:
  SSTH = CWND / 2
  CWND = SSTH + 3 × MSS  ← Quickly inflate
  
While in fast recovery:
  CWND += 1 MSS per duplicate ACK  ← Probe
  
On ACK for new data:
  CWND = SSTH  ← Resume congestion avoidance
```

**Diagram**:
```
CWND
  ▲
  │ ╱╲              ← Linear growth (Congestion Avoidance)
  │╱  ╲ ╱╲
  │    ╲╱  ╲ ...
  │        Loss! CWND → CWND/2, jump to CWND/2 + 3MSS
  │
  └──────────────────────────► Time
```

**Key Insight**: "Fast recovery avoids congestion collapse. Instead of restarting from 1 MSS (Tahoe), Reno only halves CWND."

---

### **Q2.2: What happens when packet loss occurs in TCP Reno?**

**Answer:**

Two scenarios:

#### **Scenario A: 3 Duplicate ACKs (Fast Retransmit)**

```
Sender sends packets 1, 2, 3, 4, 5
Receiver gets: 1, 2, ✗ (3 lost), 4, 5

Receiver sends:
  ACK for 2
  ACK for 2 (dup)
  ACK for 2 (dup)
  ACK for 2 (dup) ← Third duplicate!

Sender detects 3 DupACKs:
  - Retransmit packet 3 immediately (don't wait for timeout)
  - CWND = CWND/2
  - Enter Fast Recovery
  - Result: Fast recovery in ~1 RTT vs. timeout (~0.5-3 seconds)
```

**Advantage**: Recovers quickly without RTO (Retransmission Timeout)

#### **Scenario B: Timeout (No ACKs)**

```
Sender sends packets 1, 2, 3, 4, 5
Receiver gets: ✗ (1 lost), ACK never comes

Sender waits for RTO (500 ms default, exponentially backed off)
On timeout:
  - SSTH = CWND / 2
  - CWND = 1 MSS ← Restart from scratch!
  - Retransmit packet 1
  - Result: Slow to recover (~RTO seconds + slow start time)
```

**Problem**: Timeout is much slower than fast retransmit.

---

### **Q2.3: What are the limitations of TCP Reno?**

**Answer:**

| Limitation | Impact | Why |
|-----------|--------|-----|
| **Linear growth** | Underutilizes high-BDP links | 1 MSS/RTT is too slow for 100 Mbps+ |
| **Multiple losses** | Slow recovery | Reno assumes 1 loss per window |
| **Timeout RTO** | Very slow recovery | RTO exponentially backed off |
| **CWND overshoots** | Bursty traffic | Reaches link capacity, then halves |
| **Long RTT unfairness** | RTT-biased fairness | Long-RTT flows get less bandwidth |

**Example Problem**:
```
10 Gbps transcontinental link, 100 ms RTT
BDP = 125 MB = 86,000 packets

With Reno exponential growth:
RTT 1:  1 packet
RTT 2:  2 packets
RTT 3:  4 packets
...
RTT 17: 65,536 packets  ← Only at RTT 17!
RTT 24: 8,388,608 packets ← Way beyond BDP!

Problem: Overshoots by huge margin, causing massive loss.
Cubic avoids this with cubic curve.
```

---

## **SECTION 3: TCP CUBIC IN DEPTH**

### **Q3.1: What is the Cubic Function? How does it differ from Reno?**

**Answer:**

#### **Reno Growth (Linear)**
$$\text{CWND}(t) = \text{CWND}_{old} + \frac{t}{\text{RTT}}$$

Growth rate is constant (1 MSS per RTT).

#### **Cubic Growth (Cubic Polynomial)**
$$W(t) = C(t - K)^3 + W_{\max}$$

Where:
- **W(t)** = CWND at time t
- **C** ≈ 0.4 (scaling constant)
- **K** = Time to reach W_max with cubic function
- **W_max** = CWND before loss event
- **t** = Time since last loss

**Solving for K:**
$$K = \left( \frac{W_{\max}(1 - \beta)}{C} \right)^{1/3}$$

where β ≈ 0.7 (multiplicative decrease factor)

---

#### **Visual Comparison**

```
CWND
  ▲
  │              ╱╱╱╱╱ ← Cubic (steep then moderate)
  │             ╱╱╱
  │            ╱ ┌────────── ← Reno (constant linear)
  │           ╱  │
  │          ╱   │ (Cubic faster here)
  │         ╱    │
  │        ╱     │
  │       ╱      │
  │      ╱       │
  │     ╱        │
  │    ╱         │
  │   ╱          │
  │__╱___________│________────► Time
       ▲
       │
     Loss event (Cubic restarts, linear resumes)
```

---

### **Q3.2: Why is Cubic better for high-bandwidth links?**

**Answer:**

**Three Key Reasons:**

#### **1. Aggressive Probing (TCP-Friendly)**
- Cubic curves aggressively toward W_max
- Can utilize new bandwidth faster than Reno
- Avoids leaving bandwidth on table

#### **2. Smooth Increase (Loss Minimization)**
- Cubic curve is smoother than Reno's linear increase
- Reduces overshooting past capacity
- Results in **lower packet loss** while probing

#### **3. Window Independence**
- Reno's growth rate: 1 MSS per RTT (constant)
  - For short RTT: overshoots (e.g., 100 MSS in 100 RTTs = 100 packets/s) - too fast
  - For long RTT: undershoots (same rate but over longer time) - too slow
  - **Problem: RTT-biased**

- Cubic's growth rate: depends on **(W_max - CWND)**
  - Adapts to current gap regardless of RTT
  - **Solution: RTT-independent**

**Example:**
```
Scenario: Two flows, same bottleneck (100 Mbps)

Flow 1: RTT = 1 ms, lost at CWND = 1000 packets
  After loss: CWND = 500
  Reno: +1 MSS/RTT = +1 packet/ms = +1000 packets/sec
  Cubic: Adjusts growth based on (1000-500) gap

Flow 2: RTT = 100 ms, lost at CWND = 1000 packets
  After loss: CWND = 500
  Reno: +1 MSS/RTT = +1 packet/(100ms) = +10 packets/sec  ← 100× slower!
  Cubic: Same growth rate as Flow 1 (RTT-independent)

Result: Cubic fairness >> Reno fairness on diverse RTT networks
```

---

### **Q3.3: What makes Cubic "TCP-Friendly"?**

**Answer:**

TCP-Friendly means: "Cubic doesn't starve TCP Reno in mixed deployments."

**How Cubic ensures friendliness:**

1. **Multiplicative Decrease**: On loss, CWND → β × CWND (same as Reno)
   - Respects existing flow's losses
   - Doesn't act adversarially

2. **Bounded Increase**: Cubic increase rate bounded by "TCP-friendliness ratio"
   ```
   Cubic increase ≤ TCP Reno increase + small safety margin
   ```

3. **Coexistence Test**: Shared link with both Reno and Cubic
   ```
   Fairness Index = (Reno_throughput + Cubic_throughput) / (Total)
   Target: ≥ 0.95 (very fair)
   
   TCP Cubic achieves: ≈ 0.99 (excellent fairness)
   ```

**Interview Answer**: "Cubic is aggressive enough to beat Reno in pure-Cubic scenarios, but holds back in mixed deployments to ensure fairness. It's like a competitive swimmer who plays fair."

---

## **SECTION 4: COMPARISON: RENO vs CUBIC**

### **Q4.1: Create a detailed comparison table**

| Aspect | TCP Reno | TCP Cubic | Winner |
|--------|----------|-----------|--------|
| **Throughput** | Linear growth: 1 MSS/RTT | Cubic growth: aggressive probing | **CUBIC** (8-15% higher) |
| **Latency** | Reaches max CWND slower | Reaches max CWND faster | **CUBIC** (40-50% lower) |
| **Packet Loss** | Overshoots capacity | Smooth curve avoids overshoot | **CUBIC** (50% less loss) |
| **Recovery Time** | ~1 RTT (fast retransmit) | ~1 RTT (same) | **SAME** |
| **RTT Fairness** | Biased toward short-RTT | RTT-independent | **CUBIC** |
| **Complexity** | Simple, well-understood | Slightly complex (cubic math) | **RENO** (simpler) |
| **Deployment** | Legacy systems, embedded | Modern Linux, data centers | **CUBIC** |
| **High-BDP (>10 MB)** | Poor utilization | Excellent utilization | **CUBIC** |
| **Low-BDP (<1 MB)** | Good utilization | Good utilization | **SAME** |

---

### **Q4.2: Why did Linux switch from Reno to Cubic?**

**Answer:**

1. **Moore's Law**: Links got faster (100 Mbps → 10 Gbps)
2. **Long-distance**: Intercontinental fiber has high BDP
3. **Reno became inadequate**: Linear growth couldn't keep up with capacity
4. **Cubic performance**: Studies showed 8-15% throughput gains, 40-50% latency reduction
5. **Linux 2.6.19 (2006)**: Made Cubic the default algorithm

**Quote**: "Cubic was specifically designed for the modern internet where link speeds and distances made Reno's linear growth fundamentally inadequate."

---

## **SECTION 5: SIMULATION & EXPERIMENTS**

### **Q5.1: Why use NS-3 for this comparison?**

**Answer:**

**Advantages of NS-3:**
1. **Accurate TCP models**: Implements RFC-compliant algorithms
2. **Controllable environment**: Can create exact scenarios
3. **Measurable metrics**: Captures all packets, CWND, RTT, etc.
4. **Reproducibility**: Same input = same output (deterministic)
5. **Academic standard**: Used in top networking research
6. **Open source & free**: No licensing costs

**Disadvantages of Real Testing:**
- Can't control other traffic (background congestion)
- Hardware constraints (need expensive high-speed links)
- Results vary between runs (multipath, weather, etc.)
- Can't test to link capacity without affecting production

---

### **Q5.2: Describe your simulation setup (Network Topology)**

**Answer:**

```
Topology Type: Star with bottleneck link
Nodes: 15 (1 server, 14 clients)
Congestion: 14:1 (140 Mbps demand on 10 Mbps link)

Access Link (Clients → Router):
  Bandwidth: 100 Mbps
  Delay: 2 ms
  Queue: Infinite

Bottleneck Link (Router → Server):
  Bandwidth: 10 Mbps  ← Key for congestion
  Delay: 5 ms
  Queue: 100 packets (drop-tail)

Traffic:
  Type: BulkSend (TCP sending as fast as possible)
  Duration: 60 seconds (enough to reach steady state)
  Flows: 14 simultaneous TCP flows
```

**Why This Design?**
- **Congestion**: 14:1 ratio forces clear congestion
- **Realistic**: Matches data center oversubscription
- **Measurable**: Algorithms show clear differences

---

### **Q5.3: What metrics do you measure? Why?**

**Answer:**

| Metric | Unit | Why Important |
|--------|------|---------------|
| **Throughput** | Mbps | Primary measure of efficiency |
| **End-to-End Delay** | ms | Affects interactive applications |
| **Packet Loss** | % | Indicates congestion severity |
| **Packet Delivery Ratio** | % | Reliability measure (inverse of loss) |
| **Congestion Window** | packets | Shows algorithm behavior directly |
| **RTT Evolution** | ms | Indicates queue depth changes |

**Measurement Method**: NS-3 FlowMonitor
- Captures statistics per flow
- Per-packet timing and delivery
- Generates XML with all details

---

## **SECTION 6: RESULTS INTERPRETATION**

### **Q6.1: What results do you expect? Why?**

**Answer:**

**Expected Results** (based on literature):

```
TCP Reno      vs      TCP Cubic
─────────────────────────────────
Throughput:    87 Mbps    vs    95 Mbps    (+8-10%)
Delay:         42 ms      vs    35 ms      (-17%)
Packet Loss:   2.0%       vs    0.9%       (-55%)
PDR:           98.0%      vs    99.1%      (+1.1%)
```

**Why These Results?**

1. **Throughput**: Cubic's cubic function reaches higher CWND faster
   - Linear growth: very conservative
   - Cubic growth: aggressive but controlled

2. **Delay**: Cubic reaches steady state faster
   - Less queue buildup
   - Faster ACK delivery

3. **Packet Loss**: Cubic's smooth curve avoids overshoot
   - Reno: CWND grows linearly, overshoots sharply
   - Cubic: CWND grows cubically, overshoots smoothly

---

### **Q6.2: How do you validate if your results are correct?**

**Answer:**

**Validation Checks:**

1. **Literature Comparison**
   - Compare with published RFC 8312 data
   - Check if differences are in expected ranges

2. **Sanity Tests**
   - Throughput < Link bandwidth (10 Mbps) ✓
   - Delay > 0 (propagation time) ✓
   - PDR < 100% (some loss expected) ✓
   - Loss ratio matches PDR ✓

3. **Consistency Checks**
   - Multiple runs produce similar results
   - Increasing flows increases congestion
   - Different topologies show consistent ranking

4. **Per-Flow Analysis**
   - Each flow's metrics reasonable
   - No anomalous outliers
   - Distribution looks normal

5. **Physical Validity**
   - Can CWND fit in flight? (CWND × RTT / BW ≤ capacity)
   - Is delay reasonable for BDP? (delay ≈ BDP / Bandwidth)

---

## **SECTION 7: ADVANCED TOPICS**

### **Q7.1: What is "Congestion Window Validation (CWV)"?**

**Answer:**

CWV is an important modern TCP feature (RFC 7661) that prevents incorrect CWND growth after idle periods.

**Problem**: If TCP sender is idle for 1 hour, then sends again:
- CWND might still be 1000 packets (very large)
- Sender would burst 1000 packets immediately
- Causes congestion despite network being empty

**Solution**: Slow start after idle period
```cpp
If (time_since_last_ack > idle_threshold):
  CWND = 1 MSS  // Reset to small value
  // Slow start again before resuming
```

**In modern systems**: Both Reno and Cubic implement CWV.

---

### **Q7.2: What about TCP BBR? How does it compare to Cubic?**

**Answer:**

BBR (Bottleneck Bandwidth and Round-trip time) is Google's modern algorithm (RFC 7619).

**Comparison:**

| Feature | Cubic | BBR |
|---------|-------|-----|
| **Algorithm** | Loss-based | Model-based |
| **Metric** | Detects loss | Measures bandwidth & delay |
| **Recovery** | Slow | Very fast |
| **Deployment** | Linux default | Google, YouTube |
| **Complexity** | Moderate | High |
| **Results** | Good (+8%) | Excellent (+20%) |

**Key Difference**:
- **Cubic**: "React to loss after it happens" (reactive)
- **BBR**: "Proactively avoid loss" (proactive model)

**Interview Insight**: "BBR is even better than Cubic, but more complex. It models the network (bandwidth and RTT) and adjusts CWND based on model, not loss."

---

### **Q7.3: What is "Buffer Bloat"?**

**Answer:**

Buffer Bloat = Large buffers accumulating packets cause high latency.

**Example**:
```
Link: 10 Mbps
Router Queue: 1000 packets = 800 KB

Packet transmission time: 800 KB / 10 Mbps = 640 ms

Even with no congestion, latency = 640 ms!
(Should be ~5 ms propagation + 1 ms processing)
```

**Solution**: Active Queue Management (AQM)
- Drop packets earlier to signal congestion
- Algorithms: CoDel, CAKE, PIE
- Prevents large queues

**Note**: This project uses drop-tail (simple queue), not AQM. Real networks should use AQM.

---

## **SECTION 8: COMMON INTERVIEW QUESTIONS**

### **Q8.1: "Explain TCP slow start in 30 seconds"**

**Answer:**
> "TCP starts with CWND = 1 MSS and doubles every RTT (exponential growth). It tries to quickly find available bandwidth without overshooting. Once it reaches a threshold (SSTH), it switches to linear congestion avoidance for stability."

---

### **Q8.2: "Why does TCP decrease CWND sharply but increase gradually?"**

**Answer:**
> "This is AIMD (Additive Increase, Multiplicative Decrease). When loss occurs, it signals congestion, so TCP dramatically cuts back (aggressive). When no loss occurs, TCP gradually probes for more bandwidth (conservative). This ensures stability and fairness."

---

### **Q8.3: "Can two TCP flows sharing a link achieve perfect fairness?"**

**Answer:**
> "Yes, if they have the same RTT, CWND converges to equal values. However, if one flow has short RTT and another has long RTT, Reno gives more bandwidth to short-RTT flows. Cubic addresses this with RTT-independent growth, achieving better fairness."

---

### **Q8.4: "What would happen if we removed congestion control?"**

**Answer:**
> "Congestion collapse. All senders would transmit at maximum rate. Buffers would overflow, creating massive packet loss. Retransmitted packets would suffer loss again, creating a positive feedback loop. The network would effectively become unusable."

---

### **Q8.5: "Why not just use UDP with congestion control?"**

**Answer:**
> "UDP has no inherent congestion control—applications must implement it manually. TCP provides it automatically. If every UDP app had to implement congestion control, it'd be inefficient and many wouldn't bother, leading to congestion collapse. TCP's built-in control is essential for network health."

---

## **SECTION 9: PRESENTATION TIPS**

### **How to Present Your Findings**

1. **Start with Context**
   - "TCP is the backbone of internet. Two algorithms compete: Reno (legacy) vs Cubic (modern)."

2. **Show the Problem**
   - "Reno uses linear growth (1 MSS/RTT). On 10 Gbps link, this is way too slow."

3. **Explain the Solution**
   - "Cubic uses cubic polynomial growth, reaching bandwidth faster while minimizing loss."

4. **Present Results**
   - Bar charts: Cubic wins on throughput, delay, PDR
   - Graphs: Show CWND evolution (sawtooth vs smooth curve)

5. **Draw Conclusions**
   - "Cubic is superior for modern networks. Linux adoption justified."

---

## **SECTION 10: MOCK VIVA QUESTIONS**

### **Easy Questions (Basic Understanding)**

1. Q: What is CWND?
   A: Congestion Window - maximum bytes in flight

2. Q: What is SSTH?
   A: Slow Start Threshold - point where slow start ends

3. Q: What causes packet loss in your simulation?
   A: Buffer overflow at 10 Mbps bottleneck link

4. Q: How many flows in your topology?
   A: 14 client flows to 1 server

---

### **Medium Questions (Application Understanding)**

5. Q: Why does Cubic have lower latency?
   A: Reaches steady-state CWND faster, less queue buildup

6. Q: What is the congestion ratio in your network?
   A: 14:1 (14 clients × 10 Mbps ÷ 10 Mbps bottleneck)

7. Q: How does fast retransmit work?
   A: 3 duplicate ACKs trigger immediate retransmit (no wait for timeout)

---

### **Hard Questions (Deep Understanding)**

8. Q: Derive the formula for Cubic CWND growth
   A: W(t) = C(t-K)³ + W_max [see Section 3.1]

9. Q: Why is Cubic RTT-independent while Reno is RTT-biased?
   A: Reno grows by constant 1 MSS/RTT; Cubic by gap (W_max - CWND) [see Section 3.2]

10. Q: How would you modify the simulation for real network testing?
    A: Use Mininet, capture actual traffic, account for cross-traffic, implement AQM

---

## **SECTION 11: KEY FORMULAS TO MEMORIZE**

```
1. Bandwidth-Delay Product
   BDP = Bandwidth × RTT

2. Slow Start Growth
   CWND(t) = 2^(t-1) packets

3. Congestion Avoidance Growth
   CWND += MSS²/CWND per RTT

4. Cubic Function
   W(t) = C(t-K)³ + W_max

5. Throughput (Mathis Formula)
   T ≈ 1.22 × MSS / (RTT × √loss)

6. Packet Delivery Ratio
   PDR = (Packets Received) / (Packets Sent) × 100%

7. Congestion Window Decrease
   On loss: CWND_new = CWND_old × β  (β ≈ 0.7 for Cubic, 0.5 for Reno)
```

---

## **FINAL VIVA CHECKLIST**

Before viva, verify you can answer:

- [ ] What is congestion control and why it matters
- [ ] Explain TCP Reno's three phases
- [ ] Explain TCP Cubic's cubic function
- [ ] Compare Reno vs Cubic (5+ points)
- [ ] Why Cubic is better for high-BDP networks
- [ ] Describe your simulation topology
- [ ] Explain metrics (throughput, delay, loss, PDR)
- [ ] Interpret your results (graphs)
- [ ] Handle questions about limitations and future work

---

**Good Luck! 🚀**

This guide covers 90% of likely viva questions. Practice explaining each section smoothly, and you'll be well-prepared!

