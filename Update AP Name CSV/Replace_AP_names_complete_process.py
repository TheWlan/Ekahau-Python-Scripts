#!/usr/bin/env python3

import zipfile
import os
import csv
import json
import sys
import shutil

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
	with open('old_new_names.csv', 'r', encoding='utf-8-sig') as csv_file:
		reader = csv.DictReader(csv_file)
		csv_data = [record for record in reader]
except Exception as e:
	print(e)
	sys.exit()


def find_AP_by_name(old_name: str, csv_data: dict):
	new_name = old_name
	for entry in csv_data:
		if entry['old_ap_name'] == old_name:
			new_name = entry['new_ap_name']
	return new_name	


for ap in accessPoints['accessPoints']:
	old_ap_name = ap['name']
	new_ap_name = find_AP_by_name(ap['name'], csv_data)
	ap['name'] = new_ap_name
	if old_ap_name != new_ap_name:
		print(old_ap_name, 'replaced with', new_ap_name)
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