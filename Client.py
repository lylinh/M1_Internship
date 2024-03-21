#################################################################
# data collect: Soil moisture, Light, Tphg, CO2, Water level
# Nutrient level, pH, TDS, Switch 
#################################################################

import time
import socket
import json
from network import WLAN
from pop import SoilMoisture, CO2, Light, WaterLevel, NutrientLevel, Tphg, pH, TDS, Switch

print('finishing import library')

# Setup for wifi address and password
SSID = 'ICTLab Students'
PASSWORD = 'student@ict!@#'

# start connect 
wlan = WLAN(mode=WLAN.STA)
wlan.connect(SSID, auth=(WLAN.WPA2, PASSWORD))
while not wlan.isconnected():
	# wait to connect success wlan
    time.sleep(1)


# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
ip = 'localhost'
port = 8080

print(f'try to connect {ip}:{port}')
# Connect to the server
client_socket.connect((ip,port));

data = "Client connect with server success";

### Initialize object to collect data from sensors
# 1. Soil moisture
soil = SoilMoisture()

#2. Light
light_in = Light(0x5C)
light_out = Light(0x23)

#3. Tphg
tphg = Tphg(0x76) 
	
#4. CO2
co2 = CO2()

#5. Water level
waterlevel = WaterLevel()

#6. Nutrient level
nutrientlevel = NutrientLevel()

#7. pH
ph = pH()

#8. TSD
tds = TDS() 

#9. Switch
switch_up = Switch('P8')
switch_down = Switch('P23')
### Finish initalize

# Send data to server
while True:
	# collect data from sensors once per second
	time.sleep(1)
	data = {}
	
	## 1. Soil moisture
	# get value of soil moisture
	num_soil = soil.read()
	data['num_soil'] = num_soil
	
	## 2. Light
	# get value of light
	l_in = 1 if light_in.read() else 0
	l_out = 1 if light_out.read() else 0
	data['l_in'] = l_in
	data['l_out'] = l_out

	## 3. Tphg
	# get value of temperature and humidity
	temp_value,_,humi_value,_ = tphg.read()
	data['temp_value'] = temp_value
	data['humi_value'] = humi_value
	
	## 4. CO2
	# get value of co2 in air
	num_co2 = co2.read()
	data['num_co2'] = num_co2

	## 5. Water level
	# get value of water tank level: 1 is full, 0 is not full
	watr = 1 if waterlevel.read() else 0
	data['watr'] = watr

	## 6. Nutrient level
	# get value of nutrient tank level: 1 is full, 0 is not full
	nutr = 1 if nutrientlevel.read() else 0
	data['nutr'] = nutr

	## 7. pH
	# get value of ph
	num_ph = ph.read()
	data['num_ph'] = num_ph

	## 8. TSD
	# get value of tsd via ppm (parts per million) and ec (specific conductance)
	pmm_tsd = tds.readPPM()
	ec_tsd = tds.readEC()
	data['pmm_tsd'] = pmm_tsd
	data['ec_tsd'] = ec_tsd

	## 9. Switch
	# current switch value which value: 1 is on, 0 is off
	v_su = 1 if switch_up.read() else 0
	v_sd = 1 if switch_down.read() else 0
	data['v_su'] = v_su
	data['v_sd'] = v_sd

	print(data)

	# send data were collected to server
	client_socket.send(json.dumps(data).encode());
