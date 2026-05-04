# 📚 TONIGHT'S READING & PREPARATION GUIDE
## Study Plan for May 4-5, 2026

---

# **⏰ SUGGESTED SCHEDULE**

## **Tonight (May 4) - 2-3 hours**
Focus: Understanding the concepts for viva + knowing what to submit

## **Tomorrow Morning (May 5) - 1 hour**
Focus: Ubuntu setup and running simulations

## **Tomorrow Afternoon (May 5) - 1.5 hours**
Focus: Data analysis and report finalization

---

# **📖 TONIGHT'S READING LIST (Prioritized)**

## **🔴 ESSENTIAL (Must Read)**

### **1. VIVA_PREPARATION_GUIDE.md - Sections 1-4** (1 hour read)
**File**: `VIVA_PREPARATION_GUIDE.md`

**What to Read**:
- Section 1: Fundamental Concepts
  - Q1.1: What is Congestion Control? (5 mins)
  - Q1.2: What is CWND? (5 mins)
  - Q1.3: What is Bandwidth-Delay Product? (5 mins)

- Section 2: TCP Reno In Depth
  - Q2.1: Three Phases of TCP Reno (10 mins)
  - Q2.2: Packet Loss Handling (5 mins)

- Section 3: TCP Cubic In Depth
  - Q3.1: Cubic Function Explained (10 mins)
  - Q3.2: Why Cubic is Better (8 mins)

- Section 4: Comparison
  - Q4.1: Detailed Comparison Table (5 mins)
  - Q4.2: Why Linux Switched to Cubic (3 mins)

**Why**: These concepts will be asked in viva. Understanding them now means you won't panic tomorrow.

---

### **2. COMPLETE_PROJECT_REPORT_TEMPLATE.md - Sections 1-5** (45 mins read)
**File**: `COMPLETE_PROJECT_REPORT_TEMPLATE.md`

**What to Read**:
- Section 1: Introduction (5 mins)
- Section 2: Background & Literature Review (10 mins)
- Section 3: Problem Statement (8 mins)
- Section 4: Theoretical Framework (10 mins)
- Section 5: Methodology (12 mins)

**Why**: This is 60% of your report. Reading it now means you understand the full context of your project. Tomorrow you'll just insert data into it.

---

## **🟡 IMPORTANT (Should Read)**

### **3. TODAYS_COMPLETE_DELIVERABLES.md** (20 mins read)
**File**: `TODAYS_COMPLETE_DELIVERABLES.md` (this is a quick reference)

**Focus**: Sections:
- "What you have" (reassurance)
- "Workflow for tomorrow" (planning)
- "Strategic advantage" (confidence)

**Why**: Understand what's already done and what remains. Build confidence.

---

### **4. 00_QUICK_START.md** (15 mins read)
**File**: `00_QUICK_START.md`

**Focus**: Section "What You Need to Do Tomorrow"

**Why**: Prepare mentally for tomorrow's Ubuntu steps.

---

## **🟢 OPTIONAL (Good to Know)**

### **5. VIVA_PREPARATION_GUIDE.md - Sections 8-11** (20 mins)
**File**: `VIVA_PREPARATION_GUIDE.md`

**Sections**:
- Section 8: Common Interview Questions
- Section 10: Mock Viva Questions
- Section 11: Key Formulas

**Why**: Useful for quick review before viva (but less urgent tonight).

---

# **📋 READING CHECKLIST**

**Copy this list. Check off as you read:**

### **Tonight (Priority Order)**

- [ ] VIVA_PREPARATION_GUIDE.md Sections 1-4 (1 hour)
  - [ ] Sec 1: Fundamental Concepts
  - [ ] Sec 2: TCP Reno
  - [ ] Sec 3: TCP Cubic
  - [ ] Sec 4: Comparison

- [ ] COMPLETE_PROJECT_REPORT_TEMPLATE.md Sections 1-5 (45 mins)
  - [ ] Intro & Background
  - [ ] Problem & Objectives
  - [ ] Theory & Methodology

