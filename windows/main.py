


import windows.configFile
import windows.pathVariables

import windows.srcDownloads.downloadFile

import windows.srcInstallation.installPgsqlSrc
import windows.srcInstallation.installPerl
import windows.srcInstallation.installSoftware


import windows.currentDateTime

import windows.build
import windows.regression
import windows.install

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

# Initialize install software
installSoftware = windows.srcInstallation.installSoftware.InstallSoftware()
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
        rootPathSrc = pathVariable.rootDirectory + "\\workDir\\"+savedDateTime+"\\"+version['fullVersion']+"\\src"
        rootPathBuild = pathVariable.rootDirectory + "\\workDir\\" + savedDateTime + "\\" + version['fullVersion']+"\\build\\"+version['majorVersion']
        installationLogs = pathVariable.rootDirectory+ "\\workDir\\"+savedDateTime+"\\"+version['fullVersion']+"\\logs"
        if not os.path.exists(rootPathSrc):
            os.makedirs(rootPathSrc)
            print(rootPathSrc)
            time.sleep(3)
        # Setting build folder
        if not os.path.exists(rootPathBuild):
            os.makedirs(rootPathBuild)
            print(rootPathBuild)
            time.sleep(3)
        # Setting log directory
        if not os.path.exists(installationLogs):
            os.makedirs(installationLogs)
            print(installationLogs)
            time.sleep(3)
    # Process endds




    # Downloading Python
    if configFile.python[0] == "1":
        downloadFile = windows.srcDownloads.downloadFile.DownloadFile()
        downloadFile.downloadFile(configFile.python[1], configFile.python[2])
        # Installation
        path = pathVariable.windowsCmd + " /c cd " + pathVariable.rootDirectory
        command = ' && python-3.3.0.amd64.msi /qn'
        installSoftware.installSoftware("Python", path+command)

    # Downloading Perl
    if configFile.perl[0] == "1":
        downloadFile = windows.srcDownloads.downloadFile.DownloadFile()
        downloadFile.downloadFile(configFile.perl[1], configFile.perl[2])



        # Installing Perl
        #installPerl.silentInstallPerl()
    # Process completed


    # Downloading Openssl
    if configFile.openssl[0] == "1":
        downloadFile = windows.srcDownloads.downloadFile.DownloadFile()
        downloadFile.downloadFile(configFile.openssl[1], configFile.openssl[2])
        # Installation
        path = pathVariable.windowsCmd + " /c cd " + pathVariable.rootDirectory
        command = ' && Win32OpenSSL-1_1_0h.exe /SILENT, /VERYSILENT'
        installSoftware.installSoftware("Openssl", path + command)


    # Downloading Zlib
    if configFile.zlib[0] == "1":
        downloadFile = windows.srcDownloads.downloadFile.DownloadFile()
        downloadFile.downloadFile(configFile.zlib[1], configFile.zlib[2])
        # Installation
        path = pathVariable.windowsCmd + " /c cd " + pathVariable.rootDirectory
        command = ' && zlib-1.2.3.exe /SILENT, /VERYSILENT'
        installSoftware.installSoftware("Zlib", path + command)


    # Downloading Diff
    if configFile.diff[0] == "1":
        downloadFile = windows.srcDownloads.downloadFile.DownloadFile()
        downloadFile.downloadFile(configFile.diff[1], configFile.diff[2])
        # Installation
        path = pathVariable.windowsCmd + " /c cd " + pathVariable.rootDirectory
        command = ' && diffutils-2.8.7-1.exe /SILENT, /VERYSILENT'
        installSoftware.installSoftware("Diff", path + command)


    # Downloading Pgsql code
    if configFile.pgSql == 1:
        downloadFile = windows.srcDownloads.downloadFile.DownloadFile()
        for version in configFile.decoded['v']:
            link = "https://ftp.postgresql.org/pub/source/v" + version['fullVersion'] + "/postgresql-" + version[
                'fullVersion'] + ".tar.gz"
            downloadFile.downloadFile(link, "postgres-"+version['fullVersion']+".tar.gz")
            #installPgsql.unzipPgsqlSrc()






    # Generating envoirnment files
    # for version in configFile.decoded['v']:
    #     print("Generating envoirnment file for version ...", version['fullVersion'])
    #     f = open(os.path.dirname(os.path.abspath(__file__))+"\\workDir\\"+savedDateTime+"\\"+version['fullVersion']+"\\src\\postgresql-"+version['fullVersion']+"\\src\\tools\\msvc\\buildenv.pl", "w+")
    #     f.write("$ENV{PATH}=$ENV{PATH} . ';C:\Program Files (x86)\GnuWin32\\bin';")
    #     time.sleep(3)
    #     f.close()
    # Process ends


    # Build + Regression + installation
    # for version in configFile.decoded['v']:
    #     print("Build + Regression + Installation for version ... ", version['fullVersion'])
    #     print("\n\nRunning build ...")
    #     time.sleep(3)
    #     buildProc.startBuildProcess(version['fullVersion'])
    #
    #
    #     print("\n\nRunning regression ...")
    #     time.sleep(3)
    #     regressionProc.startRegresstion(version['fullVersion'])
    #
    #
    #     print("\n\nRunning instalation ...")
    #     time.sleep(3)
    #     instalationProc.startInstation(version['fullVersion'], version['majorVersion'])

    # Process ends


    # Finall message
    print("\n\nAutomation process is completed ...")


elif operatingSystem is "Linux":
    print("Welcome to Linux");
else:
    print("Undefined platform found = ", os);