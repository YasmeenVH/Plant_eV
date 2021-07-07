# Plant_eV

The Plant_eV library is built for monitoring plant electrical signals in controlled environment agriculture settings. It consists of the hardware setup on a RPi that measures environmental conditions and a NodeMcu which reads the surface electrical potential of a plant. 

# Getting started
## Building the sensor
In the hardware section, a list of sensors and diagrams are available for the wiring of the RPi and the NodeMcu.

## Dowloading the libary 
``` python
git clone https://github.com/YasmeenVH/Plant_eV
cd Plant_eV
pip install -e .

cd ..
# Installing RPi packages
sudo apt-get install dselect && sudo dselect update
sudo dpkg --set-selections < packages.txt
sudo apt-get -u dselect-upgrade

# Installing python requirements
pip install -r requirements.txt
```


