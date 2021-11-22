# MQTT Subscriber
# Read data from MQTT Broker, preprocess it and send to DataManager Module through REST Protocol

import paho.mqtt.client as paho
import sys
import json
import requests


# The callback for when the client receives a CONNACK response from the server.
def onconnect(client, userdata, flags, rc):
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("sensor")
    

#Function to Read data from broker
url = 'http://127.0.0.1:8080/iotpoc' # Rest protocol, flask server url

def onmessage(client, userdata, msg):
	message=msg.payload.decode("utf-8","ignore")
	#print(message)	
	data = payload_handler(message)
	try:
		requests.post(url, json = data)
	except:
		print("Datamanager not responding")
	#print("SUCCESS")


# Data Preprocessor
def payload_handler(jsonData):
		json_Dict=json.loads(jsonData)
		setid=json_Dict['SetId']
		latitude=(json_Dict['Position']['Lat'])
		longitude=(json_Dict['Position']['Lon'])
		altitude=(json_Dict['Position']['Alt'])
		datetime=json_Dict['DateTime']
		sensorinfo=json.dumps((json_Dict['SensorInfo']))
		
		#data preparation to send to influx
		data_out =[{"measurement": "sensordata",
			"fields": {"SetId": setid,"Lat": latitude, "Lon": longitude, "Alt": altitude, "SensorInfo": sensorinfo},
			"time": datetime}]
		
		return data_out


if __name__ == "__main__":

	#creating MQTT client object

	client=paho.Client()
	client.on_connect=onconnect
	client.on_message=onmessage


	if client.connect("localhost", 1883, 60)!=0:
		print("could not connect")
		sys.exit(-1)


	try:
		client.loop_forever()
	except:
		print("dissconect")

	client.disconnect()