- [ ] TODAYS_COMPLETE_DELIVERABLES.md (20 mins)
  - [ ] What you have
  - [ ] Workflow tomorrow

- [ ] 00_QUICK_START.md (15 mins)
  - [ ] Ubuntu steps

**Total: ~2.5 hours of productive reading**

---

# **🎯 KEY CONCEPTS TO UNDERSTAND TONIGHT**

After tonight's reading, you should be able to answer (in your own words):

### **TCP Fundamentals**
1. What is congestion control?
2. How does TCP know when network is congested?
3. What is the congestion window (CWND)?
4. Why does TCP need both "increase" and "decrease" mechanisms?

### **TCP Reno (Legacy)**
5. What are the three phases of TCP Reno?
6. How does slow start work? (Exponential or linear?)
7. What happens when packet loss is detected?
8. Why is Reno called "Additive Increase, Multiplicative Decrease"?

### **TCP Cubic (Modern)**
9. What is a cubic function? How is it different from linear?
10. Why was Cubic invented?
11. Why is Cubic better for high-bandwidth links?
12. What does "RTT-independent" mean?

### **Comparison**
13. In 5 sentences, explain why Cubic is better than Reno
14. What is the expected throughput difference? (8-15% more for Cubic)
15. Where is Reno still used? Why?
16. What is the Linux default now? (Cubic)

### **Project Context**
17. What is your network topology?
18. What is the congestion ratio in your simulation?
19. What 4 metrics are you measuring?
20. Why use NS-3 instead of real network testing?

---

# **💡 LEARNING TIPS**

