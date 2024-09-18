#!/bin/bash
rm res.csv
for i in {1..29}
do
  echo "Run $i:"
  python test.py
  #ps aux | grep python | grep -v grep | awk '{print $2}'
  #PYTHON_PID=$(pgrep -f python)
  #ps -p $PYTHON_PID -o %cpu,%mem
  echo "-------------------------"
done
