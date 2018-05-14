


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


    print("Downloading required tools")

    # Downloading Python
    if configFile.python == 1:
        pullPython = windows.srcDownloads.pullPython.PullPython()
        pullPython.PullPython()

        # Installing Python
        installPython.installPython()

    else:
        print("Skipping Python")
    # Process completed


    # Downloading Perl
    if configFile.perl == 1:
        pullPerl = windows.srcDownloads.pullPerl.PullPerl()
        pullPerl.pullPerl()

        # Installing Perl
        installPerl.silentInstallPerl()

    else:
        print("Skipping Perl")
    # Process completed


    # Downloading Openssl
    if configFile.openssl == 1:
        pullOpenssl = windows.srcDownloads.pullOpenssl.PullOpenSsl()
        pullOpenssl.PullOpenSsl()

        # Installing openssl
        installOpenssl.installOpenssl()

    else:
        print("Skipping Openssl")
    # Process completed


    # Downloading Zlib
    if configFile.zlib == 1:
        pullZlib = windows.srcDownloads.pullZlib.PullZlib()
        pullZlib.PullZlib()

        # Installing Zlib
        installZlib.installZlib()

    else:
        print("Skipping Zlib")
    # Process completed


    # Downloading Diff
    if configFile.deff == 1:
        pullDiff = windows.srcDownloads.pullDiff.PullDiff()
        pullDiff.pullDiff()

        # Initializing Diff
        installDiff.installDiff()

    else:
        print("Skipping Diff")
    # Process completed


    # Downloading Pgsql code
    if configFile.pgSql == 1:
        pullPgsqlSrc = windows.srcDownloads.pullPgsqlSrc.PullPgsqlSourceCode()
        pullPgsqlSrc.pullCodeAndUnzip()

        # Installing PGSQL
        installPgsql.unzipPgsqlSrc()

    else:
        print("Skipping Pgsql source code")
    # Process completed


    # Setting up folder hierarchy
    print("Setting up folder hierarchy\n")
    print("Following directories are being created ...\n")

    directory = pathVariable.rootDirectory + "\\workDir\\" + savedDateTime + "\\version\\src\\build"
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(directory)
        time.sleep(3)
    # Process endds


    # Removig setup.exe files from root directory to setup folder
    # try:
    #
    #      print("removing files from root directory to setup folder required files")
    #      files = ['ActivePerl-5.24.3.2404-MSWin32-x64-404865.exe', 'diffutils-2.8.7-1.exe', 'postgresql-10.3.tar.gz', 'python-3.3.0.amd64.msi',
    #              'Win32OpenSSL-1_1_0h.exe', 'zlib-1.2.3.exe']
    #      # Creating setup folder
    #      directory = pathVariable.rootDirectory + "\\setup"
    #      if not os.path.exists(directory):
    #         os.makedirs(directory)
    #      # Process ends
    #
    #      for word in files:
    #          shutil.move(pathVariable.rootDirectory + "\\" + word, pathVariable.rootDirectory + "\\setup")
    #          #copy(pathVariable.rootDirectory + "\\" + word, pathVariable.rootDirectory + "\\setup")
    #      time.sleep(3)
    #      print("Files copied")
    #
    # except:
    #     print("No file to copy")
    # Process ends



    # Generating envoirnment file
    print("Generating envoirnment file")
    f = open(pathVariable.pgSqlMsvc+"\\buildenv.pl", "w+")
    f.write("$ENV{PATH}=$ENV{PATH} . ';C:\Program Files (x86)\GnuWin32\\bin';")
    time.sleep(3)
    f.close()
    # Process ends


    # Starting build process
    print("\n\nStarting build process ...")
    time.sleep(3)
    buildProc.startBuildProcess()
    # Process ends


    # Start regression
    print("\n\nStarting regression test ...")
    time.sleep(3)
    regressionProc.startRegresstion()
    # Process ends


    # Start install
    print("\n\nStarting instalation ...")
    time.sleep(3)
    instalationProc.startInstation()
    # Proces ends


    # Finall message
    print("\n\nAutomation process is completed ...")


elif operatingSystem is "Linux":
    print("Welcome to Linux");
else:
    print("Undefined platform found = ", os);