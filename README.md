# ⚖️ Weighted Fair Queueing (WFQ) UDP Server — Python Implementation

## 📌 Overview

This project implements a **Weighted Fair Queueing (WFQ) packet scheduling server** using UDP sockets in Python. The server fairly distributes bandwidth among multiple client flows based on assigned weights using **Virtual Finish Time (VFT) scheduling**.

UDP clients generate traffic to the server, and packets are scheduled according to WFQ principles to ensure proportional fairness and work-conserving behavior under congestion.

Developed as part of a Communication Networks assignment on packet scheduling and fairness.

---

## 🎯 Features

- UDP multi-flow server
- Weighted Fair Queueing (WFQ) scheduler
- Per-packet Virtual Finish Time (VFT) computation
- Min-heap priority queue ordered by VFT
- Port-based flow identification
- Configurable per-flow weights
- Configurable server capacity (packets/sec)
- Finite buffer with WFQ-aware drop policy
- Echo reply to clients
- Per-flow throughput measurement

---

## ⚙️ WFQ Scheduling Logic

Each arriving packet is assigned a **Virtual Finish Time (VFT)**:

```
VFT_i = max(VT, VFT_last_flow) + (1 / (C × W_i))
```

Where:

- VT = system virtual time
- VFT_last_flow = last finish time of that flow
- C = server capacity (packets/sec)
- W_i = weight of the flow

---

## 📦 Scheduling Behavior

- All packets stored in a single priority queue
- Queue ordered by increasing VFT
- Packet with smallest VFT served first
- Server is:
  - Non-preemptive
  - Work-conserving
- Virtual time updated when packets are served

---

## 🧱 Buffer Policy

When buffer is full:

- Packet with **largest VFT** is dropped
- New packet replaces it only if it has smaller VFT
- Preserves weighted fairness under congestion

---

## 🗂 Project Structure

```
.
├── server.py
├── client1.py
├── report.pdf
├── ee5150-assignment-3-wfq.pdf
└── README.md
```

- `server.py` — WFQ UDP scheduling server
- `client1.py` — Traffic generator client
- `ee21b068_report.pdf` — Implementation + performance report
- `ee5150-assignment-3-wfq.pdf` — Assignment specification

---

## 📝 Note on Client Script

This repository includes a single client script:

```
client1.py
```

During the original assignment, multiple client files were used to simulate different flows with different port numbers and sending rates. Since those scripts were functionally identical and differed only in configuration values, only one representative client implementation is included here to avoid duplication.

Multiple flows can still be simulated by running this client script with modified port and rate parameters.

---

## 🔧 Configuration

Edit parameters inside `server.py`:

```
SERVER_PORT
FLOW_PORTS
FLOW_WEIGHTS
CAPACITY
BUFFER_SIZE
```

Example:

```
Capacity = 10 packets/sec
Weights = {5001:1, 5002:2, 5003:4}
Buffer Size = 10 packets
```

---

## 🚀 How to Run

### Step 1 — Start WFQ Server

```
python server.py
```

---

### Step 2 — Start Client

```
python client1.py
```

Run multiple instances with different ports/rates (if configurable) to simulate multiple flows.

---

## 📊 Performance Results

| Capacity | Weights | Buffer | Client Rates | Throughput |
|------------|------------|-----------|----------------|----------------|
| 10 | 1:1:1 | 10 | 10:10:10 | 3.33:3.33:3.33 |
| 10 | 1:1:1 | 10 | 10:20:40 | 3.33:3.33:3.33 |
| 10 | 1:2:4 | 10 | 10:10:10 | 1.43:2.86:5.70 |
| 20 | 1:2:4 | 100 | 10:10:10 | 3.40:6.80:9.80 |

Small deviations occur due to OS timing and sleep interval granularity.

---

## 🧠 Concepts Demonstrated

- Weighted Fair Queueing (WFQ)
- Virtual Finish Time scheduling
- Fair bandwidth allocation
- Multi-flow packet scheduling
- Congestion buffer management
- UDP socket programming
- Priority queue scheduling
- Traffic fairness control

---

## 🛠 Requirements

- Python 3.x
- Standard library only
- No external dependencies

---

## 📘 Academic Context

Course: Communication Networks  
Topic: Packet Scheduling and Fair Queueing  

Includes:

- WFQ server implementation
- Multi-flow traffic scheduling
- Virtual time based fairness
- Throughput evaluation

---

## 📜 License

MIT License — free for learning and experimentation.
