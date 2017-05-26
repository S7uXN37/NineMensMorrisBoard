cd ~
rm piscope.tar
sudo rm -rf PISCOPE
wget abyz.co.uk/rpi/pigpio/piscope.tar
tar xvf piscope.tar
cd PISCOPE
make hf
sudo make install
cd ..
rm piscope.tar
