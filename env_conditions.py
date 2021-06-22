#IMPORTS
import h5py
import sys
import Adafruit_DHT
import time
from time import sleep
import datetime
import busio
import board 
import adafruit_ccs811
from picamera import PiCamera
import numpy as np
import os.path
from os import path 
import pandas as pd
import RPi.GPIO as GPIO

class Sensors(object):
	def hdf5_exist(self,root):
		# Check if file exists and have it in write option

		if os.path.exists(root+'rpi1_env_data.h5'):
			f = pd.read_hdf(root+'rpi1_env_data.h5',mode = 'a')
		else:
		# Create file if this it doesn't exist

			df = pd.DataFrame(columns=['time','co2','voc','rh','temp'])
			f = pd.HDFStore(root+'rpi1_env_data.h5')
			f.append('rp1',df)

		return f

	def create_Folder(self, directory):
		try:
			if not os.path.existis(directory):
				os.makedirs(directory):
			except OSError:
				print('Error making directory: ' + directory)


	def picture(self,root):				
		camera = PiCamera()
		day = time.time() 
		camera.start_preview()
		camera.capture(
		sleep(1)
		camera.stop_preview()

	def gas(self):
		i2c_bus = busio.I2C(board.SCL, board.SDA)
		ccs811 = adafruit_ccs811.CCS811(i2c_bus)
		co2 = ccs811.eco2	# results in ppm
		voc = ccs811.tvoc      # results in ppm

		return co2, voc

	def rh_temp(self):
		DHT_SENSOR = Adafruit_DHT.DHT11 
		DHT_PIN = 21 	
		humidity, temperature = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)

		return humidity, temperature

	def light_intensity(self):
		GPIO.setmode(GPIO.BCM)
		light_pin = 17
		# Output setup (trying for analog readings)
		GPIO.setup(light_pin,GPIO.OUT)
		GPIO.output(light_pin,GPIO.LOW)
		time.sleep(0.1)
		count = 0
		# Back to input
		GPIO.setup(light_pin, GPIO.IN)
		while (GPIO.input(light_pin) == GPIO.LOW)
			count += 1
		
		return count
				
def main():
# Sensor activating
	time_id = time.time()
	root = '/home/pi/sensors/' # define root
	data = pd.DataFrame({'time':time_id,'co2':sensors.gas()[0],'voc'sensors.gas()[1],'rh':,'temp':})
	## add to hdf5
	# Whats up jerome ici c'est ma branche
	# whats up	 		
if __name__ == '__main__':
	main()
