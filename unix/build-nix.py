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
DOWNLOAD_KEY = 'curl -O'
osType = platform.system();

if osType == 'Linux':
        DOWNLOAD_KEY = 'wget'

print('Operating system ... '+ osType)


# Checking all the required file, directories exists or not

if os.path.isfile('postgres_versions.json') != True:
	print('postgres_versions.json ... NOT FOUND')
	exit()
else:
	print('postgres_versions.json ... OK')

if os.path.getsize('postgres_versions.json') == 0:
	print('postgres_versions.json ... CONTENT NOT FOUND')
	exit()
else:
	print('postgres_versions.json ... CONTENT FOUND')

	try:
		with open('postgres_versions.json', 'r') as postgresVersions:
			postgresVersions = json.load(postgresVersions)
	except ValueError:
		print('Reading postgres_versions.json ... FAILED\nNOTE: Please check for proper json syntax')
		exit()
	print('Reading postgres_versions.json ... OK')

if os.path.exists(shareLib):
	print('Shared libraries folder ... OK')

	if not os.listdir(shareLib):
		print('Shared libraries folder ... CONTENT NOT FOUND')
		exit()
	else:
		print('Shared libraries folder ... CONTENT FOUND ')
else:
	print('Shared libraries folder ... NOT FOUND')
	exit()

if os.path.exists(pl_languages):
        print('PL languages folder ... OK')

        if not os.listdir(pl_languages):
                print('PL languages folder ... CONTENT NOT FOUND')
                exit()
        else:
                print('PL languages folder ... CONTENT FOUND ')
else:
        print('PL languages folder ... NOT FOUND')
        exit()

if os.path.exists(python_home):
        print('Python folder ... OK')

        if not os.listdir(python_home):
                print('Python folder ... CONTENT NOT FOUND')
                exit()
        else:
                print('Python folder ... CONTENT FOUND ')
else:
        print('Python folder ... NOT FOUND')
        exit()

if os.path.exists(openssl_home):
        print('Openssl folder ... OK')

        if not os.listdir(openssl_home):
                print('Openssl folder ... CONTENT NOT FOUND')
                exit()
        else:
                print('Openssl folder ... CONTENT FOUND ')
else:
        print('Openssl folder ... NOT FOUND')
        exit()

if projectName == '':
	print('Project Name property ... EMPTY')
	exit()
else:
	print('Project name ... '+ projectName)

# Checking status for installers creation mode switch
installerCreationMode = 'Disabled'
for postgresVersion in postgresVersions:

	if postgresVersion['createInstaller'] == '1':
		installerCreationMode = 'Enabled'
		break

print('Installer creation status ... '+ installerCreationMode)

# Running check if Installer creation mode is Enabled

