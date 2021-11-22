import requests
import json
import sensorprocess
from time import sleep

	
def dataprocess(message, sensorinfo):
	altitude = float(message['last_Alt'])
	latitude = float(message['last_Lat'])
	longitude = float(message['last_Lon'])

	acc_x = float(sensorinfo['ACC']['ACC_X'])
	acc_y = float(sensorinfo['ACC']['ACC_Y'])
	acc_x_base = float(sensorinfo['ACC']['ACC_X_BASE'])
	acc_y_base = float(sensorinfo['ACC']['ACC_Y_BASE'])

	moi_base = float(sensorinfo['MOI']['MOI_BASE'])
	moi_value = float(sensorinfo['MOI']['MOI'])

	fle_base = float(sensorinfo['FLEX']['FLEX_BASE'])
	fle_value = float(sensorinfo['FLEX']['FLEX'])

	setid = message['last_SetId']


	acc_status = sensorprocess.accelerometer(acc_x,acc_y)
	moi_status = sensorprocess.moisture(moi_value)
	fle_status = sensorprocess.flex(fle_value)
	zonestatus = sensorprocess.slideindex(acc_status[0],acc_status[1],moi_status,fle_status)


	data_out =[{"measurement": 'logicoutput', "tags":{"LOCID":setid},
			"fields": {"SetId": setid,"Lat": latitude, "Alt": altitude, "Lon": longitude,"ACCX_Status": acc_status[0], "ACCY_Status": acc_status[1], "Moi_Status": moi_status, "Fle_Status": fle_status, "Metric": zonestatus}
				}]

	return data_out

if __name__ == "__main__":

	url = 'http://127.0.0.1:8080/iotpoc' # Rest protocol, flask server url

	while True:

		try:
		
			message = requests.get(url).json()
			sensorinfo = (json.loads(message['last_SensorInfo']))
			
			write_data = dataprocess(message, sensorinfo)

			requests.post(url, json = write_data)
			
			sleep(450)

		except:
			print("Datamanager not responding")
			sleep(2)
