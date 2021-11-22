from Rcfalgorithm import rcfalgorithm
import xlrd
import requests
import numpy as np
from time import sleep
from sklearn.ensemble import IsolationForest
from math import isnan


if __name__ == "__main__":

	work=xlrd.open_workbook("rcfdata.xls")
	worksheet=work.sheet_by_index(0)
	url = 'http://127.0.0.1:8080/iotpoc'

	battery_data = np.array([])
	battery_np = np.array([])
	hvac_cur_data = [] # hvac total power consumption
	hvac_cmp_data = [] #hvac compressor power consumption data
	hvac_air_data = [] # air temperature delta
	hvac_air_flow = [] # air flow data

	faultstatus = [0.9, 0.9, 0.9, 0.9, 0.9]

	while True:
		for i in range(1,100):
############################################# Compressor Power Consumption [0] ##############################################
			datapoint = worksheet.cell_value(i,3)
			hvac_cmp_data.append(datapoint)

			if len(hvac_cmp_data)>100:
				del hvac_cmp_data[0]
					
			anomaly = rcfalgorithm(hvac_cmp_data, 10)

			anomalyround = anomaly

			if anomaly > 50:
				anomalyround = 50.0

			if anomaly > 30:
				hvac_cmp_data.pop()
				faultstatus[0] = 0.2
				

			anomalyinvert = 52.0-anomalyround

			data_write = [{"measurement": "hvaccompressor","fields": {"current": datapoint,"hvacanomaly": anomaly, "anomalyround": anomalyround, "hvacstatus": anomalyinvert,"faultstatus": faultstatus[0]}}]

			sleep(1)		

			try:		
				x = requests.post(url, json = data_write)
			except:	
				print("Datamanager not responding")	
				sleep(2)

			

################################################### Total Power Consumption [1]###########################################
			datapoint = worksheet.cell_value(i,0) 
			hvac_cur_data.append(datapoint)

			if len(hvac_cur_data)>100:
				del hvac_cur_data[0]
					
			anomaly = rcfalgorithm(hvac_cur_data, 10)

			anomalyround = anomaly

			if anomaly > 50:
				anomalyround = 50.0

			if anomaly > 30:
				hvac_cur_data.pop()
				faultstatus[1] = 0.2
				

			anomalyinvert = 52.0-anomalyround

			data_write = [{"measurement": "hvaccurrent","fields": {"current": datapoint,"hvacanomaly": anomaly, "anomalyround": anomalyround, "hvacstatus": anomalyinvert,"faultstatus": faultstatus[1]}}]


			sleep(1)		

			try:		
				x = requests.post(url, json = data_write)
			except:	
				print("Datamanager not responding")	
				sleep(2)

			

################################################### Air Delta Temperature [2]########################################
			datapoint = worksheet.cell_value(i,4)
			hvac_air_data.append(datapoint)
					
			if len(hvac_air_data)>100:
				del hvac_air_data[0]
					
			anomaly = rcfalgorithm(hvac_air_data, 10)

			anomalyround = anomaly

			if anomaly > 50:
				anomalyround = 50.0


			if anomaly > 30:
				hvac_air_data.pop()
				faultstatus[2] = 0.2

			anomalyinvert = 52.0-anomalyround

			data_write = [{"measurement": "hvacairtemp","fields": {"airtemp": datapoint,"hvacanomaly": anomaly, "anomalyround": anomalyround, "hvacstatus": anomalyinvert,"faultstatus": faultstatus[2]}}]


			if anomaly > 30:
				hvac_air_data.pop()

			sleep(1)		

			try:		
				x = requests.post(url, json = data_write)
			except:	
				print("Datamanager not responding")	
				sleep(2)

####################################################### Battery Data [4]####################################

			datapoint = worksheet.cell_value(i,2)
			battery_data = np.append(battery_data, datapoint)
			#battery_cond(datapoint)

			if len(battery_data)>100:
				battery_data = battery_data[1:]
			
			battery_np = battery_data.reshape(-1,1)
			
			model = IsolationForest(n_estimators =100, max_samples ='auto',contamination=float(0.2),max_features=1.0)
			model.fit(battery_np)
			anomalylist = model.decision_function(battery_np)

			anomaly = list(anomalylist).pop()

			
			if isnan(anomaly):
				anomaly = 0.0

			anomalyround = anomaly + 1.0

			anomalyinvert = 2.0 - anomalyround

			if anomaly < -0.3:
				battery_data = battery_data[:-1]
				faultstatus[4] = 0.2


			data_write = [{"measurement": "battery","fields": {"volatge": datapoint,"batteryanomaly": anomaly, "anomalyround": anomalyround, "batterystatus": anomalyinvert,"faultstatus": faultstatus[4]}}]
			

			sleep(1)		

			try:		
				x = requests.post(url, json = data_write)
			except:	
				print("Datamanager not responding")	
				sleep(2)
			sleep(438)
################################################## HVAC AIR FLOW [3]#########################################
'''
			datapoint = worksheet.cell_value(i,1)
			hvac_air_flow.append(datapoint)
					
			if len(hvac_air_flow)>100:
				del hvac_air_flow[0]
					
			anomaly = rcfalgorithm(hvac_air_flow, 10)

			anomalyround = anomaly

			if anomaly > 50:
				anomalyround = 50.0


			if anomaly > 30:
				#hvac_air_flow.pop()
				faultstatus[3] = 0.2

			anomalyinvert = 52.0-anomalyround

			data_write = [{"measurement": "hvacairflow","fields": {"airflowp": datapoint,"hvacanomaly": anomaly, "anomalyround": anomalyround, "hvacstatus": anomalyinvert,"faultstatus": faultstatus[3]}}]


			if anomaly > 30:
				hvac_air_data.pop()

			sleep(1)		

			try:		
				x = requests.post(url, json = data_write)
			except:	
				print("Datamanager not responding")	
				sleep(2)
'''