if installerCreationMode == 'Enabled':
	# Some temp variables used to create installer

	if osType == 'Darwin':
		tempOsType = 'OSX'
		tempOsTypeForInstaller = 'osx'
	else:
		tempOsType = 'Linux'
		tempOsTypeForInstaller = 'linux-x64'


	# Creating directory for Postgres installer source code and log files
	installerSourcFolder = root +'/workDir/'+ projectName +"/installers" # Variable which will point to installer directory inside workDir
	os.system('mkdir -p '+ installerSourcFolder)
	os.system('mkdir -p '+ installerSourcFolder +'/logs')

	# clone Postgres installer code
	res = os.system('cd '+ installerSourcFolder +' && git clone --recursive https://github.com/2ndQuadrant/postgresql-installer.git > '+ installerSourcFolder +'/logs/Installer-source-clone.log 2>&1')
	if res != 0:
		print('Clne Postgres installer source repository ... FAILS')
		exit()
	else:
		print('Clne Postgres installer source repository ... OK')


        # Preparing a folder hierarchy for installers
	os.system('mkdir -p '+ installerSourcFolder +'/postgresql-installer/final-installers' )
	os.system('mkdir -p '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'/OmniDB')

	# Checking required directories are created or not
	if os.path.exists(installerSourcFolder +'/postgresql-installer/final-installers'):
		print('Installer final executable path ... '+ installerSourcFolder +'/postgresql-installer/final-installers')
	else:
		print('Unable to create => '+ installerSourcFolder +'/postgresql-installer/final-installers')
		exit()

	if os.path.exists(installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'/OmniDB'):
		print('OmniDB binaries path ... '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'OmniDB')
	else:
		print('Unable to create => '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'OmniDB')
		exit()



	# Checkout stable branch
	res = os.system('cd '+ installerSourcFolder +'/postgresql-installer && git checkout stable')
	if res != 0:
		print('Checkout stable branch ... FAILS')
		exit()
	else:
		print('Checkout stable branch ... OK')

	# Preparing components for installer

	# Pl languages
	res = os.system('cp -r '+ pl_languages +' '+ installerSourcFolder+'/postgresql-installer/Builds/'+ tempOsType)
	if res != 0:
		print('PL languages component ... FAILS')
		exit()
	else:
		print('PL languages component ... OK')

	# OmniDB
	res = os.system('cd '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +' && '+ DOWNLOAD_KEY +'  '+ omnidbUrl +' > '+ installerSourcFolder +'/logs/OmniDB-download.log 2>&1')

	if res != 0:
		print('Download OmniDB ... FAILS')
		exit()
	else:
		print('Download OmniDB ... OK')

	# Get filename from url
	omnidbFileName = urlparse(omnidbUrl)
	omnidbFileName = os.path.basename(omnidbFileName.path)

	if osType == 'Linux':
		res = os.system('cd '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +' && rpm2cpio ./'+ omnidbFileName +' | cpio -idmv > '+ installerSourcFolder +'/logs/OmniDB-extract.log 2>&1')

		if res != 0:
			print('Extract OmniDB files  ... FAILS')
			exit()
		else:
			print('Extract OmniDB files ... OK')

		res = os.system('cp -r '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'/opt/* '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'/OmniDB')

		if res != 0:
			print('OmniDB component ... FAILS')
			exit()
		else:
			print('OmniDB component ... OK')

	else:
		print('Prepare OmniDB component ...')
		res = os.system('open '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'/'+ omnidbFileName)

		if res != 0:
			print('Can not open OmniDB file ... '+ omnidbFileName)
			exit()

		while True:
			if os.path.exists('/Volumes/OmniDB Installer/OmniDB.app'):
				os.system('cp -r "/Volumes/OmniDB Installer/OmniDB.app" '+ installerSourcFolder +'/postgresql-installer/Builds/'+ tempOsType +'/OmniDB > '+ installerSourcFolder +'/logs/OmniDB-copy.log 2>&1')

				res = os.system('hdiutil detach "/Volumes/OmniDB Installer"')

				if res != 0:
					print('detach "/Volumes/OmniDB Installer" ... FAILS')
					exit()
				else:
					print('detach "/Volumes/OmniDB Installer" ... OK')

				break
			else:
				continue


print('Pre build checks are executed successfully ...')




print('\n\n\n')

print(' ********************************************* \n')

print('           BUILDS GENERATION SECTION           \n')

print(' ********************************************* \n')



print('Preparing to generate builds now ...')

""" Reading postgreSQ versions from postgres_versions.json """

with open('postgres_versions.json', 'r') as postgresVersions:
	postgresVersions = json.load(postgresVersions)


""" Saving current state of PATH """
PATH = os.environ['PATH']


currentProjectDir = root +'/workDir/'+ projectName


for postgresVersion in postgresVersions:

	""" Setting up system PATH variables
        This section will hold/set/modify all the build related PATHS """

	print('Setting up proper system PATH variables ...')
	os.environ['LD_LIBRARY_PATH']   = shareLib +'/lib'
	os.environ['CPPFLAGS']          = '-I'+ shareLib +'/include'
	os.environ['LDFLAGS']           = ' -L'+ shareLib +'/lib'


	dateTime = time.strftime("%Y%m%d%H%M%S")

	print('\nStarting build process for '+ postgresVersion['fullVersion'])

	print('\n\nSetting up work dir structure ...')

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
		print('\n\nBuild POSTGIS now ...')

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


	""" ****** POST BUILD STEPS ***** """
	print('****** POST BUILD STEPS *****')
	
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

			print('------------------')
			print('INSTALLER CREATION')
			print('------------------')

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
			res = os.system('source '+ signingPasswordRoot +'/signing-pass.vault && '+ bitrockInstallation +'/bin/builder build '+ installerSourcFolder +'/postgresql-installer/'+ projectFileName +' '+ tempOsTypeForInstaller +' --setvars project.outputDirectory='+ installerSourcFolder +'/postgresql-installer/installers > '+ logsDir +'/build-installer-'+ postgresVersion["majorVersion"] +'.log 2>&1')


			if res != 0:
				print('Unable to generate installer ...')