### **While Reading**
- **Take notes** on paper (reinforces memory)
- **Highlight key formulas** (you'll need them for viva)
- **Draw diagrams** (especially CWND evolution graphs)
- **Create concept maps** (connect related ideas)

### **After Each Section**
- Close the document
- Explain the concept to yourself (out loud)
- If stuck, re-read the section

### **Connect to Your Project**
- "How does this apply to my simulation?"
- "What graph will show this?"
- "What question might teacher ask about this?"

---

# **🎓 VIVA WARM-UP EXERCISES**

After reading, try these (without looking at answers):

### **Exercise 1: Explain in 30 seconds**
**Prompt**: "What is TCP congestion control and why is it important?"

**Your answer** (practice out loud):
> [Write/say your answer here]

**Check**: Does it mention network stability, fairness, efficiency, QoS?

---

### **Exercise 2: Compare and Contrast**
**Prompt**: "How does TCP Reno differ from TCP Cubic?"

**Your answer** (10-20 seconds):
> [Write/say your answer here]

**Check**: Does it mention linear vs cubic growth, RTT-independence, throughput difference?

---

### **Exercise 3: Explain Congestion Window**
**Prompt**: "What is CWND and how does it work?"

**Your answer** (15 seconds):
> [Write/say your answer here]

**Check**: Does it mention limit on bytes in-flight, increases on ACK, decreases on loss?

---

# **📊 CONCEPT MAP TO DRAW**

Draw this concept map on paper (helps memory):

```
                    TCP CONGESTION CONTROL
                             │
                ┌────────────┼────────────┐
                │            │            │
              WHY?         HOW?         WHEN?
              ├──          ├──          ├──
         Network         Window       Startup
         Stability        Growth      Congestion
         Fairness        ACK-based    Recovery
         Efficiency      Loss-based
                
                ┌──────────────────────────┐
                │   TWO MAIN ALGORITHMS   │
                ├──────────────────────────┤
                │                          │
           TCP Reno                   TCP Cubic
           ├─ Linear growth          ├─ Cubic growth
           ├─ Fast recovery          ├─ RTT-independent
           ├─ Sawtooth CWND          ├─ Smooth CWND
           ├─ Legacy (pre-2006)      ├─ Modern (2006+)
           └─ Used: Legacy systems   └─ Used: Linux default
```

---

# **🔑 KEY FORMULAS TO MEMORIZE**

Write these on a card and review 3x before viva:

```
1. CWND doubles every RTT during slow start
   CWND(RTT n) = 2^(n-1) packets

2. CWND increases linearly during congestion avoidance
   CWND_new = CWND_old + MSS²/CWND_old

3. Bandwidth-Delay Product (maximum useful CWND)
   BDP = Bandwidth × RTT

4. Cubic function (window evolution)
   W(t) = C(t - K)³ + W_max

5. Throughput estimate (Mathis formula)
   T ≈ 1.22 × MSS / (RTT × √loss)

6. Loss indicates congestion
   On loss: CWND_new = CWND_old × β  (β≈0.5-0.7)

7. Packet Delivery Ratio
   PDR = Packets_Received / Packets_Sent × 100%
```

---

# **❓ QUICK REFERENCE Q&A**

### **If asked: "Explain slow start"**
> "TCP starts with CWND=1 MSS. Every RTT, CWND doubles (exponential). This quickly finds available bandwidth without overshooting significantly."

### **If asked: "Why decrease CWND on loss?"**
> "Loss signals congestion. TCP must back off immediately. Multiplicative decrease (×0.5) is aggressive enough to reduce load, while gradual additive increase prevents waste."

### **If asked: "Why is Cubic better?"**
> "Cubic uses cubic polynomial growth instead of linear. It reaches bandwidth faster on high-speed links, has lower latency, and causes less packet loss due to smoother probing."

### **If asked: "What's your simulation topology?"**
> "Star topology: 14 clients sending to 1 server over 10 Mbps bottleneck link. Access links are 100 Mbps. This creates 14:1 congestion ratio, forcing algorithms to compete under stress."

---

# **🎬 MENTAL REHEARSAL**

Before bed, visualize:

1. **Tomorrow morning**: Following Ubuntu commands step-by-step
2. **Simulations running**: Three protocol runs (10 mins each)
3. **Data transfer**: Copying files to Windows
4. **Graphs generating**: Professional plots appearing
5. **Report completion**: Data filled into template
6. **Submission**: Confident handoff of complete project

**This mental practice reduces tomorrow's anxiety and improves performance.**

---

# **😴 BEFORE SLEEP**

Do these final checks:

- [ ] Fully charged laptop (for Ubuntu work tomorrow)
- [ ] Internet connection tested (Ubuntu downloads)
- [ ] Project folder backed up (just in case)
- [ ] Notes organized (for tomorrow reference)
- [ ] Alarm set (don't be late!)

---

# **⏰ TIMELINE FOR TOMORROW**

### **Morning (7:00-8:00 AM)**
- Install NS-3 (follow UBUNTU_SETUP.md)
- Build and test

### **Morning (8:00-9:00 AM)**
- Run three simulations
- Verify output files

### **Midday (9:00-9:30 AM)**
- Transfer data to Windows
- Verify metrics files

### **Afternoon (1:00-2:00 PM)**
- Run plotting script
- Review graphs

### **Afternoon (2:00-3:00 PM)**
- Fill template with data
- Write analysis

### **Afternoon (3:00-3:30 PM)**
- Format and proofread
- Submit!

---

# **✅ FINAL CHECKLIST BEFORE SLEEP**

- [ ] Read core sections 1-4 of VIVA_PREPARATION_GUIDE
- [ ] Understand TCP Reno's three phases
- [ ] Understand TCP Cubic's cubic function
- [ ] Know the key differences (5+ points)
- [ ] Reviewed your simulation topology
- [ ] Know the 4 metrics you're measuring
- [ ] Laptop fully charged
- [ ] Tomorrow's plan is clear
- [ ] You feel confident (or at least prepared!)

---

# **💪 YOU'VE GOT THIS**

**Remember**:
- All the hard work (code, theory, setup) is DONE
- Tomorrow is just execution + data insertion
- You're 90% complete before running a single simulation
- This project is at expert level (far beyond average student)
- You know more about TCP than 99% of computer science undergrads

**Confidence**: ★★★★★ (5/5 stars)

---

**Good night! See you tomorrow for the final push! 🚀**

