# Plant_eV

The Plant_eV library is built for monitoring plant electrical signals in controlled environment agriculture settings. It consists of the hardware setup on a RPi that measures environmental conditions and a NodeMcu which reads the surface electrical potential of a plant. 

# Getting started
## 1. Building the sensor
In the hardware section, a list of sensors and diagrams are available for the wiring of the RPi and the NodeMcu.
### 1.1 Raspberry PI
The Raspberry Pi monitors environmental variables such as:
- CO2 and Volatile Organic Compounds (CJMCU - 8118) - unit= ppm
- Relative Humidity and Temperature (DHT11) - unit= % and C
- Camera 
- Photoresistor (Qifei) - unit = binary (0 is off 1 is on)
#### 1.1.1 CO2 and VOC sensor - Enabling I2C Protocol
The I2C protocol needs to be enabled for the CO2 and VOC sensor to work. 

The first step is to enable the IC2 port.
```python
sudo raspi-config
```
- Select interface option 
- Enable IC2 port
```python
sudo reboot
```
More detailed information can be found [here](https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/)

The second step is to deal with potential IC2 clock stretching problems.
```python
sudo nano /boot/config.txt
```
```python
# Uncomment some or all of these to enable the optional hardware interfaces
dtparam=i2c_arm=on
dtparam=i2s=on
dtparam=spi=on
```
```python
# Clock stretching by slowing down to 10KHz
dtparam=i2c_arm_baudrate=10000
```
Next, save the file and exit (in Nano, press Ctrl-O, Enter, then press Ctrl-X)
```python
sudo reboot
```
More detailed information can be found [here](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/i2c-clock-stretching)

Finally, it is possible to test the hardware. 
```python
sudo i2cdetect -y 1
```
Make sure that devices are connected to adresses 0x40 and ax50. If not, check the wiring of the Raspberry Pi and make sure that the previous procedures have been done correctly. 
#### 1.1.2 Enabling Camera
```python
sudo raspi-config
```
- Select interface option 
- Enable Camera
```python
sudo reboot
```

### 1.2 NodeMcu
The NodeMcu is built to measure a plant's surface potential, it includes:
- Resistance 
- Positive and Negative arm

## 2. Dowloading the libary 
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


