#####
'''Normalisation Method to find the Landslide Index'''
###

# 0= green, 1=amber, 2= red #

ACC_MIN = 265 		# Minimum Accelerometer sensor value (ADC Output Value)
ACC_MAX = 415		# Maximum Accelerometer sensor value (ADC Output Value)

MOI_MIN = 200		# Minimum Moisture sensor value (ADC Output Value)
MOI_MAX = 700		# Maximum Moisture sensor value (ADC Output Value)

FLE_MIN = 200		# Minimum Flex sensor value (ADC Output Value)
FLE_MAX = 700		# Maximum Flex sensor value (ADC Output Value)


def accelerometer(ACC_X, ACC_Y):
	# Normalisation converts [265,415] to [-1,1] and takes absoulute function to convert to [0,1]
	# [0,1] is used to get absolutes of [-90,90]
	# -60 degree = 290(ADC) || 60 degree = 390(ADC) || -30 degree = 315(ADC) || 30 degree = 365(ADC)
	# 60 degree Red threshold = 0.6666 || 30 degree Amber threshold = 0.333

	accnormx = abs((((ACC_X-ACC_MIN)/(ACC_MAX-ACC_MIN))*2)-1) 
	accnormy = abs((((ACC_Y-ACC_MIN)/(ACC_MAX-ACC_MIN))*2)-1)
	
	return [accnormx, accnormy]


def moisture(MOI_VALUE):
	# Normalisation of [700,200] to [0,1]
	# 700(ADC) = Dry || 200(ADC) = Wet
	# Red Threshold (>65%) = 0.65 || Amber Threshold (45% to 65%) = 0.45 to 0.65
	moinorm = 1-((MOI_VALUE - MOI_MIN)/(MOI_MAX - MOI_MIN))
	
	return moinorm


def flex(FLE_VALUE):
	# Normalisation of [200,700] to [0,1]
	# 
	# Red Threshold (>65%) = 0.65 || Amber Threshold (45% to 65%) = 0.45 to 0.65
	flenorm = (FLE_VALUE - FLE_MIN)/(FLE_MAX - FLE_MIN)
	
	return flenorm


def slideindex(acc_normx, acc_normy, moi_norm, fle_norm):
	# Calculation of Landslide Index
	# Accelerometer Reading Weightage = 0.3
	# Moisture Reading Weightage = 0.22
	# Flex Reading Weightage = 0.18
	# Red Threshold = 0.6 || Amber Threshold = 0.35
	indexnorm = 0.3*(acc_normx + acc_normy) + (0.22*moi_norm) + (0.18*fle_norm)
	
	return indexnorm

	
	

if __name__ == "__main__":
	accelerometer_status = accelerometer(390,390)
	print("Zone accelerometer status: ", accelerometer_status)
	moisture_status = moisture(550)
	print("Zone moisture status: ", moisture_status)
	flex_status = flex(450)
	landsildeindex = slideindex(accelerometer_status[0], accelerometer_status[1], moisture_status, flex_status)
	print("Landslide Index: ", landsildeindex)
	


	
