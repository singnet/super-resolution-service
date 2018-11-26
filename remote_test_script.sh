#!/usr/bin/env bash

kill -- -1 && sleep 0.5s
git pull && sleep 1.5s
python3.6 run_service.py &
sleep 2s
python3.6 test_service.py
