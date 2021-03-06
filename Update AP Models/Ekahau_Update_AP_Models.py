#!/usr/bin/env python3
'''------------------------------------------------------------------
    Filename:   Ekahau_Update_AP_Models.py
    author:     Haydn Andrews 
    date:       14/04/2021 
    desc:       Will Update AP models in Ekahau. I use this
    			when i have surveys using external antennas
    			done with 3700/ 2800 series where the 
    			customer then change mind to 9100 series
    			and i need to import the Ekahau plan to DNA-C
    			or Prime

    			Thanks to François Vergès (@VergesFrancois) who 
    			developed the script that i used as the base build
    			of this script that I used to develop this:
    			https://github.com/francoisverges/semfio-ekahau

    modification history:
    what    when            who     why
    v1.0    14/04/2021      HA      Initial version
-------------------------------------------------------------------'''

import zipfile
import os
import csv
import json
import sys
import shutil
import re

# Get current working directory
working_directory = os.getcwd()
#print(working_directory)

# Get project file name passed into script by user
filename = input('Project file: ')
#print (filename)

# The project name, filename remove the extension (last 4x characters)
project_name = filename[:-4]
#print(project_name)

# Unzip the .esx project file into foler named "project_name"
with zipfile.ZipFile(filename,'r') as zip_ref:
	zip_ref.extractall(project_name)

# Read the accessPoints.json file
with open(working_directory + '/' + project_name + '/accessPoints.json', 'r') as file :
	accessPoints = json.load(file)

# Read CSV as Dictionary
# This CSV file needs to be local to the Python script
try:
	with open('old_models.csv', 'r', encoding='utf-8-sig') as csv_file:
		reader = csv.DictReader(csv_file)
		csv_data = [record for record in reader]
except Exception as e:
	print(e)
	sys.exit()

def find_AP_by_name(old_model: str, csv_data: dict):
	new_model = old_model
	for entry in csv_data:
		if entry['old_ap_model'] == old_model:
			new_model = entry['new_ap_model']
	return new_model	

for ap in accessPoints['accessPoints']:
	old_ap_model = ap['model']
	new_ap_model = find_AP_by_name(ap['model'], csv_data)
	ap['model'] = new_ap_model
	if old_ap_model != new_ap_model:
		print(old_ap_model, 'replaced with', new_ap_model)
#	if old_ap_name == new_ap_name:
#		print(old_ap_name, 'left unchanged')

try:	
	with open(working_directory + '/' + project_name + '/accessPoints.json', 'w') as file:
		json.dump(accessPoints, file, indent=4)

except Exception as e:
	print(e)

new_file_name = project_name + '_re-zip'

try:
	shutil.make_archive(new_file_name, 'zip', project_name)
	shutil.move(new_file_name + '.zip', new_file_name + '.esx')
	shutil.rmtree(project_name)
except Exception as e:
	print(e)