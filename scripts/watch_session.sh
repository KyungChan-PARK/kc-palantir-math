#!/bin/bash
# Real-time session monitoring

while true; do
    clear
    python3 scripts/monitor_session.py
    sleep 5
done

