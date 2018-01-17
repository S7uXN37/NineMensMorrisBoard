#!/bin/bash
DATE=$(date +"%Y-%m-%d--%H_%M_%S")
cd /home/pi/nine-mens-morris/board
sudo pkill -f "python3 mills.py"
python3 mills.py > logs/$DATE.log
if [ $? = 1 ]; then
    sudo shutdown 0
fi
