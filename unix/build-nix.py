import json
import os
import time
import platform
import subprocess
from local_env import *
from urllib.parse import urlparse



print('\n\n\n')

print(' ************************************* \n')

print('           PRE BUILD SECTION           \n')

print(' ************************************* \n')



# Checking operating system and setting platform specific commands
print('checking operating system ...')
time.sleep(2)
DOWNLOAD_KEY = 'curl -O'
osType = platform.system();
if osType == 'Linux':
        DOWNLOAD_KEY = 'wget'
print('Operating system ... '+ osType)


# Checking all the required file, directories exists or not
print('Checking postgres_versions.json ...')
time.sleep(2)
if os.path.isfile('postgres_versions.json') != True:
	print('postgres_versions.json ... Not found\nError: Following property file is maybe deleted '+ root +'/postgres_versions.json')
	exit()


if os.path.getsize('postgres_versions.json') == 0:
	print('postgres_versions.json ... Empty\nError: Following property file should not be an empty file '+ root +'/postgres_versions.json')
	exit()
else:
	try:
		with open('postgres_versions.json', 'r') as postgresVersions:
			postgresVersions = json.load(postgresVersions)
	except ValueError:
		print('Reading postgres_versions.json ... FAILED\nError: Please check for proper json syntax in '+ root +'/postgres_versions.json')
		exit()
print('Reading postgres_versions.json ... ok')


print('Checking shared libraries directory ...')
time.sleep(2)
if os.path.exists(shareLib):
	if not os.listdir(shareLib):
		print('Shared libraries folder ... Empty\nError: Provided path to share libraries is empty '+ shareLib)
		exit()
else:
	print('Shared libraries folder ... NOT FOUND\nError: Provided path to share libraries does not exists '+ shareLib)
	exit()
print('Shared libraries folder ... ok')


print('Checking PL language directory ...')
time.sleep(2)
if os.path.exists(pl_languages):
        if not os.listdir(pl_languages):
                print('PL languages directory ... Empty\nError: Provided PL languages directory is empty '+ pl_languages)
                exit()
else:
        print('PL languages directory ... NOT FOUND\nError: Provided PL languages directory does not exists '+ pl_languages)
        exit()
print('PL language directory ... ok')


print('Checking Python directory ...')
time.sleep(2)
if os.path.exists(python_home):
        if not os.listdir(python_home):
                print('Python directory ... Empty\nError: Provided Python directory is empty '+ python_home)
                exit()
else:
        print('Python directory ... Not found\nError: Provided Python directory does not exists '+ python_home)
        exit()
print('Python directory ... ok')


print('Checking Openssl directory ...')
time.sleep(2)
if os.path.exists(openssl_home):
        if not os.listdir(openssl_home):
                print('Openssl directory ... Empty\nError: Provided Openssl directory is empty '+ openssl_home)
                exit()
else:
        print('Openssl directory ... NOT FOUND\nError: Provided Openssl directory dose not exists '+ openssl_home)
        exit()
print('Openssl directory ... ok')


print('Checking project name ...')
time.sleep(2)
if projectName == '':
	print('Project Name ... EMPTY\nError: Project name can not be an empty value please set a value in local_env.py')
	exit()
print('Project name ... '+ projectName)


# Checking status for installers creation mode switch
print('Checking installer creation mode ...')
time.sleep(1)
installerCreationMode = 'Disabled'
for postgresVersion in postgresVersions:
	if postgresVersion['createInstaller'] == '1':
		installerCreationMode = 'Enabled'
		break
print('Installer creation status ... '+ installerCreationMode)


