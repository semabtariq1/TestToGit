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



# Checking operating system
print('checking operating system ...')
time.sleep(2)
osType = platform.system();
if osType != 'Windows':
    print('This code is only for Windows can not execute on current operating system '+ osType)
    exit()
print('Operating system ... '+ osType)


# Saving current state of system PATH variable
print('Saving current state of system PATH variable ...')
systemPATH = os.environ['PATH']


# Checking all the required file, directories exists or not
print('Checking Project directory ...')
time.sleep(2)
if projectName == '':
	print('Project Name ... EMPTY\nError: Project name can not be an empty value please set a value in local_env.py')
	exit()
print('Project name ... '+ projectName)

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


print('Checking PL language directory ...')
time.sleep(2)
if os.path.exists(shareLib +'\\pl-languages'):
    print('PL language directory ... ok')
    if not os.listdir(shareLib +'\\pl-languages'):
        print('PL languages directory ... Empty\nError: Provided PL languages directory is empty '+ pl_languages)
        exit()
else:
    print('PL languages directory ... NOT FOUND\nError: Provided PL languages directory does not exists '+ pl_languages)
    exit()

print('Checking PL Python directory ...')
time.sleep(2)
if os.path.exists(shareLib +'\\pl-languages\\Python-3.3'):
    print('PL Python directory ... ok')

    if not os.listdir(shareLib +'\\pl-languages\\Python-3.3'):
        print('PL Python directory ... Empty\nError: PL Python folder inside PL languages is empty '+ pl_languages)
        exit()
    os.system(shareLib +'\\pl-languages\\Python-3.3\\python --version')
else:
    print('PL Python directory ... NOT FOUND\nError: Provided PL languages folder do not have Pl Python folder '+ pl_languages)
    exit()

print('Checking PL Perl directory ...')
time.sleep(2)
if os.path.exists(shareLib +'\\pl-languages\\Perl-5.26'):
    print('PL Perl directory ... ok')

    if not os.listdir(shareLib +'\\pl-languages\\Perl-5.26'):
        print('PL Perl directory ... Empty\nError: PL Perl folder inside PL languages is empty '+ pl_languages)
        exit()
else:
    print('PL Perl directory ... NOT FOUND\nError: Provided PL languages folder do not have Pl Perl folder '+ pl_languages)
    exit()

print('Checking PL Tcl directory ...')
time.sleep(2)
if os.path.exists(shareLib +'\\pl-languages\\Tcl-8.6'):
    print('PL Tcl directory ... ok')

    if not os.listdir(shareLib +'\\pl-languages\\Tcl-8.6'):
        print('PL Tcl directory ... Empty\nError: PL Tcl folder inside PL languages is empty '+ pl_languages)
        exit()
else:
    print('PL Tcl directory ... NOT FOUND\nError: Provided PL languages folder do not have Pl Tcl folder '+ pl_languages)
    exit()


print('Checking Openssl directory ...')
time.sleep(2)
if os.path.exists(shareLib +'\\openssl'):
    print('Openssl directory ... ok')

    if not os.listdir(shareLib +'\\Openssl'):
        print('Openssl directory ... Empty\nError: Openssl folder is empty '+ pl_languages)
        exit()
