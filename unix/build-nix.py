import json
import os


""" Pre build checks """


""" Check file exists, Check if not empty, Read version file(postgresVersions.json) """

try:
	if os.path.isfile('postgresVersions.json') != True:
		print('postgresVersions.json file not found ...')
		exit()

	if os.path.getsize('postgresVersions.json') == 0:
		print('postgresVersions.json should not be an empty file ...')
		exit()

	with open('postgresVersions.json', 'r') as componentsInfo:
		componentsInfo = json.load(componentsInfo)

	print('all ok ...')
except:
	print('Please use proper formatting for postgresVersions.json file ...')
