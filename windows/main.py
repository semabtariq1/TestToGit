


import windows.configFile
import windows.pathVariables

import windows.srcDownloads.pullPgsqlSrc
import windows.srcDownloads.pullPython
import windows.srcDownloads.pullPerl
import windows.srcDownloads.pullDiff
import windows.srcDownloads.pullOpenssl
import windows.srcDownloads.pullZlib

import windows.srcInstallation.installPgsqlSrc
import windows.srcInstallation.installPerl
import windows.srcInstallation.installDiff
import windows.srcInstallation.installZlib
import windows.srcInstallation.installPython
import windows.srcInstallation.installOpenssl

import windows.currentDateTime

import windows.build
import windows.regression
import windows.install

import shutil
import platform
import os
import time

# Getting system properties
operatingSystem = platform.system();
# Process completed


# Initializing config file
configFile = windows.configFile.ConfigFile()
# Process ends


# Initializing path variable file
pathVariable = windows.pathVariables.PathVarriables()
# Process ends


# Initialize install pgsql
installPgsql = windows.srcInstallation.installPgsqlSrc.InstallPgsqlSrc()
# Process done


# Initialize install Perl
installPerl = windows.srcInstallation.installPerl.InstallPerl()
# Process done


# Initialize install Diff
installDiff = windows.srcInstallation.installDiff.InstallDiff()
# Process done


# Initialize install Zlib
installZlib = windows.srcInstallation.installZlib.InstallZlib()
# Process done


# Initialize install Python
installPython = windows.srcInstallation.installPython.InstallPython()
# Process done


# Initialize install Openssl
installOpenssl = windows.srcInstallation.installOpenssl.InstallOpenssl()
# Process done


# Getting saved date time
savedDateTime = windows.currentDateTime.savedDateTime
# Process ends


# Initializing build
buildProc = windows.build.Building()
# Process ends


# Initializing regression
regressionProc = windows.regression.Regression()
# Process ends


# Initializing regression
instalationProc = windows.install.Installation()
# Process ends




if operatingSystem is "Windows":

    # # Setting up folder hierarchy..
    print("Setting up folder hierarchy\n")
    print("Following directories are being created ...\n")
    for version in configFile.decoded['v']:
        directory = pathVariable.rootDirectory + "\\workDir\\"+savedDateTime+"\\"+version['fullVersion']+"\\src\\build"
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(directory)
            time.sleep(3)
    # Process endds




    # Downloading Python
    if configFile.python == 1:
        pullPython = windows.srcDownloads.pullPython.PullPython()
        pullPython.PullPython()

        # Installing Python
        installPython.installPython()
    # Process completed


    # Downloading Perl
    if configFile.perl == 1:
        pullPerl = windows.srcDownloads.pullPerl.PullPerl()
        pullPerl.pullPerl()

        # Installing Perl
        installPerl.silentInstallPerl()
    # Process completed


    # Downloading Openssl
    if configFile.openssl == 1:
        pullOpenssl = windows.srcDownloads.pullOpenssl.PullOpenSsl()
        pullOpenssl.PullOpenSsl()

        # Installing openssl
        installOpenssl.installOpenssl()
    # Process completed


    # Downloading Zlib
    if configFile.zlib == 1:
        pullZlib = windows.srcDownloads.pullZlib.PullZlib()
        pullZlib.pullZlib()

        # Installing Zlib
        installZlib.installZlib()
    # Process completed


    # Downloading Diff
    if configFile.deff == 1:
        pullDiff = windows.srcDownloads.pullDiff.PullDiff()
        pullDiff.pullDiff()

        # Initializing Diff
        installDiff.installDiff()
    # Process completed


    # Downloading Pgsql code
    if configFile.pgSql == 1:
        pullPgsqlSrc = windows.srcDownloads.pullPgsqlSrc.PullPgsqlSourceCode()
        pullPgsqlSrc.pullCode()

        # Installing PGSQL
        installPgsql.unzipPgsqlSrc()
    # Process completed

    # Generating envoirnment files
    for version in configFile.decoded['v']:
        print("Generating envoirnment file for version ...", version['fullVersion'])
        f = open(os.path.dirname(os.path.abspath(__file__))+"\\workDir\\"+savedDateTime+"\\"+version['fullVersion']+"\\src\\postgresql-"+version['fullVersion']+"\\src\\tools\\msvc\\buildenv.pl", "w+")
        f.write("$ENV{PATH}=$ENV{PATH} . ';C:\Program Files (x86)\GnuWin32\\bin';")
        time.sleep(3)
        f.close()
    # Process ends


    # Build + Regression + installation
    for version in configFile.decoded['v']:
        print("Build + Regression + Installation for version ... ", version['fullVersion'])
        print("\n\nStarting build process ...")
        time.sleep(3)
        buildProc.startBuildProcess(version['fullVersion'])
        print("Build process completed")

        print("\n\nStarting regression test ...")
        time.sleep(3)
        regressionProc.startRegresstion(version['fullVersion'])
        print("Regression process completed")

        print("\n\nStarting instalation ...")
        time.sleep(3)
        instalationProc.startInstation(version['fullVersion'])
        print("Installation process completed")
    # Process ends


    # Finall message
    print("\n\nAutomation process is completed ...")


elif operatingSystem is "Linux":
    print("Welcome to Linux");
else:
    print("Undefined platform found = ", os);