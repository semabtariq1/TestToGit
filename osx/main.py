import os

import configFile
import paths
import currentDateTime
import srcDownload.download
import srcInstallation.installation
import copyFile
import configuration
import regression
import build
import install


install = install.Install()
build = build.Build()
regression = regression.Regression()
configuration = configuration.Configuration()
copyFile = copyFile.CopyFile()
srcInstallation = srcInstallation.installation.Install()
srcDownload = srcDownload.download.Download()
currentDateTime = currentDateTime.savedDateTime
configFile = configFile.ConfigFile()
paths = paths.Path()


# Setting up folder structure
print("Setting up folder structure")
for version in configFile.decoded['v']:
    dirSrc = paths.root+ "/workDir/"+currentDateTime+ "/"+ version['fullVersion']+"/src"
    dirLog = paths.root+ "/workDir/"+currentDateTime+ "/"+ version['fullVersion']+"/logs"
    dirBuild = paths.root + "/workDir/" + currentDateTime + "/" + version[
        'fullVersion'] + "/build/" + version['majorVersion']

    if not os.path.exists(dirSrc):
        os.makedirs(dirSrc)
        print(dirSrc)
    if not os.path.exists(dirLog):
        os.makedirs(dirLog)
        print(dirLog)
    if not os.path.exists(dirBuild):
        os.makedirs(dirBuild)
        print(dirBuild)



#

if configFile.postgresql == 1:
    print("Downloading postgres ...")
    for version in configFile.decoded['v']:
        # downloadResult = srcDownload.download(version["url"], version["fullVersion"])
        downloadResult = 0

        if downloadResult == 0:


            # unzipping the postgresql
            print("Unzipping the postgresql ...")
            resultUnzip = srcInstallation.unzipPostgresql(version["fullVersion"])

            if resultUnzip == 0:
                # Downloading ReadLine
                # print("Installing ReadLine")
                # srcInstallation = srcInstallation.installdReadline(version["fullVersion"])

                # Copying the quantile folder
                # print("Adding quantile support ...")
                # src = paths.root + "/winShareLib/quantile"
                # dest = paths.currentProject +"/"+ version[
                #     'fullVersion'] + "/src/postgresql-" + version['fullVersion'] + "/contrib"
                # copyFile.copy(src, dest)

                # Running configure
                print("Running configure ...")
                configuration.runConfiguration(version['fullVersion'], version["majorVersion"])

                # # Running build
                print("Running build ...")
                build.runBuild(version["fullVersion"])


                # # Running install
                print("Running install ...")
                install.runInstall(version["fullVersion"])
                #
                #
                # # Running the postgres server
                print("starting postgres server")
                os.system("cd " + paths.currentProject + "/" + version["fullVersion"] + "/build/" + version[
                    "majorVersion"] + "/bin && ./initdb -D data && ./pg_ctl -D data -l logfile start ")
                #
                # # # # Adding postgis feature
                # # # adding postgis

                # # Running configure on postgis
                print("Running configure on postgis ...")
                os.system("cd /Users/2ndquadrant/pythonAutomation/src/postgis/src/postgis-2.4.4 && ./configure --prefix=/Users/2ndquadrant/pythonAutomation/srcBuild --with-pgconfig="+paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/bin/pg_config --with-gdalconfig=/Users/2ndquadrant/pythonAutomation/srcBuild/bin/gdal-config  --with-geosconfig=/Users/2ndquadrant/pythonAutomation/srcBuild/bin/geos-config --with-projdir=/Users/2ndquadrant/pythonAutomation/srcBuild > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/postgisConfigure.log 2>&1")


                #
                # Running build
                print("Running make ...")
                os.system("cd /Users/2ndquadrant/pythonAutomation/src/postgis/src/postgis-2.4.4 && make > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/postgisBuild.log 2>&1")

                #
                # # Running install
                print("Running make install ...")
                os.system("cd /Users/2ndquadrant/pythonAutomation/src/postgis/src/postgis-2.4.4 && make install > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/postgisInstall.log 2>&1")

                #
                # # # Copying required libraries to build
                print("Copying required libraries to build ...")
                src= "/Users/2ndquadrant/pythonAutomation/srcBuild"
                dest = ""+paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/"
                copyFile.copy(src, dest)

            else:
                print("Something went wrong with unzipping the postgresql")
        else:
            print("Something went wrong with downloading step please refer download.log file for more details")