else:
    print('PL Tcl directory ... NOT FOUND\nError: Openssl folder not exists '+ pl_languages)
    exit()

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
        if os.path.isfile(signingPasswordRoot +'\\signing-pass.vault'):
            print('signing-pass.vault ... ok')
            print('Creating signing-pass.vault.bat file ...')
            # Read in the file
            with open(signingPasswordRoot +'\\signing-pass.vault', 'r') as file :
                filedata = file.read()

            # Replace the target string
            filedata = filedata.replace('export', 'set')

            # Write the file out again
            with open(signingPasswordRoot +'\\signing-pass.vault.bat', 'w') as file:
                file.write(filedata)
        else:
            print('signing-pass.vault ... Not a file\nError: signing-pass.vault does not exists at give path '+ signingPasswordRoot)
            exit()
    else:
        print('Signing directory ... Not found\nError: signing directory does not exists at given path '+ signingPasswordRoot)
        exit()

    print('Checking Bitrock installation ...')
    time.sleep(2)
    if os.path.exists(bitrockInstallation):
        res = os.system(bitrockInstallation +'/bin/builder-cli --version')
        if res != 0:
            print('Bitrock version ... Not found\nError: Unable to check version of Bitrock it might be corrupted please try to re-install bitrock')
            exit()
    else:
        print('Installbuilder directory does not exists ...\nPlease provide a valid path to installbuilder installation directory ...')
        exit()
    print('Bitrock installation ... ok')

    # Creating directory for Postgres installer source code and log files
    print('Creating required directory to clone installer source code ...')
    time.sleep(2)
    installerSourcFolder = root +'\\workDir\\'+ projectName +'\\installers' # Variable which will point to installer directory inside workDir
    os.system('mkdir '+ installerSourcFolder +'\\logs')

    if os.path.exists(installerSourcFolder):
        if os.path.exists(installerSourcFolder +'\\logs'):
            print('Created ... '+ installerSourcFolder)
            print('Created ... '+ installerSourcFolder +'\\logs')
        else:
            print('Create directory ... Fails\nError: Unable to create following directory '+ installerSourcFolder +'\\logs')
            exit()
    else:
        print('Create directory ... Fails\nError: Unable to create following directory '+ installerSourcFolder)
        exit()

    # Add git in system PATH variable
    os.environ['PATH'] = 'C:\\Program Files\\Git\\bin;'+ systemPATH

    # Clone postgresql installer repo
    print('Clone Postgres installer source repository ...')
    res = os.system('cd '+ installerSourcFolder +' && git clone --recursive https://github.com/2ndQuadrant/postgresql-installer.git > '+ installerSourcFolder +'\\logs\\Installer-source-clone.log 2>&1')
    if res != 0:
        print('Could not able to clone Postgres installer repository ...')
        exit()

    # Checkout stable branch in postgresql
    os.system('cd '+ installerSourcFolder +'\\postgresql-installer && git checkout stable')

    # Checkout master branch in codesign
    os.system('cd '+ installerSourcFolder +'\\postgresql-installer\\codesign && git checkout master')

    # Restoring system PATH variable into its orignal shape
    os.environ['PATH'] = systemPATH


    # Preparing a folder hierarchy for final installers, Builds anc components
    print('Creating directory hierarchy for final installers, builds and preparing components ...')
    time.sleep(2)
    os.system('mkdir '+ installerSourcFolder +'\\postgresql-installer\\final-installers' )
    os.system('mkdir '+ installerSourcFolder +'\\postgresql-installer\\Builds\\'+ osType +'\\OmniDB')
    os.system('mkdir '+ installerSourcFolder +'\\postgresql-installer\\Builds\\'+ osType +'\\pl-languages')

    # Checking required directories are created or not
    if os.path.exists(installerSourcFolder +'\\postgresql-installer\\final-installers'):
        print('Created ... '+ installerSourcFolder +'\\postgresql-installer\\final-installers')
    else:
        print('Unable to create => '+ installerSourcFolder +'\\postgresql-installer\\final-installers')
        exit()

    if os.path.exists(installerSourcFolder +'\\postgresql-installer\\Builds\\'+ osType +'\\OmniDB'):
        print('Created ... '+ installerSourcFolder +'\\postgresql-installer\\Builds\\'+ osType +'\\OmniDB')
    else:
        print('Unable to create => '+ installerSourcFolder +'\\postgresql-installer\\Builds\\'+ osType +'\\OmniDB')
        exit()

    if os.path.exists(installerSourcFolder +'\\postgresql-installer\\Builds\\'+ osType +'\\pl-languages'):
        print('Created ... '+ installerSourcFolder +'\\postgresql-installer\\Builds\\'+ osType +'\\pl-languages')
    else:
        print('Unable to create => '+ installerSourcFolder +'\\postgresql-installer\\Builds\\'+ osType +'\\pl-languages')
        exit()


    # Preparing components for installer
    # Pl languages
    print('Prepare PL languages component ...')
    copy_tree(shareLib +'\\pl-languages', installerSourcFolder +'\\postgresql-installer\\Builds\\'+ osType +'\\pl-languages')
    if res != 0:
        print('PL languages component ... FAILS')
        exit()
    else:
        print('PL languages component ... OK')


    # OmniDB
    print('Prepare OmniDB ...')
    print('Download OmniDB ...')
    print('Getting OmniDB binaries ...')



