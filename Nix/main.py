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
                print("Adding quantile support ...")
                src = paths.root + "/winShareLib/quantile"
                dest = paths.currentProject +"/"+ version[
                    'fullVersion'] + "/src/postgresql-" + version['fullVersion'] + "/contrib"
                copyFile.copy(src, dest)

                # Running configure
                print("Running configure ...")
                configuration.runConfiguration(version['fullVersion'], version["majorVersion"])

                # # Running build
                print("Running build ...")
                build.runBuild(version["fullVersion"])

                # Running regression
                # print("Running regression ...")
                # regression.runRegression(version["fullVersion"])

                # # Running install
                print("Running install ...")
                install.runInstall(version["fullVersion"])
                #
                #
                # # Running the postgres server
                print("startin postgres server")
                os.system("cd " + paths.currentProject + "/" + version["fullVersion"] + "/build/" + version[
                    "majorVersion"] + "/bin && ./initdb -D data && ./pg_ctl -D data -l logfile start ")

                # # # Adding postgis feature
                # # adding postgis
                # # Unzipping the postgis file
                print("Unzipping the postgis ...")
                os.system("tar -xf postgis-2.4.4.tar.gz --directory /opt/shared_src/ > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/unzipPostgis.log 2>&1")

                # Running configure on postgis
                print("Running configure on postgis ...")
                os.system("cd /opt/shared_src/postgis-2.4.4 && ./configure --prefix=/opt/linux_shared_lib/myTempData --with-pgconfig="+paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/bin/pg_config --with-gdalconfig=/opt/linux_shared_lib/bin/gdal-config  --with-geosconfig=/opt/linux_shared_lib/bin/geos-config --with-projdir=/opt/linux_shared_lib > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/postgisConfigure.log 2>&1")
                # print("Setting temp path of psql ..)
                # os.system("export PATH=~/postgresql/workdir/"+currentDateTime+"/"+version["fullVersion"]+"/"+"build/"+version["majorVersion"]+"/"+"bin:$PATH && printenv")


                # Running build
                print("Running make ...")
                os.system("cd /opt/shared_src/postgis-2.4.4 && make > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/postgisBuild.log 2>&1")


                # Running install
                print("Running make install ...")
                os.system("cd /opt/shared_src/postgis-2.4.4 && make install > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/postgisInstall.log 2>&1")




                # print("done")


                # # Setting Rpath
                # binPath = paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/bin"
                # print("Setting RPATH for bin")
                # for file in os.listdir(binPath):
                #     os.system('cd '+binPath+' && chrpath -r "\${ORIGIN}/../lib/" ./'+file+" > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/binRpath.log 2>&1")
                #
                # libPath = paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/lib"
                # print("Setting RPATH for lib")
                # for file in os.listdir(libPath):
                #     os.system('cd '+libPath+' && chrpath -r "\${ORIGIN}/../lib/" ./' + file+ " > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/libRpath.log 2>&1")

                # # Copying documentation
                # print("copying documentation files ...")
                # src = paths.root + "/workDir/" + currentDateTime + "/" + version[
                #     "fullVersion"] + "/src/postgresql-" + version["fullVersion"] \
                #     + "/doc/src/sgml/html"
                # dest = paths.root + "/workDir/" + currentDateTime + "/" + version[
                #     'fullVersion'] + "/build/" + version['majorVersion'] + "/doc"
                # copyFile.copy(src, dest)

                # # Generating zip file
                # print("Generating zip file ...")
                # os.system("cd "+paths.currentProject+"/"+version["fullVersion"]+" && tar -zcvf postgresql-linux.tar.gz build > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/zip.log 2>&1")
            else:
                print("Something went wrong with unzipping the postgresql")
        else:
            print("Something went wrong with downloading step please refer download.log file for more details")