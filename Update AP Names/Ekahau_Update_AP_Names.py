#!/usr/bin/env python3
'''------------------------------------------------------------------
    Filename:   Ekahau_Update_AP_Name.py
    author:     Haydn Andrews 
    date:       14/04/2021 
    desc:       Will Update AP names in Ekahau, appending a prefrex 
    			and Suffix. 
    			This is used as a lot of customers have the AP 
    			number in the middle of the naming convention.

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
	
#Request Naming Convention
NamePrefex = input("Please input the AP Naming prefex (wwmvmfdw): ")
NameSuffix = input("Please input the AP Naming prefex (c91): ")

for ap in accessPoints['accessPoints']:
	old_ap_name = ap['name']
	print(old_ap_name)
	#AP-(\d+)
	new_ap_name = NamePrefex + str(re.search(r'\d+', old_ap_name).group(0)) + NameSuffix
	print(new_ap_name)
	ap['name'] = new_ap_name
	if old_ap_name != new_ap_name:
		print(old_ap_name, 'replaced with', new_ap_name)
	if old_ap_name == new_ap_name:
		print(old_ap_name, 'left unchanged')

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