print('\n\nPre build checks are executed successfully ...')



print('\n\n\n')

print(' ********************************************* \n')

print('           BUILDS GENERATION SECTION           \n')

print(' ********************************************* \n')


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




    print('\n\n\n')

    print(' ************************************************ \n')

    print('           INSTALLER GENERATION SECTION           \n')

    print(' ************************************************ \n')

    # Checking installer creation mode
    if installerCreationMode == 'Enabled':

        # Check if current version of PostgreSQL build needs an installer
        if postgresVersion['createInstaller'] == '1':


            # Creating required folder structure inside Postgres installer cloned folder
            print(installerSourcFolder +'\\postgresql-installer\\Builds\\'+ osType +'\\'+ postgresVersion["majorVersion"])
            os.makedirs(installerSourcFolder +'\\postgresql-installer\\Builds\\'+ osType +'\\'+ postgresVersion["majorVersion"])
            # Copy build into installerSourcFolder/postgresql-installer/Builds/ 
            print('Copy build into: '+ installerSourcFolder +'\\postgresql-installer\\Builds\\'+ osType +'\\'+ postgresVersion["majorVersion"])

            copy_tree(buildDir, installerSourcFolder +'\\postgresql-installer\\Builds\\Windows\\'+ postgresVersion["majorVersion"])


            # Re-generating installer-properties.sh
            print('Re-generating installer-properties.sh ...')
            f = open(installerSourcFolder +'\\postgresql-installer\\installer-properties.sh',"w+")

            f.write('__PG_MAJOR_VERSION__='+      postgresVersion['majorVersion']              +'\n')
            f.write('__FULL_VERSION__='+          postgresVersion['fullVersion']               +'\n')
            f.write('__EXTRA_VERSION_STRING__='+  postgresVersion['__EXTRA_VERSION_STRING__']  +'\n')
            f.write('__RELEASE__='+               postgresVersion['__RELEASE__']               +'\n')
            f.write('__BUILD_NUMBER__='+          postgresVersion['__BUILD_NUMBER__']          +'\n')
            f.write('__DEV_TEST__='+              postgresVersion['__DEV_TEST__']              +'\n')
            f.write('__DEBUG__='+                 postgresVersion['__DEBUG__']                 +'\n')

            f.close()


            # Running autogen.sh
            os.system('cd '+ installerSourcFolder +'\\postgresql-installer && autogen.sh')


            # Generating installer
            print('Build installer ...')
            res = os.system(signingPasswordRoot +'\\signing-pass.vault.bat && '+ bitrockInstallation +'\\bin\\builder-cli.exe build '+ installerSourcFolder +'\\postgresql-installer\\'+ projectFileName +' windows --setvars project.outputDirectory='+ installerSourcFolder  +'\\postgresql-installer\\final-installers  --verbose > '+ logsDir +'\\build-installer-'+ postgresVersion["majorVersion"] +'.log 2>&1')


            if res != 0:
                print('Unable to generate installer ...')
            else:
                print('Installer placed at: '+ installerSourcFolder +'\\postgresql-installer\\final-installers/PostgreSQL-'+ postgresVersion['fullVersion'] +'-'+ postgresVersion['__BUILD_NUMBER__'] +'-windows-installer.exe')
