#IMPORTS
import h5py
import sys
import Adafruit_DHT
import time
from time import sleep
from datetime import datetime
from datetime import date
#import datetime
import busio
import board
import adafruit_ccs811
from picamera import PiCamera
import numpy as np
import os.path
from os import path
import pandas as pd
import RPi.GPIO as GPIO


PATH = 'home/pi/Pictures/Plant_eV/'

def check_day(t1,t2):
	print("what type is this",type(t1.day()))
	if t1.day() == t2.day():
		day_root = t1.strftime("%Y%m%d")
		return day_root
	else:
		return t2.strftime("%Y%m%d")

class Sensors(object):
	def __init__(self, path = PATH):
		self.path = path
		self.timestamp = datetime.now()

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
			if not os.path.exists(directory):
				os.makedirs(directory)

		except OSError:

                        print('Error making directory: ',directory)


	def picture(self):
		t = datetime.now()
		#tday = t.day()
		print('what type is t1',t.day)
		print("t1,t2",t,self.timestamp)
		day_root = check_day(t,self.timestamp)
		self.timestamp = t
		camera = PiCamera()
		day = int(time.time())
		camera.start_preview()
		camera.capture(self.root+day_root+'/'+str(int(day))+'.jpg')
		sleep(.2)
		camera.stop_preview()
		
	def gas(self):
		i2c_bus = busio.I2C(board.SCL, board.SDA)
		ccs811 = adafruit_ccs811.CCS811(i2c_bus)
		co2 = ccs811.eco2	     # results in ppm
		voc = ccs811.tvoc      # results in ppm

		return co2, voc

	def rh_temp(self):
		DHT_SENSOR = Adafruit_DHT.DHT11
		DHT_PIN = 21
		humidity, temperature = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)

		return humidity, temperature

	def light_intensity(self):
		#GPIO.setmode(GPIO.BCM)
		light_pin = 17
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(light_pin,GPIO.IN)
		GPIO.setwarnings(True)
		b = GPIO.input(light_pin)
		# Output setup (trying for analog readings)
		#GPIO.setup(light_pin,GPIO.OUT)
		#GPIO.output(light_pin,False) #GPIO.LOW)
		time.sleep(0.1)
		#count = 0
		# Back to input

		#GPIO.setup(light_pin, GPIO.IN)
		#while (GPIO.input(light_pin) == GPIO.LOW):
		#	count += 1
		#GPIO.input()
		return b # count


def main():
# Sensor activating
	S = Sensors()
	print("what is this",datetime.now().day)
	#root = "/home/pi/sensors/"	 # define root
	time_id = time.time()
	#root = '/home/pi/sensors/' # define root
	#data = pd.DataFrame({'time':time_id,'co2':S.gas()[0],'voc':S.gas()[1],'rh':S.rh_temp()[0],'temp':S.rh_temp()[1]})
	## add to hdf5
	S.picture()
	print('temp',S.rh_temp()[1],'humidity',S.rh_temp()[0])
	co2 = S.gas()[0]
	voc = S.gas()[1]
	light = S.light_intensity()
	#time_id = time.time()
	#root = '/home/pi/sensors/' # define root
	#data = pd.DataFrame({'time':time_id,'co2':S.gas()[0],'voc':S.gas()[1],'rh':S.rh_temp()[0],'temp':S.rh_temp()[1]})
	## add to hdf5
	print(co2,"what is co2")
	print(voc,"what is voc")
	print(time_id)
	print(light, "what is light")


if __name__ == '__main__':
	main()
