#!/bin/bash
cd /home/pi/nine-mens-morris/board
sudo pkill -f "python3 mills.py"
python3 mills.py
cd /
