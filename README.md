---
title: Email Triage Env
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
app_file: inference.py
pinned: false
---

# Email Triage OpenEnv Environment

This project simulates a real-world email triage system where an AI agent:

- Classifies emails (spam, normal, urgent)
- Generates replies
- Handles escalation cases

## Tasks

1. Easy: Spam classification  
2. Medium: Customer complaint reply  
3. Hard: Urgent email handling  

## Features

- OpenEnv compatible environment  
- Reward-based scoring system  
- Multi-task evaluation  
- Dockerized deployment  

## Run

```bash
python inference.py
