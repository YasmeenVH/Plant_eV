from Plant_eV.env_conditions import Sensors
import paho.mqtt.client as mqtt
import pandas as pd
from pandas import HDFStore

class DataLoader(object):
	def __init__(self):
		self.s = Sensors()
		self.client = mqtt.Client()
		self.hdf = HDFStore('hdf_file.h5')

	def on_message(client,userdata, msg):
    		topic=msg.topic
    		m_decode=str(msg.payload.decode("utf-8","ignore"))
    		message_handler(client,m_decode,topic)
    		#print("message received")

	def message_handler(client,msg,topic):
	    	data=dict()
    		tnow=time.localtime(time.time())
    		try:
       			msg=json.loads(msg)#convert to Javascript before saving
       			#print("json data")
    		except:
        		pass
        		#print("not already json")
    		data["time"]=tnow
    		data["topic"]=topic
    		data["message"]=msg

    		if command.options["storechangesonly"]:
        		if has_changed(client,topic,msg):
            			client.q.put(data) #put messages on queue
    		else:
        		client.q.put(data) #put messages on queue

	def has_changed(topic,msg):
    		topic2=topic.lower()
    		if topic2.find("control")!=-1:
        		return False

    		if topic in last_message:
        		if last_message[topic]==msg:
            			return False
    		last_message[topic]=msg
    		return True

	def log_worker():
    		"""runs in own thread to log data"""
    		while Log_worker_flag:
        		while not q.empty():
            			results = q.get()
            			if results is None:
                			continue
            			log.log_json(results)
            			#print("message saved ",results["message"])
    		log.close_file()	