# Running checks if Installer creation mode is Enabled
if installerCreationMode == 'Enabled':
	print('Checking signing directory ...')
	time.sleep(2)
	if os.path.exists(signingPasswordRoot):
		if os.path.isfile(signingPasswordRoot +'/signing-pass.vault'):
			print('signing-pass.vault ... ok')
		else:
			print('signing-pass.vault ... File not found\nError: signing-pass.vault does not exists at give path '+ signingPasswordRoot)
			exit()
	else:
		print('Signing directory ... Not found\nError: signing directory does not exists at given path '+ signingPasswordRoot)
		exit()


	print('Checking Bitrock installation ...')
	time.sleep(2)
	if os.path.exists(bitrockInstallation):
		res = os.system(bitrockInstallation +'/bin/builder --version')
		if res != 0:
			print('Bitrock version ... Not found\nError: Unable to check version of Bitrock it might be corrupted please try to re-install bitrock')
			exit()
		else:
			print('Bitrock installation ... ok')


	# Some temp variables used to create installer
	if osType == 'Darwin':
		tempOsType = 'OSX'
		tempOsTypeForInstaller = 'osx'
	else:
		tempOsType = 'Linux'
		tempOsTypeForInstaller = 'linux-x64'


	# Creating directory for Postgres installer source code and log files
	print('Creating required directory to clone installer source code ...')
	time.sleep(2)
	installerSourcFolder = root +'/workDir/'+ projectName +"/installers" # Variable which will point to installer directory inside workDir
	os.system('mkdir -p '+ installerSourcFolder)
	os.system('mkdir -p '+ installerSourcFolder +'/logs')


	if os.path.exists(installerSourcFolder):
		if os.path.exists(installerSourcFolder +'/logs'):
			print('Created ... '+ installerSourcFolder)
			print('Created ... '+ installerSourcFolder +'/logs')
		else:
			print('Create directory ... Fails\nError: Unable to create following directory '+ installerSourcFolder)
			exit()
	else:
		print('Create directory ... Fails\nError: Unable to create following directory '+ installerSourcFolder +'/logs')
		exit()


	# clone Postgres installer code
	print('Clone Installer repository ...')
	res = os.system('cd '+ installerSourcFolder +' && git clone --recursive https://github.com/2ndQuadrant/postgresql-installer.git > '+ installerSourcFolder +'/logs/Installer-source-clone.log 2>&1')
	if res != 0:
		print('Clone Postgres installer source repository ... FAILS')
		exit()
	else:
		print('Clone Postgres installer source repository ... OK')


        # Preparing a folder hierarchy for installers
	print('Creating directory hierarchy for builds and preparing components ...')
	time.sleep(2)
	os.system('mkdir -p '+ installerSourcFolder +'/postgresql-installer/final-installers' )
	os.system('mkdir -p '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'/OmniDB')


	# Checking required directories are created or not
	if os.path.exists(installerSourcFolder +'/postgresql-installer/final-installers'):
		print('Created ... '+ installerSourcFolder +'/postgresql-installer/final-installers')
	else:
		print('Unable to create => '+ installerSourcFolder +'/postgresql-installer/final-installers')
		exit()

	if os.path.exists(installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'/OmniDB'):
		print('Created ... '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'OmniDB')
	else:
		print('Unable to create => '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'OmniDB')
		exit()


	# Checkout stable branch
	print('Checkout stable branch ...')
	time.sleep(2)
	res = os.system('cd '+ installerSourcFolder +'/postgresql-installer && git checkout stable > '+ installerSourcFolder +'/logs/checkout-stable.log 2>&1')
	if res != 0:
		print('Checkout stable branch ... FAILS')
		exit()
	else:
		print('Checkout stable branch ... OK')


	# Preparing components for installer
	# Pl languages
	print('Prepare PL languages component ...')
	res = os.system('cp -r '+ pl_languages +' '+ installerSourcFolder+'/postgresql-installer/Builds/'+ tempOsType)
	if res != 0:
		print('PL languages component ... FAILS')
		exit()
	else:
		print('PL languages component ... OK')


	# OmniDB
	print('Prepare OmniDB component... ')
	time.sleep(2)
	print('Downloading OmniDB ...')
	res = os.system('cd '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +' && '+ DOWNLOAD_KEY +'  '+ omnidbUrl +' > '+ installerSourcFolder +'/logs/OmniDB-download.log 2>&1')
	if res != 0:
		print('Download OmniDB ... FAILS\nErroe: OmniDB downloading fails please see followng file for more details '+ installerSourcFolder +'/logs/OmniDB-download.log')
		exit()


	# Get filename from url
	omnidbFileName = urlparse(omnidbUrl)
	omnidbFileName = os.path.basename(omnidbFileName.path)
	print('OmniDB file name ... '+ omnidbFileName)


	if osType == 'Linux':
		res = os.system('cd '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +' && rpm2cpio ./'+ omnidbFileName +' | cpio -idmv > '+ installerSourcFolder +'/logs/OmniDB-extract.log 2>&1')
		if res != 0:
			print('Extract OmniDB files  ... FAILS\nError: Could not able to extract OmniDB file please see following file for more details '+ installerSourcFolder +'/logs/OmniDB-extract.log')
			exit()
		else:
			print('Extract OmniDB files ... OK')
		res = os.system('cp -r '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'/opt/* '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'/OmniDB')
		if res != 0:
			print('OmniDB component ... FAILS\nError: Copy fails from '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'/opt/*')
			exit()
		else:
			print('OmniDB component status ... OK')
	else:
		print('Running open on ... '+ omnidbFileName )
		res = os.system('open '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'/'+ omnidbFileName)
		if res != 0:
			print('open OmniDB file ... Fails\nError: open command returns non zeor value on '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'/'+ omnidbFileName)
			exit()

		print('Waiting for /Volumes/OmniDB Installer/OmniDB.app path to became available ...')
		while True:
			if os.path.exists('/Volumes/OmniDB Installer/OmniDB.app'):
				print('Copy OmniDB binaries ...')
				os.system('cp -r "/Volumes/OmniDB Installer/OmniDB.app" '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'/OmniDB > '+ installerSourcFolder +'/logs/OmniDB-copy.log 2>&1')
				print('Detach the /Volumes/OmniDB Installer ...')
				time.sleep(1)
				res = os.system('hdiutil detach "/Volumes/OmniDB Installer" > '+ installerSourcFolder +'/logs/OmniDB-detach.log 2>&1')
				if res != 0:
					print('detach "/Volumes/OmniDB Installer" ... FAILS')
					exit()
				else:
					print('detach "/Volumes/OmniDB Installer" ... OK')
					print('OmniDB component ... ok')
				break
			else:
				continue


