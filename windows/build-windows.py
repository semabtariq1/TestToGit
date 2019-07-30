import os
import json
import time
import requests
import tarfile
import shutil
import subprocess
from local_env import *
from distutils.dir_util import copy_tree



print('\n\n\n')

print(' ************************************* \n')

print('           PRE BUILD SECTION           \n')

print(' ************************************* \n')


# Checking all the required file, directories exists or not
print('Checking Project directory ...')
time.sleep(2)
if os.path.exists(root +'/workDir/'+ projectName):
	print('Project directory ... Already exist\nPlease specify different name for project in projectName variable inside local_env.py file')
	exit()
else:
	print('Project directory ... ok')


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


print('\n\nPre build checks are executed successfully ...')


# Saving current state of system PATH variable
print('Saving current state of system PATH variable ...')
systemPATH = os.environ['PATH']


""" Reading postgreSQ versions from postgres_versions.json """
with open('postgres_versions.json', 'r') as postgresVersions:
	postgresVersions = json.load(postgresVersions)


# Checking if installers creation mode is Enabled or Disabled
installerCreationMode = 'Disabled'
for postgresVersion in postgresVersions:

    if postgresVersion['createInstaller'] == '1':
        installerCreationMode = 'Enabled'
        break

print('Installer creation mode ... '+ installerCreationMode)


# Running check if Installer creation mode is Enabled
if installerCreationMode == 'Enabled':

    # Add git in system PATH variable
    os.environ['PATH'] = 'C:\\Program Files\\Git\\bin;'+ systemPATH

    # Creating a directory if not exists and clone installer code from GitHub
    installerSourcFolder = root +'\\workDir\\'+ projectName +"\\installers"
    print('Clone Postgres installer source repository from GitHub ...')
    os.makedirs(installerSourcFolder)
    res = os.system('cd '+ installerSourcFolder +' && git clone --recursive https://github.com/2ndQuadrant/postgresql-installer.git')
    if res != 0:
        print('Could not able to clone Postgres installer repository ...')
        exit()

    # Checkout stable branch and Getting latest commit hash
    os.system('cd '+ installerSourcFolder +'\\postgresql-installer && git checkout stable')
    latestCommitHash = subprocess.check_output('cd '+ installerSourcFolder +'\\postgresql-installer && git rev-parse HEAD', shell=True)
    print('latest commit hash: '+ latestCommitHash.decode("utf-8"))

    # Restoring system PATH variable into its orignal shape
    os.environ['PATH'] = systemPATH


currentProjectDir = root +'\\workDir\\'+ projectName


