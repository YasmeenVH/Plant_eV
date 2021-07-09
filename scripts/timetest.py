from Plant_eV.env_conditions import Sensors
import time

def time_test():
	start = time.time()
	S = Sensors() 
	light = S.light_intensity()
	co2, voc = S.gas()
	rh, temp = S.rh_temp()
	p = S.picture()
	diff = time.time() - start
	return print("time to collect:", diff)

if __name__ == '__main__':
	time_test()

		
