import json
import os
from config import *
from local_env import *


""" Call Linux build machine to generate builds """
if platform.system() == 'Darwin' and callLinuxBuildMachine == 1:
	os.system('ssh '+ userName +'@'+ ipAddr +' "cd '+ buildCode +' && python3 build-nix.py"')


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

except:
	print('Please use proper formatting for postgresVersions.json file ...')

""" Check share lib folder available or not on give path """

if os.path.exists(shareLib) and os.path.isdir(shareLib):
	if not os.listdir(shareLib):
		print('Provided share lib is empty ...')
		exit()
else:
	print('provided share lib don"t exists ...')
	exit()

print('Pre build checks are executed successfully ...')