for postgresVersion in postgresVersions:

    print('\n\nStarting build process for '+ postgresVersion['fullVersion'])


    print('\nSetting up work dir structure ...')
    dateTime = time.strftime("%Y%m%d%H%M%S")
    currentBuild = currentProjectDir +'\\'+ dateTime +'\\'+ postgresVersion['fullVersion']
    sourceDir = currentBuild +'\\'+ 'source'
    logsDir = currentBuild +'\\'+ 'logs'
    buildDir = currentBuild +'\\'+ 'build' +'\\'+ postgresVersion['majorVersion']

    os.makedirs(sourceDir)
    os.makedirs(logsDir)
    os.makedirs(buildDir)
    print(buildDir +'\n'+ logsDir +'\n'+ sourceDir)


    # Downloading postgreSQL source code
    print('Downloading source code ...')
    req = requests.get(postgresVersion["tarball"])
    with open(sourceDir +'\\postgresql-'+ postgresVersion["fullVersion"] +'.tar.gz', 'wb') as tarBall:
        tarBall.write(req.content)


    # Unzipping postgreSQL
    print('Unzipping source code ...')
    tar = tarfile.open(sourceDir +'\\postgresql-'+ postgresVersion["fullVersion"] +'.tar.gz', "r:gz")
    tar.extractall(sourceDir)
    tar.close()


    # These variables will hold system PATHS
    opensslPATH = ''
    icuPATH     = ''
    zlibPATH    = ''
	
	
    # Adding paths in config_default.pl file
    print("Updating config_default.pl file")
    number = 0
    configDefault = sourceDir +'\\postgresql-'+ postgresVersion['fullVersion'] +'\\src\\tools\\msvc\\config_default.pl'
    file = open(configDefault)
    line = file.read().splitlines()
    for li in line:
        if 'python' in li:
            if postgresVersion['PYTHON'] == '1':
                line[number] = "    python    => '"+ shareLib +"\\pl-languages\\Python-3.3',    # --with-python=<path>"
                open(configDefault, 'w').write('\n'.join(line))

        elif "openssl" in li:
            if postgresVersion['OPENSSL'] == '1':
                line[number] = "    openssl   => '"+ shareLib +"\\openssl',    # --with-openssl=<path>"
                open(configDefault, 'w').write('\n'.join(line))

                # Copying Openssl binaries in build
                src = shareLib +"\\openssl"
                copy_tree(src, buildDir)

                # Setting PATH variable
                opensslPATH = shareLib +'\\openssl\\bin;'

        elif "icu" in li:
            if postgresVersion['ICU'] == '1':
                line[number] = "    icu       => '"+ shareLib +"\\icu',    # --with-icu=<path>"
                open(configDefault, 'w').write('\n'.join(line))

                # Copying icu binaries in build
                src = shareLib +"\\icu\\bin64\\"
                copy_tree(src, buildDir +'\\bin')
				
                # Setting PATH variable
                icuPATH = shareLib +'\\icu\\bin64;'
				
        elif "perl" in li:
            if postgresVersion['PERL'] == '1':
                line[number] = "    perl      => '"+ shareLib +"\\pl-languages\\perl-5.26',    # --with-perl=<path>"
                open(configDefault, 'w').write('\n'.join(line))

        elif "tcl" in li:
            if  postgresVersion['TCL'] == '1':
                line[number] = "    tcl       => '"+ shareLib +"\\pl-languages\\Tcl-8.6',    # --with-tcl=<path>"
                open(configDefault, 'w').write('\n'.join(line))

        elif "zlib" in li:
            if postgresVersion['ZLIB'] == '1':
                line[number] = "    zlib      => '"+ shareLib +"\\zlib'    # --with-zlib=<path>"
                open(configDefault, 'w').write('\n'.join(line))

                # Copying Zlib binaries in build
                src = shareLib +"\\zlib"
                copy_tree(src, buildDir)
				
                # Setting PATH variable
                zlibPATH    = shareLib +'\\zlib\\bin;'
				

        number += 1;
    file.close()


    # Modifying system PATH variable
    print('Modify system PATH variable ...')
    os.environ['PATH'] = buildDir +'\\bin;'+ shareLib +'\\extra_utils\\bin;'+ opensslPATH + icuPATH + zlibPATH + systemPATH
	
	
    # Copying quantile binaries in build
    if postgresVersion['QUANTILE'] == 1:
        print("Copying QUANTILE binaries in build ...")
        if postgresVersion['majorVersion'] == '9.5':
            src = shareLib +"\\quantile"
        else:
            src = shareLib +"\\quantile-parallel"
        dest = sourceDir +'\\postgresql-'+ postgresVersion['fullVersion'] +"\\contrib\\quantile"
        copy_tree(src, dest)

	
    # Running build on PostgreSQL
    print('Running build ...')
    res = os.system(windowsCmd +' /c '+'" cd /d '+ vsCommandPromptX64 +' && vcvarsall amd64 && cd /d '+ sourceDir +'\\postgresql-'+ postgresVersion['fullVersion'] +'\\src\\tools\\msvc && build > '+ logsDir +'\\PostgreSQL_build.log 2>&1"')
    if res != 0:
        print('Something went wrong with PostgreSQL build please see: '+ logsDir +'\\PostgreSQL_build.log')
        exit()

		
    # Running make check on PostgreSQL
    print('Running vcregress check ...')
    res = os.system(windowsCmd +' /c '+'" cd /d '+ vsCommandPromptX64 +' && vcvarsall amd64 && cd /d '+ sourceDir +'\\postgresql-'+ postgresVersion['fullVersion'] +'\\src\\tools\\msvc && vcregress check  > '+ logsDir +'\\PostgreSQL_regression.log 2>&1"')
    if res != 0:
        print('Something went wrong with PostgreSQL regression tests please see: '+ logsDir +'\\PostgreSQL_regression.log')
        exit()


    # Running make install on PostgreSQL
    print("Running make install ...")
    res = os.system(windowsCmd +' /c '+'" cd /d '+ vsCommandPromptX64 +' && vcvarsall amd64 && cd /d '+ sourceDir +'\\postgresql-'+ postgresVersion['fullVersion'] +'\\src\\tools\\msvc && install '+ buildDir +' > '+ logsDir +'\\PostgreSQL_install.log 2>&1"')
    if res != 0:
        print('Something went wrong with PostgreSQL installation please see: '+ logsDir +'\\PostgreSQL_install.log')
        exit()


    # Adding PostGIS support
    if postgresVersion['POSTGIS'] == '1':
        print("Adding PostGIS support ...")
        src = shareLib +"\\postgis-"+ postgresVersion['majorVersion']
        copy_tree(src, buildDir)


    # Generating zip
    print('Generating zip file for build ...')
    shutil.make_archive(currentBuild +'\\Windows-'+ postgresVersion['fullVersion'], 'zip', currentBuild +'\\build')


    # Restoring system PATH variable into default state
    os.environ['PATH'] = systemPATH


    # --------------------------
    # Installer creation section
    # --------------------------


    # Checking installer creation mode
    if installerCreationMode == 'Enabled':

        # Check if current version of PostgreSQL build needs an installer
        if postgresVersion['createInstaller'] == '1':

            print('------------------')
            print('INSTALLER CREATION')
            print('------------------')

            # Creating required folder structure inside Postgres installer clone repo
            print(installerSourcFolder +'\\postgresql-installer\\Builds\\Windows\\'+ postgresVersion["majorVersion"])
            os.makedirs(installerSourcFolder +'\\postgresql-installer\\Builds\\Windows\\'+ postgresVersion["majorVersion"])

            # Copy build into installerSourcFolder\postgresql-installer\Builds\Windows
            print('Copy build into: '+ installerSourcFolder +'\\postgresql-installer\\Builds\\Windows\\'+ postgresVersion["majorVersion"])
            copy_tree(buildDir, installerSourcFolder +'\\postgresql-installer\\Builds\\Windows\\'+ postgresVersion["majorVersion"])