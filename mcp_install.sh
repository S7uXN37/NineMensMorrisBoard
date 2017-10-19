sudo apt-get update
sudo apt-get install build-essential python3-dev python3-smbus git
cd ~
git clone https://github.com/adafruit/Adafruit_Python_MCP3008.git
cd Adafruit_Python_MCP3008
sudo python3 setup.py install
