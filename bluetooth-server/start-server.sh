#!/bin/bash
sudo hciconfig hci0 up
sudo hciconfig hci0 name 'RaspberryPi'
sudo hciconfig hci0 piscan
echo 'Bluetooth enabled, device discoverable'
echo 'Starting server...'
sudo python rfcomm-server.py
