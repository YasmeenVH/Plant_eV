# Plant_eV

The Plant_eV library is built for monitoring plant electrical signals in controlled environment agriculture settings. It consists of the hardware setup on a RPi that measures environmental conditions and a NodeMcu which reads the surface electrical potential of a plant. 

# Getting started
## Building the sensor
In the hardware section, a list of sensors and diagrams are available for the wiring of the RPi and the NodeMcu.
### Raspberry PI
The Raspberry Pi monitors environmental variables such as:
- CO2 and Volatile Organic Compounds (CJMCU - 8118) - unit= ppm
- Relative Humidity and Temperature (DHT11) - unit= % and C
- Camera 
- Photoresistor (Qifei) - unit = binary (0 is off 1 is on)

### NodeMcu
The NodeMcu is built to measure a plant's surface potential, it includes:
- Resistance 
- Positive and Negative arm

## Enabling I2C Protocol
The CO2 and VOC sensor needs the I2C protocol to be enabled. Instructions can be found [here](https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/)

## Dowloading the libary 
``` python
git clone https://github.com/YasmeenVH/Plant_eV
cd Plant_eV
pip3 install -e .

# Installing RPi packages
sudo apt-get install dselect && sudo dselect update
sudo dpkg --set-selections < packages.txt
sudo apt-get -u dselect-upgrade

# Installing python requirements
pip3 install -r requirements_good.txt
```


