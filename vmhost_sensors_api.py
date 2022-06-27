#!/usr/bin/env python3 

from typing import Optional
from fastapi import FastAPI

import subprocess
import uvicorn

api = FastAPI()
VERSION = '1.0.1'

def _get_sensors_v1():
	sensors = subprocess.run(['sensors'], stdout=subprocess.PIPE, encoding='utf-8')
	temp = {
	'default': 'k10temp-pci-00c3',
	'layout': 'by_adapter',
	'version': VERSION,
	'data': {}
	}
	sensors_readout = sensors.stdout.splitlines(True)
	key = None
	for i,line in enumerate(sensors_readout):
		line = [_.strip() for _ in line.split(':')]		
		if line[0] != '':
			if 'Adapter' in line[0]:
				key = sensors_readout[i-1].strip()
				temp['data'][key] = {}

			if 'Adapter' not in line[0] and len(line) > 1: 
				temp['data'][key][line[0]] = line[1]

	return temp

def _get_sensors_v2():
	sensors = subprocess.run(['sensors'], stdout=subprocess.PIPE, encoding='utf-8')
	temp = {
	'default': 'Temps',
	'layout': 'by_measurement_type',
	'version': VERSION,
	'data': {
		'Temps': {},
		'Fans': {},
		'Voltages': {}
		}
	}
	sensors_readout = sensors.stdout.splitlines(True)
	for i,line in enumerate(sensors_readout):
		line = [_.strip() for _ in line.split(':')]		
		if len(line) > 1:
			if 'RPM' in line[1]:
				temp['data']['Fans'][line[0]] = line[1]
			elif 'V' in line[1]:
				temp['data']['Voltages'][line[0]] = line[1]
			elif '°C' in line[1]:
				temp['data']['Temps'][line[0]] = line[1]
	return temp

@api.get("/")
def sensors_output():
	sensors = subprocess.Popen(['sensors'], stdout=subprocess.PIPE)
	grep_temp = subprocess.run(['grep', '°C'], stdin=sensors.stdout, stdout=subprocess.PIPE, encoding='utf-8')
	temp = {}

	for line in grep_temp.stdout.splitlines(True):
		line = [_.strip() for _ in line.split(':')]
		if len(line) > 1: temp[line[0]] = line[1]
	return temp

@api.get("/v1")
def sensors_output():
	return _get_sensors_v1()



@api.get("/v2")
def sensors_output():
	return _get_sensors_v2()

if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8004, log_level="error")
