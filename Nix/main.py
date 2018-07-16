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
import sys

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


os.environ['PYTHON_HOME']="/opt/Python-3.4.4/inst"
os.environ['OPENSSL_HOME']="/opt/openssl-1.0.2g/inst"
os.environ['PATH']=os.environ['PYTHON_HOME'] +"/bin:" + os.environ['OPENSSL_HOME'] + "/bin:" + paths.shareLib + "/bin:" + os.environ['PATH'] 
os.environ['LD_LIBRARY_PATH']=os.environ['PYTHON_HOME'] +"/lib:" + os.environ['OPENSSL_HOME'] + "/lib:" + paths.shareLib + "/lib:"
os.environ['LDFLAGS']="-Wl,-rpath," + os.environ['PWD'] + " -L" + os.environ['PYTHON_HOME'] + "/lib/ -L" + os.environ['OPENSSL_HOME'] + "/lib" + " -L" + paths.shareLib + "/lib"
os.environ['CPPFLAGS']="-I"+os.environ['PYTHON_HOME'] + "inlclude/python3.4m" + " -I"+ os.environ['OPENSSL_HOME'] + "/include/" + " -I" + paths.shareLib + "/include"
os.environ['PYTHON']=os.environ['PYTHON_HOME']+"/bin/python3"

print("PATH=" + os.environ['PATH'])
print("LD_LIBRARY_PATH=" + os.environ['LD_LIBRARY_PATH'])
print("LDFLAGS=" + os.environ['LDFLAGS'])
print("CPPFLAGS=" + os.environ['CPPFLAGS'])
print("PYTHON=" + os.environ['PYTHON'])
os.system('env')

#Setting up folder structure
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
        downloadResult = srcDownload.download(version["url"], version["fullVersion"])

        if downloadResult == 0:
            # unzipping the postgresql
            print("Unzipping the postgresql ...")
            resultUnzip = srcInstallation.unzipPostgresql(version["fullVersion"])

            if resultUnzip == 0:
                # Downloading postgis
                print("Downloading postgis ...")
                postgisVersion = ""
                for postgis in configFile.decodedPostgis['postgisV']:
                    srcDownload.download(postgis["url"], version["fullVersion"])
                    postgisVersion = postgis["fullVersion"]

                    # Unzipping postgis
                    print("Unzipping postgis ...")
                    srcInstallation.unzipPostgis(version["fullVersion"], postgis["fullVersion"])

		# set environment variables	
                # Running configure
                print("Running configure ...")
                configuration.runConfiguration(version['fullVersion'], version["majorVersion"])

                # Running build
                print("Running build ...")
                build.runBuild(version["fullVersion"])

                # Running regression
                print("Running regression ...")
                regression.runRegression(version["fullVersion"])

                # Running install
                print("Running install ...")
                install.runInstall(version["fullVersion"])

		# unset environment variables
                print("\n*********************************************************************\n")
                print("\n                       Adding Postgis feature                        \n")
                print("\n*********************************************************************\n")


                # Running configure on postgis
                print("Running configure on postgis ...")
                os.system("cd "+paths.currentProject+"/"+version["fullVersion"]+"/src/postgis-"+postgisVersion+" && ./configure --prefix=/opt/linux_shared_lib --with-pgconfig="+paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/bin/pg_config --with-gdalconfig=/opt/PGInstaller/Python-automation-code/linux_share_lib1/bin/gdal-config  --with-geosconfig=/opt/PGInstaller/Python-automation-code/linux_share_lib1/bin/geos-config --with-projdir=/opt/PGInstaller/Python-automation-code/linux_share_lib1 --with-xml2config=/opt/PGInstaller/Python-automation-code/linux_share_lib1/bin/xml2-config > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/postgisConfigure.log 2>&1")

                # Running build
                print("Running make ...")
                os.system("cd "+paths.currentProject+"/"+version["fullVersion"]+"/src/postgis-"+postgisVersion+" && make > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/postgisBuild.log 2>&1")

                # Running regression
                print("Running regression ...")
                os.system("cd " + paths.currentProject + "/" + version[
                    "fullVersion"] + "/src/postgis-" + postgisVersion + " && make check > " + paths.currentProject + "/" +
                          version["fullVersion"] + "/logs/postgisRegression.log 2>&1")

                # Running install
                print("Running make install ...")
                os.system("cd "+paths.currentProject+"/"+version["fullVersion"]+"/src/postgis-"+postgisVersion+" && make install > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/postgisInstall.log 2>&1")


                # Copying required libraries to build
                print("Copying required libraries to build ...")
                src = paths.shareLib + "/lib/*"
                dest = ""+paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/lib/"
                #copyFile.copy(src, dest)
                os.system("cp -rv " + src + " " + dest + " > " + paths.currentProject+"/"+version["fullVersion"]+"/logs/sharedlibCopy.log 2>&1")

                # Copying share/gdal
                print("Copying sharedLib/share/gdal to build")
                src = paths.shareLib+ "/share/gdal"
                dest = ""+paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/share"
                #copyFile.copy(src, dest)
                os.system("cp -r "+src+" "+dest+"")

                 # Copying share/proj
                print("Copying sharedLib/share/proj to build")
                src = paths.shareLib+ "/share/proj"
                dest = ""+paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/share"
                #copyFile.copy(src, dest)
                os.system("cp -r "+src+" "+dest+"")


              

 
                # Copying openssl
                src = "/opt/openssl-1.0.2g/inst/lib"
                dest = paths.root+ "/workDir/" + currentDateTime + "/" + version['fullVersion'] + "/build/" + version['majorVersion'] + "/lib"
                copyFile.copy(src, dest)


                # Setting Rpath
                binPath = paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/bin"
                print("Setting RPATH for bin ...")
                for file in os.listdir(binPath):
                    os.system('cd '+binPath+' && chrpath -r "\${ORIGIN}/../lib/" ./'+file+" >> "+paths.currentProject+"/"+version["fullVersion"]+"/logs/binRpath.log 2>&1")

                libPath = paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/lib"
                print("Setting RPATH for lib ...")
                for file in os.listdir(libPath):
                    os.system('cd '+libPath+' && chrpath -r "\${ORIGIN}/../lib/" ./' + file+ " >> "+paths.currentProject+"/"+version["fullVersion"]+"/logs/libRpath.log 2>&1")

                libPostgresql =  paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/lib/postgresql"
             
                print("Setting RPATH for lib/postgresql ...")
                for file in os.listdir(libPostgresql):
                    os.system('cd '+libPostgresql+' && chrpath -r "\${ORIGIN}/../../lib/" ./' + file+ " >> "+paths.currentProject+"/"+version["fullVersion"]+"/logs/postgresqlRpath.log 2>&1")


                
              
                # Removing extra files
                os.system("rm -rf postgresql-"+version["fullVersion"]+".tar.gz postgis-"+postgisVersion+".tar.gz")


                # Generating zip file
                print("Generating zip file ...")
                os.system("cd "+paths.currentProject+"/"+version["fullVersion"]+" && tar -zcvf postgresql-linux.tar.gz build > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/zip.log 2>&1")

                # Final message
                print("All binaries are placed at : " + dirBuild)
            else:
                print("Something went wrong with unzipping the postgresql")
        else:
            print("Something went wrong with downloading step please refer download.log file for more details")
