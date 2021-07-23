from software.Plant_eV.env_conditions import Sensors
import time
import os.path

def sensors_test():

	S = Sensors()
	#Testing RH and  temperature sensor
	try:
	    rh, temp = S.rh_temp()
	except (RuntimeError, TypeError, NameError):
	    print("Temperature and humidity sensor is not functional")
	else:
	    if temp and rh is not None or temp and rh !=0:
	      print("Temperature and humidity sensor is functional and working properly.")
	      print("Temperature:",temp)
	      print("Humidity:",rh)
	    else:
	      print("Temperature and humidity sensor is functional, but not working properly.")
	      print("Temperature:",temp)
	      print("Humidity:",rh)

	#Testing CO2 and VOC sensor
	try:
	    co2, voc = S.gas()
	except (RuntimeError, TypeError, NameError):
	    print("CO2 and VOC sensor is not functional")
	else:
	    if co2 and voc is not None or co2 and voc !=0:
	      print("CO2 and VOC sensor is functional and working properly.")
	      print("CO2:",co2)
	      print("VOC:",voc)
	    else:
	      print("CO2 and VO sensor is functional, but not working properly.")
	      print("CO2:",co2)
	      print("VOC:",voc)

	#Testing light sensor
	try:
	    light = S.light_intensity()
	except (RuntimeError, TypeError, NameError):
	    print("Light sensor is not functional")
	else:
	    if light is not None:
	      print("Light sensor is functional and working properly.")
	      if light == 1:
	        print("Light is on")
	      else:
	        print("light is off")
	    else:
	      print("Temperature and humidity sensor is functional, but not working properly.")

	#Testing camera
	p = S.picture()
	#print(p)
	return

if __name__ == '__main__':
	sensors_test()
