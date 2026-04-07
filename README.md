---

title: Email Triage AI Environment
emoji: 📧
colorFrom: blue
colorTo: purple
sdk: docker
app_file: inference.py
pinned: false
-------------

# 📧 Email Triage OpenEnv Environment

## 🚀 Overview

This project simulates a **real-world email triage system** where an AI agent processes incoming emails and performs tasks such as:

* 📩 Classifying emails (spam, normal, urgent)
* ✍️ Generating intelligent replies
* ⚠️ Escalating critical issues

It is designed as a **complete OpenEnv-compatible environment** for training and evaluating AI agents.

---

## 🎯 Motivation

Email management is a real-world problem faced by:

* Customer support teams
* Businesses handling large volumes of communication
* Automated AI assistants

This environment provides a **realistic simulation** for evaluating agent intelligence in such scenarios.

---

## 🧠 Tasks & Difficulty Levels

### 🟢 Easy Task

* Classify spam emails
* Objective: Correct classification
* Reward: Binary (0 or 1)

---

### 🟡 Medium Task

* Generate customer support replies
* Objective: Helpful and polite response
* Reward: Partial scoring based on keywords

---

### 🔴 Hard Task

* Handle urgent emails
* Multi-step reasoning:

  * Classify urgency
  * Respond appropriately
  * Escalate if needed

---

## 🏅 Reward Design

* Continuous reward system (0.0 → 1.0)
* Partial credit for progress
* Penalties for incorrect actions
* Encourages realistic agent behavior

---

## ⚙️ Environment API

Implements full OpenEnv specification:

* `reset()` → Initializes environment
* `step(action)` → Executes action
* `state()` → Returns current state

---

## 📦 Project Structure

```
email_env/
├── data/
├── env/
├── models/
├── inference.py
├── Dockerfile
├── openenv.yaml
├── README.md
```

---

## 🧪 Baseline Agent

* Uses LLM-based inference
* Produces reproducible results
* Example Output:

```
Baseline Score: 1.0
```

---

## 🐳 Docker Support

Fully containerized environment:

```
docker build -t email-env .
docker run email-env
```

---

## 🌍 Real-World Impact

This environment can be used for:

* AI customer support automation
* Email classification systems
* Reinforcement learning research
* LLM evaluation benchmarks

---

## 🏁 Conclusion

This project provides a **practical, scalable, and realistic AI environment** that aligns with real-world applications and OpenEnv standards.

---
