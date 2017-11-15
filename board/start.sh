#!/bin/bash
DATE=$(date +"%Y-%m-%d-%H-%M")
cd /home/pi/nine-mens-morris/board
exec > logs/$DATE.log
sudo pkill -f "python3 mills.py"
python3 mills.py
if [ $? = 1 ]; then
    sudo shutdown 5
fi