print('\nPre build checks are executed successfully ...')
time.sleep(3)


print('\n\n\n')

print(' ********************************************* \n')

print('           BUILDS GENERATION SECTION           \n')

print(' ********************************************* \n')



# Saving current state of PATH
PATH = os.environ['PATH']


currentProjectDir = root +'/workDir/'+ projectName


for postgresVersion in postgresVersions:
	print('\nStarting build process for '+ postgresVersion['fullVersion']+'\n')

	# Setting up system PATH variables
        # This section will hold/set/modify all the build related PATHS
	print('Setting up system PATH variables ...')
	os.environ['LD_LIBRARY_PATH']   = shareLib +'/lib'
	os.environ['CPPFLAGS']          = '-I'+ shareLib +'/include'
	os.environ['LDFLAGS']           = ' -L'+ shareLib +'/lib'

	dateTime = time.strftime("%Y%m%d%H%M%S")

	print('Setting up work dir structure ...')
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

	os.environ['LDFLAGS']           = '-Wl,-rpath,'+ buildDir + os.environ['LDFLAGS'] 

	os.environ['PATH']              = buildDir +"/bin:"+ shareLib +"/bin:"+ os.environ['PATH']


	print('Downloading PostgreSQL source code ...')
	res = os.system('cd '+ sourceDir +' && '+ DOWNLOAD_KEY +' '+ postgresVersion['tarball'] +' > '+ logsDir +'/postgreSQL-source.log 2>&1')
	if res != 0:
		print('\nSomething went wrong for PostgreSQL source code downloading please refer to postgreSQL-source.log file ...')
		exit()


	""" Unzip the source code """
	print('Uncompress the source code ...')
	res = os.system('cd '+ sourceDir +' && tar xzf postgresql-'+ postgresVersion['fullVersion'] +'.tar.gz')
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
		os.environ['OPENSSL_HOME']      = openssl_home
		os.environ['LD_LIBRARY_PATH']   = os.environ['OPENSSL_HOME'] +'/lib:'+ os.environ['LD_LIBRARY_PATH']
		os.environ['CPPFLAGS']          = '-I'+ os.environ['OPENSSL_HOME'] +'/include '+ os.environ['CPPFLAGS']
		os.environ['LDFLAGS']           = os.environ['LDFLAGS'] +' -L'+ os.environ['OPENSSL_HOME'] +"/lib"
		os.environ['PATH']              = os.environ['OPENSSL_HOME'] +"/bin:"+ os.environ['PATH']

	if postgresVersion['GSSAPI']  == '1':
		configureWith += ' --with-gssapi '

	if postgresVersion['PYTHON']  == '1':
		configureWith += ' --with-python '
		os.environ['PYTHON_HOME']       = python_home
		os.environ['LD_LIBRARY_PATH']   = os.environ['PYTHON_HOME'] +'/lib:'+ os.environ['LD_LIBRARY_PATH']
		os.environ['PYTHON']            = os.environ['PYTHON_HOME'] +'/bin/python3'
		os.environ['CPPFLAGS']          = '-I'+ os.environ['PYTHON_HOME'] +'/inlclude/python3.4m '+ os.environ['CPPFLAGS']
		os.environ['LDFLAGS']           = os.environ['LDFLAGS'] +' -L'+ os.environ['PYTHON_HOME'] +'/lib'
		os.environ['PATH']              = os.environ['PYTHON_HOME'] +"/bin:"+ os.environ['PATH']

	if postgresVersion['PERL']    == '1':
		configureWith += ' --with-perl '
		os.environ['LD_LIBRARY_PATH']   = pl_languages +'/Perl-5.26/lib:'+ os.environ['LD_LIBRARY_PATH']
		os.environ['LDFLAGS']           = os.environ['LDFLAGS'] +' -L'+ pl_languages +'/Perl-5.26/lib'
		os.environ['PATH']              = pl_languages +'/Perl-5.26/bin:'+ os.environ['PATH']

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


	""" Running make on PostgreSQL source code """
	print('Running make ...')
	res = os.system('cd '+ sourceDir +'/postgresql-'+ postgresVersion['fullVersion'] +' && make world > '+ logsDir +'/postgreSQL-make.log 2>&1')
	if res != 0:
		print('\nSomething went wrong with make see\n'+ logsDir +'/postgreSQL-make.log ...')
		exit()


	""" Running make check on PostgreSQL """	
	print('Running make check ...')
	res = os.system('cd '+ sourceDir +'/postgresql-'+ postgresVersion['fullVersion'] +' && make check > '+ logsDir +'/postgreSQL-make-check.log 2>&1')
	if res != 0:
		print('\nSomething went wrong with make check see\n'+ logsDir +'/postgreSQL-make-check.log ...')
		exit()


	""" Running make install on PostgreSQL """
	print('Running make install ...')
	res = os.system('cd '+ sourceDir +'/postgresql-'+ postgresVersion['fullVersion'] +' && make install-world > '+ logsDir +'/postgreSQL-make-install.log 2>&1')
	if res != 0:
		print('\nSomething went wrong with make install see\n'+ logsDir +'/postgreSQL-make-install.log ...')
		exit()


	if postgresVersion['POSTGIS'] == '1':
		print('Build POSTGIS now ...')

		""" Download source code """
		res = os.system('cd '+ sourceDir +' && '+ DOWNLOAD_KEY +' '+ postgresVersion['POSTGISTARBALL'] +' > '+ logsDir +'/postgis-source.log 2>&1')
		if res != 0:
			print('\nSomething went wrong with downloading the source code see\n'+ logsDir +'/postgis-source.log')
			exit()


		""" Uncompress the source code """
		print('Uncompress the source code ...')
		res = os.system('cd '+ sourceDir +' && tar xzf postgis-'+ postgresVersion['POSTGISVERSION'] +'.tar.gz')
		if res != 0:
			print('Something went wrong with postgis uncompressing ...')
			exit()


		""" Running ./configure """
		print('Running ./configure ...')
		res = os.system('cd '+ sourceDir +'/postgis-'+ postgresVersion['POSTGISVERSION'] +' && ./configure --prefix='+ shareLib +' --with-pgconfig='+ buildDir +'/bin/pg_config --with-gdalconfig=' + shareLib + '/bin/gdal-config  --with-geosconfig='+ shareLib +'/bin/geos-config --with-projdir='+ shareLib +' --with-xml2config='+ shareLib +'/bin/xml2-config > '+ logsDir +'/postgis-configure.log 2>&1')
		if res != 0:
			print('\nSomthing went wrong with postgis configure see\n'+ logsDir +'/postgis-configure.log ...')
			exit()


		""" Running make """
		print('Running make ...')
		res = os.system('cd '+ sourceDir +'/postgis-'+ postgresVersion['POSTGISVERSION'] +' && make > '+ logsDir +'/postgis-make.log 2>&1')
		if res != 0:
			print('\nSomething went wrong with make see\n'+ logsDir +'\postgis-make.log ...')
			exit()


		""" Running regression tests on postgis """
		print('Running make check ...')
		
		""" initializing the data dir """
		res = os.system('cd '+ buildDir +'/bin && ./initdb -D '+ logsDir +'/data > '+ logsDir +'/postgreSQL-init.log 2>&1')
		if res != 0:
			print('\nCould not able to initialize the data dir see\n'+ logsDir +'/postgreSQL-init.log ...')
			exit()

		""" Starting postgreSQL server """
		res = os.system('cd '+ buildDir +'/bin && ./pg_ctl -D '+ logsDir +'/data start > '+ logsDir +'/postgreSQL-pgctl.log 2>&1')
		if res != 0:
			print('\nCould not able to start PostgreSQL server see\n'+ logsDir +'/postgreSQL-pgctl.log ...')
			exit()

		""" Running make check on postgis now """
		res = os.system('cd '+ sourceDir +'/postgis-'+ postgresVersion['POSTGISVERSION'] +' && make check > '+ logsDir +'/postgis-make-check.log 2>&1')
		if res != 0:
			print('\nSomething went wrong with make check see\n'+ logsDir +'/postgis-make-check.log ...')
			exit()

		""" Shutting down postgresql servver """
		os.system('cd '+ buildDir +'/bin && ./pg_ctl -D '+ logsDir +'/data stop >> '+ logsDir +'/postgreSQL-pgctl.log 2>&1')

		""" running make install on postgis """
		print('Running make install ...')
		res = os.system('cd '+ sourceDir +'/postgis-'+ postgresVersion['POSTGISVERSION'] +' && make install > '+ logsDir +'/postgis-make-install.log 2>&1')
		if res != 0:
			print('\nSomething went wrong with make install see\n'+ logsDir +'/postgis-make-install.lo ...')
			exit()


	""" Copy shareLib/lib into buildDir/lib """
	print('Copy shareLib/lib into buildDir/lib ...')
	os.system('cp -rv '+ shareLib +'/lib/* '+ buildDir +'/lib/ > '+ logsDir +'/copy.log')

	""" Copy shareLib/share/gdal into buildDir/share """
	print('Copy shareLib/share/gdal into buildDir/share ...')
	os.system('cp -rv '+ shareLib +'/share/gdal '+ buildDir +'/share/ >> '+ logsDir +'/copy.log')

	""" Copy sharelib/share/proj from buildDir/share """
	print('Copy sharelib/share/proj from buildDir/share...')
	os.system('cp -rv '+ shareLib +'/share/proj '+ buildDir +'/share/ >> '+ logsDir +'/copy.log')

	""" Copy openssl/lib into buildDir/lib """
	print('Copy openssl/lib into buildDir/lib ...')
	os.system('cp -rv '+ openssl_home +'/lib/* '+ buildDir +'/lib/ >> '+ logsDir +'/copy.log')

	""" Platform related actions """
	if osType == 'Linux':
		
		""" Setting runtime paths """

		print('Setting runtime paths for bin ...')
		for file in os.listdir(buildDir +'/bin'):
			os.system('cd '+ buildDir +'/bin && chrpath -r "\${ORIGIN}/../lib/" "./'+ file +'" >> '+ logsDir +'/postgreSQL-bin-rpaths.log 2>&1')

		print('Setting runtime paths for lib ...')
		for file in os.listdir(buildDir +'/lib'):
			os.system('cd '+ buildDir +'/lib && chrpath -r "\${ORIGIN}/../lib/" "./'+ file +'" >> '+ logsDir +'/postgreSQL-lib-rpaths.log 2>&1')

		if os.path.exists(buildDir +'/lib/postgresql'):
			print('Setting runtime paths for lib/postgresql ...')
			for file in os.listdir(buildDir +'/lib/postgresql'):
				os.system('cd '+ buildDir +'/lib/postgresql && chrpath -r "\${ORIGIN}/../../lib/" "./'+ file +'" >> '+ logsDir +'/postgreSQL-postgresql-rpaths.log 2>&1')

		# Uncommit it if we have build a new version of TCL 
                # os.system('cd /opt/2ndQuadrant/pl-languages/Tcl-8.6/bin && chrpath -r "\${ORIGIN}/../lib/" ./tclsh8.6' " >> "+ logsDir +"/pltcl-rpath.log 2>&1")

	else:
		""" Setting runtime paths """
		print('Setting runtime paths for bin ...')

		for file in os.listdir(buildDir +"/bin"):

                                    os.system('cd '+ buildDir +'/bin && install_name_tool -delete_rpath '+ buildDir +' -add_rpath @executable_path/../lib "./'+ file +'" >> '+ logsDir +"/postgreSQL-bin-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/bin && install_name_tool -change "'+ buildDir +'/lib/libpq.5.dylib" "@executable_path/../lib/libpq.5.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-bin-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/bin && install_name_tool -change "'+ os.environ['OPENSSL_HOME'] +'/lib/libssl.1.0.0.dylib" "@executable_path/../lib/libssl.1.0.0.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-bin-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/bin && install_name_tool -change "'+ os.environ['OPENSSL_HOME'] +'/lib/libcrypto.1.0.0.dylib" "@executable_path/../lib/libcrypto.1.0.0.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-bin-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/bin && install_name_tool -change "'+ shareLib +'/lib/libgeos_c.1.dylib" "@executable_path/../lib/libgeos_c.1.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-bin-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/bin && install_name_tool -change "'+ shareLib +'/lib/libproj.13.dylib" "@executable_path/../lib/libproj.13.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-bin-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/bin && install_name_tool -change "'+ shareLib +'/lib/libgeos-3.6.2.dylib" "@executable_path/../lib/libgeos-3.6.2.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-bin-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/bin && install_name_tool -change "'+ shareLib +'/lib/libxml2.2.dylib" "@executable_path/../lib/libxml2.2.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-bin-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/bin && install_name_tool -change "'+ shareLib +'/lib/libgdal.20.dylib" "@executable_path/../lib/libgdal.20.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-bin-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/bin && install_name_tool -change "'+ shareLib +'/lib/libicui18n.62.dylib" "@executable_path/../lib/libicui18n.62.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-bin-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/bin && install_name_tool -change "'+ shareLib +'/lib/libicuuc.62.dylib" "@executable_path/../lib/libicuuc.62.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-bin-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/bin && install_name_tool -change "'+ shareLib +'/lib/libicudata.62.dylib" "@executable_path/../lib/libicudata.62.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-bin-rpath.log 2>&1")


		print('Setting rpaths for lib ...')
		for file in os.listdir(buildDir +"/lib"):
                                    os.system('cd '+ buildDir +'/lib && install_name_tool -delete_rpath '+ buildDir +' -add_rpath @executable_path/../lib "./'+ file +'" >> '+ logsDir +"/postgreSQL-lib-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib && install_name_tool -change "'+ buildDir +'/lib/libpq.5.dylib" "@executable_path/../lib/libpq.5.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-lib-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib && install_name_tool -change "'+ os.environ['OPENSSL_HOME'] +'/lib/libssl.1.0.0.dylib" "@executable_path/../lib/libssl.1.0.0.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-lib-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib && install_name_tool -change "'+ os.environ['OPENSSL_HOME'] +'/lib/libcrypto.1.0.0.dylib" "@executable_path/../lib/libcrypto.1.0.0.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-lib-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib && install_name_tool -change "'+ shareLib +'/lib/libgeos_c.1.dylib" "@executable_path/../lib/libgeos_c.1.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-lib-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib && install_name_tool -change "'+ shareLib +'/lib/libproj.13.dylib" "@executable_path/../lib/libproj.13.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-lib-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib && install_name_tool -change "'+ shareLib +'/lib/libgeos-3.6.2.dylib" "@executable_path/../lib/libgeos-3.6.2.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-lib-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib && install_name_tool -change "'+ shareLib +'/lib/libxml2.2.dylib" "@executable_path/../lib/libxml2.2.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-lib-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib && install_name_tool -change "'+ shareLib +'/lib/libgdal.20.dylib" "@executable_path/../lib/libgdal.20.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-lib-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib && install_name_tool -change "'+ shareLib +'/lib/libicui18n.62.dylib" "@executable_path/../lib/libicui18n.62.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-lib-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib && install_name_tool -change "'+ shareLib +'/lib/libicuuc.62.dylib" "@executable_path/../lib/libicuuc.62.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-lib-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib && install_name_tool -change "'+ shareLib +'/lib/libicudata.62.dylib" "@executable_path/../lib/libicudata.62.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-lib-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib && install_name_tool -change "/Users/2ndquadrant/pl-languages/perl-5.26/lib/CORE/libperl.dylib" "@executable_path/../../pl-languages/Perl-5.26/lib/CORE/libperl.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-postgresql-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib && install_name_tool -change "/Applications/2ndQuadrant/PostgreSQL/pl-languages/Tcl-8.6/lib/libtcl8.6.dylib" "@executable_path/../../pl-languages/Tcl-8.6/lib/libtcl8.6.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-postgresql-rpath.log 2>&1")


		if os.path.exists(buildDir +'/lib/postgresql'):
			print('Setting rpaths for lib/postgresql ...')
			for file in os.listdir(buildDir +"/lib/postgresql"):  
                                    os.system('cd '+ buildDir +'/lib/postgresql && install_name_tool -delete_rpath '+ buildDir +' -add_rpath @executable_path/../lib "./'+ file +'" >> '+ logsDir +"/postgreSQL-postgresql-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib/postgresql && install_name_tool -change "'+ buildDir +'/lib/libpq.5.dylib" "@executable_path/../lib/libpq.5.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-postgresql-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib/postgresql && install_name_tool -change "'+ os.environ['OPENSSL_HOME'] +'/lib/libssl.1.0.0.dylib" "@executable_path/../lib/libssl.1.0.0.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-postgresql-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib/postgresql && install_name_tool -change "'+ os.environ['OPENSSL_HOME'] +'/lib/libcrypto.1.0.0.dylib" "@executable_path/../lib/libcrypto.1.0.0.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-postgresql-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib/postgresql && install_name_tool -change "'+ shareLib +'/lib/libgeos_c.1.dylib" "@executable_path/../lib/libgeos_c.1.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-postgresql-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib/postgresql && install_name_tool -change "'+ shareLib +'/lib/libproj.13.dylib" "@executable_path/../lib/libproj.13.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-postgresql-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib/postgresql && install_name_tool -change "'+ shareLib +'/lib/libgeos-3.6.2.dylib" "@executable_path/../lib/libgeos-3.6.2.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-postgresql-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib/postgresql && install_name_tool -change "'+ shareLib +'/lib/libgdal.20.dylib" "@executable_path/../lib/libgdal.20.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-postgresql-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib/postgresql && install_name_tool -change "'+ shareLib +'/lib/libxml2.2.dylib" "@executable_path/../lib/libxml2.2.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-postgresql-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib/postgresql && install_name_tool -change "'+ shareLib +'/lib/libicui18n.62.dylib" "@executable_path/../lib/libicui18n.62.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-postgresql-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib/postgresql && install_name_tool -change "'+ shareLib +'/lib/libicuuc.62.dylib" "@executable_path/../lib/libicuuc.62.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-postgresql-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib/postgresql && install_name_tool -change "'+ shareLib +'/lib/libicudata.62.dylib" "@executable_path/../lib/libicudata.62.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-postgresql-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib/postgresql && install_name_tool -change "/Users/2ndquadrant/pl-languages/perl-5.26/lib/CORE/libperl.dylib" "@executable_path/../../pl-languages/Perl-5.26/lib/CORE/libperl.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-postgresql-rpath.log 2>&1")

                                    os.system('cd '+ buildDir +'/lib/postgresql && install_name_tool -change "/Applications/2ndQuadrant/PostgreSQL/pl-languages/Tcl-8.6/lib/libtcl8.6.dylib" "@executable_path/../../pl-languages/Tcl-8.6/lib/libtcl8.6.dylib" "./'+ file +'" >> '+ logsDir +"/postgreSQL-postgresql-rpath.log 2>&1")


	""" Code related to 2UDA """
	if postgresVersion['QUANTILE'] == '1':
		print('build QUANTILE ... ')
		os.system('cd '+ sourceDir +' && git clone https://github.com/tvondra/quantile.git > '+ logsDir +'/quantile-clone.log 2>&1')
		if postgresVersion['majorVersion'] == '9.5':
			res = os.system('cd '+ sourceDir +'/quantile && make USE_PGXS=1 > '+ logsDir +'/quantile-build.log 2>&1 && make USE_PGXS=1 install >> '+ logsDir +'/quantile-build.log 2>&1')
			if res != 0:
				print('QUANTILE fails ...')
				exit()
		else:
			res = os.system('cd '+ sourceDir +'/quantile && git checkout parallel-aggregation && make USE_PGXS=1 > '+ logsDir +'/quantile-build.log 2>&1 && make USE_PGXS=1 install >> '+ logsDir +'/quantile-build.log 2>&1')
			if res != 0:
				print('QUANTILE fails ...')
				exit()


	""" Generating .tar.gz file of final bundle """
	res = os.system('cd '+ currentBuild +'/build && tar -zcvf PostgreSQL-'+ osType +'-'+ postgresVersion['fullVersion'] +'.tar.gz '+ postgresVersion['majorVersion'] +' > '+ logsDir +'/generate-tar-file.log 2>&1')
	if res != 0:
		print('\nUnable to create tar.gz of final bundle see\n'+ logsDir +'/generate-tar-file.log ...')
		exit()



	print('\n\n\n')

	print(' ************************************************ \n')

	print('           INSTALLER GENERATION SECTION           \n')

	print(' ************************************************ \n')



	""" Checking installer creation mode """
	if installerCreationMode == 'Enabled':

		""" Check if current version of PostgreSQL build needs an installer """
		if postgresVersion['createInstaller'] == '1':

			""" Creating required folder structure inside Postgres installer clone repo """
			print(installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'/'+ postgresVersion["majorVersion"])
			os.makedirs(installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'/'+ postgresVersion["majorVersion"])
			""" Copy build into installerSourcFolder/postgresql-installer/Builds/ """
			print('Copy build into: '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'/'+ postgresVersion["majorVersion"])
			os.system('cp -r '+ buildDir +'/* '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'/'+ postgresVersion["majorVersion"])

			# Re-generating installer-properties.sh
			print('Re-generating installer-properties.sh ...')
			f = open(installerSourcFolder +'/postgresql-installer/installer-properties.sh',"w+")

			f.write('__PG_MAJOR_VERSION__='+      postgresVersion['majorVersion']              +'\n')
			f.write('__FULL_VERSION__='+          postgresVersion['fullVersion']               +'\n')
			f.write('__EXTRA_VERSION_STRING__='+  postgresVersion['__EXTRA_VERSION_STRING__']  +'\n')
			f.write('__RELEASE__='+               postgresVersion['__RELEASE__']               +'\n')
			f.write('__BUILD_NUMBER__='+          postgresVersion['__BUILD_NUMBER__']          +'\n')
			f.write('__DEV_TEST__='+              postgresVersion['__DEV_TEST__']              +'\n')
			f.write('__DEBUG__='+                 postgresVersion['__DEBUG__']                 +'\n')

			f.close()


			# Running autogen.sh
			os.system('cd '+ installerSourcFolder +'/postgresql-installer && ./autogen.sh')


			# Generating installer
			print('Build installer ...')
			res = os.system('source '+ signingPasswordRoot +'/signing-pass.vault && '+ bitrockInstallation +'/bin/builder build '+ installerSourcFolder +'/postgresql-installer/'+ projectFileName +' '+ tempOsTypeForInstaller +' --setvars project.outputDirectory='+ installerSourcFolder +'/postgresql-installer/final-installers > '+ logsDir +'/build-installer-'+ postgresVersion["majorVersion"] +'.log 2>&1')


			if res != 0:
				print('Unable to generate installer ...')
			else:
				installerExetension = '.app.zip'
				if osType == 'Linux':
					installerExetension = '.run'
				print('Installer placed at: '+ installerSourcFolder +'/postgresql-installer/final-installers/PostgreSQL-'+ postgresVersion['fullVersion'] +'-'+ postgresVersion['__BUILD_NUMBER__'] +'-'+ tempOsTypeForInstaller +'-installer'+ installerExetension)
