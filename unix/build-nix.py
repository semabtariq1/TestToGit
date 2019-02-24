import json
import os
from config import *
from local_env_pvt import *


""" Call Linux build machine to generate builds """
if platform.system() == 'Darwin' and callLinuxBuildMachine == 1:
	os.system('ssh '+ userName +'@'+ ipAddr +' "cd '+ buildCode +' && python3 build-nix.py"')


""" Pre build checks """

""" Check file exists, Check if not empty, Read version file(postgres_versions.json) """

try:
	if os.path.isfile('postgres_versions.json') != True:
		print('postgres_versions.json file not found ...')
		exit()

	if os.path.getsize('postgres_versions.json') == 0:
		print('postgres_versions.json should not be an empty file ...')
		exit()

	with open('postgres_versions.json', 'r') as componentsInfo:
		componentsInfo = json.load(componentsInfo)

except:
	print('Please use proper formatting for postgres_versions.json file ...')

""" Check share lib folder available or not on give path """

if os.path.exists(shareLib) and os.path.isdir(shareLib):
	if not os.listdir(shareLib):
		print('Provided share lib is empty ...')
		exit()
else:
	print('provided share lib don"t exists ...')
	exit()

print('Pre build checks are executed successfully ...')


""" Generate build """

print('Preparing to generate builds now ...')

""" Reading postgreSQ versions from postgres_versions.json """

with open('postgres_versions.json', 'r') as postgresVersion:
	postgresVersion = json.load(postgresVersion)

for version in postgresVersion:
	print('full version = '+ version['postgresFullVersion'])
