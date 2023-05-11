#!/bin/bash

cat /app/version.txt
python3 /app/src/collector.py --token /secrets/TOKEN --data /storage -vvvv
