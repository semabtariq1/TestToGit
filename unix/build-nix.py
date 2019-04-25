import json
import os
import time
import platform
from config import *
from local_env import *


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


""" Checking operating system and setting platform related commands """
DOWNLOAD_KEY = 'curl -O'
osType = platform.system();
if osType == 'Linux':
	DOWNLOAD_KEY = 'wget'


""" Generate build """

print('Preparing to generate builds now ...')

""" Reading postgreSQ versions from postgres_versions.json """

with open('postgres_versions.json', 'r') as postgresVersions:
	postgresVersions = json.load(postgresVersions)


""" Setting up system PATH variables
	This section will hold/set/modify all the build related PATHS """

""" Saving current state of PATH """

PATH = os.environ['PATH']

""" Setting new PATHS """
print('Setting up proper system PATH variables ...')

os.environ['PYTHON_HOME']       = python_home

os.environ['OPENSSL_HOME']      = openssl_home

os.environ['LD_LIBRARY_PATH']   = os.environ['PYTHON_HOME'] +"/lib:"+ os.environ['OPENSSL_HOME'] +"/lib:"+ shareLib +"/lib:"+ pl_languages +"/Perl-5.26/lib"

os.environ['CPPFLAGS']          = "-I"+ os.environ['PYTHON_HOME'] +"inlclude/python3.4m -I"+ os.environ['OPENSSL_HOME'] +"/include -I"+ shareLib +"/include"

os.environ['PYTHON']            = os.environ['PYTHON_HOME'] +"/bin/python3"


for postgresVersion in postgresVersions:
	dateTime = time.strftime("%Y%m%d%H%M%S")

	print('\nStarting build process for '+ postgresVersion['fullVersion'])

	print('\n\nSetting up work dir structure ...')

	currentProjectDir = root +'/workDir/'+ projectName
	currentBuild = currentProjectDir +'/'+ dateTime +'/'+ postgresVersion['fullVersion']

	sourceDir = currentBuild +'/'+ 'source'
	logsDir = currentBuild +'/'+ 'logs'
	buildDir = currentBuild +'/'+ 'build' +'/'+ postgresVersion['majorVersion']

	res = os.system('mkdir -p '+ sourceDir +' && echo '+ sourceDir)
	res = os.system('mkdir -p '+ logsDir   +' && echo '+ logsDir)
	res = os.system('mkdir -p '+ buildDir  +' && echo '+ buildDir)
	if res != 0:
		print('\nCould not able to create proper work dir exit code 1 ...')
		exit()

	time.sleep(1)

	""" Setting system PATH to its default state first then set it to current build this is because if we have to built more than 1 postgreSQL versions then PATH will contain project dir PATH or each build which is why we need to remove the PATH of old builds first same case is true of build dir as we need to add current build dir path in LDfLAGS """

	os.environ['PATH']              = PATH

	os.environ['LDFLAGS']           = "-Wl,-rpath,"+ buildDir +" -L"+ os.environ['PYTHON_HOME'] +"/lib -L"+ os.environ['OPENSSL_HOME'] +"/lib -L"+ shareLib +"/lib -L"+ pl_languages +"/Perl-5.26/lib "

	os.environ['PATH']              = buildDir +"/bin:"+ os.environ['PYTHON_HOME'] +"/bin:"+ os.environ['OPENSSL_HOME'] +"/bin:"+ shareLib +"/bin:"+ pl_languages +"/Perl-5.26/bin:"+ os.environ['PATH']


	print('Downloading PostgreSQL source code ...')
	res = os.system('cd '+ sourceDir +' && '+ DOWNLOAD_KEY +' '+ postgresVersion['tarball'] +' > '+ logsDir +'/postgreSQL-source.log 2>&1')
	if res != 0:
		print('\nSomething went wrong for PostgreSQL source code downloading please refer to postgreSQL-source.log file ...')
		exit()


	""" Unzip the source code """
	print('Uncompress the source code ...')
	res = os.system('cd '+ sourceDir +' && tar xzf postgresql-'+ postgresVersion['fullVersion']+ '.tar.gz')
	if res != 0:
		print('\nSomething went wrong with PostgreSQL source code uncompressing ...')
		exit()


	""" Running ./configure on PostgreSQL """
	print('Running ./configure ...')
	
	""" Creating configure options """
	configureWith = ''
	configureFlags = ''

	if postgresVersion['OPENSSL'] == '1':
		configureWith += ' --with-openssl '

	if postgresVersion['GSSAPI']  == '1':
		configureWith += ' --with-gssapi '

	if postgresVersion['PYTHON']  == '1':
		configureWith += ' --with-python '

	if postgresVersion['PERL']    == '1':
		configureWith += ' --with-perl '

	if postgresVersion['LDAP']    == '1':
		configureWith += ' --with-ldap '

	if postgresVersion['ZLIB']    == '1':
		configureWith += ' --with-zlib '

	if postgresVersion['TCL']     == '1':
		configureWith += ' --with-tcl --with-tclconfig='+ pl_languages +'/Tcl-8.6/lib '
		os.environ['TCLSH'] = pl_languages +"/Tcl-8.6/lib"

	if postgresVersion['ICU']     == '1':
		configureWith += ' --with-icu '
		configureFlags = ' ICU_CFLAGS=\'-I'+ shareLib +'/include\' ICU_LIBS=\'-L'+ shareLib +'/lib -licui18n -licuuc -licudata\' '

	""" Executing ./configure command now """
	print('./configure '+ configureWith)
	res = os.system('cd '+ sourceDir +'/postgresql-'+ postgresVersion['fullVersion'] +' && ./configure '+ configureWith +' '+ configureFlags +' --prefix='+ buildDir +' > '+ logsDir +'/postgreSQL-configure.log 2>&1')
	if res != 0:
		print('\nSomething went wrong with ./configure see\n'+ logsDir +'/postgreSQL-configure.log ...')
		exit()
