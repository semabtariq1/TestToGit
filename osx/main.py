import os
import time
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
import smtplib

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



print("\n*********************************************************************\n")
print("\n                        Starting automation                          \n")
print("\n*********************************************************************\n")
time.sleep(3)

# Setting up folder structure
dirBuild = ""
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
        #downloadResult = srcDownload.download(version["url"], version["fullVersion"])
        result = os.system("curl -O  "+ version["url"] +" > "+paths.currentProject+ "/"+ version["fullVersion"] +"/logs/PostgresqlDownload.log 2>&1")

        if result == 0:
            # unzipping the postgresql
            print("Unzipping the postgresql ...")
            #resultUnzip = srcInstallation.unzipPostgresql(version["fullVersion"])
            result = os.system("tar xzf postgresql-"+ version["fullVersion"] +".tar.gz --directory "+paths.currentProject +"/"+ version["fullVersion"] +"/src")


            if result == 0:
                # Downloading postgis
                print("Downloading postgis ...")
                postgisVersion = ""
                for postgis in configFile.decodedPostgis['postgisV']:
                    #srcDownload.download(postgis["url"], version["fullVersion"])
                    result = os.system("curl -O  "+ postgis["url"] +" > "+paths.currentProject+ "/"+ version["fullVersion"] +"/logs/PostgisDownload.log 2>&1")
                    postgisVersion = postgis["fullVersion"]

                    if result == 0:
                 

                        # Unzipping postgis
                        print("Unzipping postgis ...")
                        #srcInstallation.unzipPostgis(version["fullVersion"], postgis["fullVersion"])
                        result = os.system("tar xzf postgis-"+ postgis["fullVersion"] +".tar.gz --directory "+paths.currentProject +"/"+ version["fullVersion"] +"/src")
                        
                        if result == 0:

                            # Setting paths
                            buildLocation = paths.currentProject+"/"+version["fullVersion"]+"/build/"+version['majorVersion']
                            os.environ['PATH'] = paths.currentProject + "/" + version["fullVersion"] + "/build/"+ version["majorVersion"] + "/bin:"+ os.environ['PATH']
                            os.environ['PYTHON_HOME'] = "/Users/2ndquadrant/2UDA/Python-3.4.4/inst"
                            os.environ['OPENSSL_HOME'] = "/Users/2ndquadrant/2UDA/openssl-1.0.2g/inst"
                            os.environ['LD_LIBRARY_PATH'] = os.environ['PYTHON_HOME'] + "/lib:" + os.environ['OPENSSL_HOME'] + "/lib:/Users/2ndquadrant/pythonAutomation/srcBuild/lib"
                            os.environ['LDFLAGS'] = "-Wl,-rpath," + buildLocation + " -L" + os.environ['PYTHON_HOME'] + "/lib -L" + os.environ['OPENSSL_HOME'] + "/lib -L/Users/2ndquadrant/pythonAutomation/srcBuild/lib"
                            os.environ['CPPFLAGS'] = "-I" + os.environ['PYTHON_HOME'] + "/include/python3.4m" + " -I" + os.environ['OPENSSL_HOME'] + "/include -I/Users/2ndquadrant/pythonAutomation/srcBuild/include"
                            os.environ['PYTHON'] = "/Users/2ndquadrant/2UDA/Python-3.4.4/inst/bin/python3"
                            
                            # Running configure
                            print("Running configure ...")
                           
                            configPath = paths.currentProject+"/"+ version["fullVersion"] +"/src/postgresql-"+version["fullVersion"]
                            configCommand = "./configure  --with-openssl --with-python --with-zlib --prefix="+paths.currentProject+"/"+ version["fullVersion"] +"/build/"+ version["majorVersion"] +" > "+paths.currentProject+"/"+ version["fullVersion"] +"/logs/PostgresqlConfigure.log 2>&1"
                            result = os.system("cd "+configPath+" && "+configCommand+"")
                          
                            if result == 0:
                                # Running build
                                print("Running build ...")
                                buildPath = paths.currentProject + "/" + version["fullVersion"] + "/src/postgresql-" + version["fullVersion"]
                                command = " make world > "+paths.currentProject+"/"+ version["fullVersion"] +"/logs/PostgresqlBuild.log 2>&1"
                                result = os.system("cd "+buildPath+" && "+command+"")

                                if result == 0:
                                    # Running install
                                    print("Running install ...")
                                    buildPath = paths.currentProject + "/" + version["fullVersion"] + "/src/postgresql-" + version["fullVersion"]
                                    command = " make install-world > "+paths.currentProject+"/"+ version["fullVersion"] +"/logs/PostgresqlInstall.log 2>&1"
                                    result = os.system("cd "+buildPath+" && "+command+"")
 
                                    if result == 0:
                                        print("\n*********************************************************************\n")
                                        print("\n                       Adding Postgis feature                        \n")
                                        print("\n*********************************************************************\n")
                                        time.sleep(3)

                                        # Running configure on postgis
                                        print("Running configure ...")
                                        result = os.system("cd "+paths.currentProject+"/"+ version["fullVersion"] +"/src/postgis-"+postgisVersion +" && ./configure --prefix="+ paths.shareLib +" --with-pgconfig="+paths.currentProject+"/"+ version["fullVersion"] +"/build/"+version["majorVersion"]+"/bin/pg_config --with-gdalconfig="+ paths.shareLib +"/bin/gdal-config  --with-geosconfig="+ paths.shareLib +"/bin/geos-config --with-projdir="+ paths.shareLib +" > "+paths.currentProject+"/"+version["fullVersion"] +"/logs/PostgisConfigure.log 2>&1")

                                        if result == 0:
                                            
                                            # Running build
                                            print("Running make ...")
                                            result = os.system("cd "+paths.currentProject+"/"+version["fullVersion"]+"/src/postgis-"+postgisVersion+" && make > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/PostgisBuild.log 2>&1")

                                            if result == 0:
                    
                                                # Starting postgresql server
                                                result = os.system("cd "+paths.currentProject + "/"+ version["fullVersion"] + "/build/" +version["majorVersion"]+ "/bin && ./initdb -D data > "+ paths.currentProject + "/" + version["fullVersion"] + "/logs/PostgresqlInit.log 2>&1")
                                                if result == 0:
                                           	         
                                                    result = os.system("cd "+paths.currentProject + "/"+ version["fullVersion"] + "/build/" +version["majorVersion"]+ "/bin && ./pg_ctl -D data start > "+ paths.currentProject + "/" + version["fullVersion"] + "/logs/PostgresStart.log 2>&1")
                                                    if result == 0:
                                                        # Running regression
                                                        print("Running regression ...")
                                                        result = os.system("cd " + paths.currentProject + "/" + version["fullVersion"] + "/src/postgis-" + postgisVersion + " && make check > " + paths.currentProject + "/" + version["fullVersion"] + "/logs/PostgisRegression.log 2>&1")
                                                
                                                        os.system("cd "+paths.currentProject + "/"+ version["fullVersion"] + "/build/" +version["majorVersion"]+ "/bin && rm -rf data ")

                                                        if result == 0:
                                                            # Running install
                                                            print("Running make install ...")
                                                            result = os.system("cd "+paths.currentProject+"/"+version["fullVersion"]+"/src/postgis-"+postgisVersion+" && make install > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/PostgisInstallation.log 2>&1")

                                                            if result == 0:
                                                                print("\n*********************************************************************\n")
                                                                print("\n                      Finalizing the automation                      \n")
                                                                print("\n*********************************************************************\n")
                                                                time.sleep(3)

                                                                # Copying required libraries to build
                                                                print("Copying required libraries to build ...")
                                                                src= paths.shareLib + "/lib/"
                                                                dest = ""+paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/lib/"
                                                                copyFile.copy(src, dest)
 
                                                                print("Copying share into share ...")
                                                                src= paths.shareLib + "/share/"
                                                                dest = ""+paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/share/"
                                                                copyFile.copy(src, dest)                

                                                                # Copying openssl
                                                                src = "/Users/2ndquadrant/2UDA/openssl-1.0.2g/inst/lib"
                                                                dest = paths.root+ "/workDir/" + currentDateTime + "/" + version['fullVersion'] + "/build/" + version['majorVersion'] + "/lib"
                                                                copyFile.copy(src, dest)
                                                                time.sleep(2) 

                                                                # Setting RunTime path
                                                                # Bin
                                                                binPath = paths.currentProject + "/" + version["fullVersion"] + "/build/" + version["majorVersion"] + "/bin"
                                                                print("Setting RPATH for bin ...")
                                                                for file in os.listdir(binPath):
                   
                                                                    os.system('cd ' + binPath + ' && install_name_tool -delete_rpath '+buildLocation+' -add_rpath @executable_path/../lib "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/binRpath.log 2>&1")
                                                                    os.system('cd ' + binPath + ' && install_name_tool -change "'+buildLocation+'/lib/libpq.5.dylib" "@executable_path/../lib/libpq.5.dylib" "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/binChange.log 2>&1")
                                                                    os.system('cd ' + binPath + ' && install_name_tool -change "'+os.environ['OPENSSL_HOME']+'/lib/libssl.1.0.0.dylib" "@executable_path/../lib/libssl.1.0.0.dylib" "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/binChange.log 2>&1")
                                                                    os.system('cd ' + binPath + ' && install_name_tool -change "'+os.environ['OPENSSL_HOME']+'/lib/libcrypto.1.0.0.dylib" "@executable_path/../lib/libcrypto.1.0.0.dylib" "./' + file + '" >> ' + paths.currentProject + "/"+ version["fullVersion"] + "/logs/binChange.log 2>&1")
                                                                    os.system('cd ' + binPath + ' && install_name_tool -change "'+paths.shareLib+'/lib/libgeos_c.1.dylib" "@executable_path/../lib/libgeos_c.1.dylib" "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/binChange.log 2>&1")
                                                                    os.system('cd ' + binPath + ' && install_name_tool -change "'+paths.shareLib+'/lib/libproj.13.dylib" "@executable_path/../lib/libproj.13.dylib" "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/binChange.log 2>&1")
                                                                    os.system('cd ' + binPath + ' && install_name_tool -change "'+paths.shareLib+'/lib/libgeos-3.6.2.dylib" "@executable_path/../lib/libgeos-3.6.2.dylib" "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/binChange.log 2>&1")
                                                                    os.system('cd ' + binPath + ' && install_name_tool -change "'+paths.shareLib+'/lib/libgdal.20.dylib" "@executable_path/../lib/libgdal.20.dylib" "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/binChange.log 2>&1")

                                 

                                                                # Lib
                                                                libPath = paths.currentProject + "/" + version["fullVersion"] + "/build/" + version["majorVersion"] + "/lib"
                                                                print("Setting RPATH for lib ...")
                                                                for file in os.listdir(libPath):
                                                                    os.system('cd ' + libPath + ' && install_name_tool -delete_rpath '+buildLocation+' -add_rpath @executable_path/../lib "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/libRpath.log 2>&1")
                                                                    os.system('cd ' + libPath + ' && install_name_tool -change "'+buildLocation+'/lib/libpq.5.dylib" "@executable_path/../lib/libpq.5.dylib" "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/libChange.log 2>&1")
                                                                    os.system('cd ' + libPath + ' && install_name_tool -change "'+os.environ['OPENSSL_HOME']+'/lib/libssl.1.0.0.dylib" "@executable_path/../lib/libssl.1.0.0.dylib" "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/libChange.log 2>&1")
                                                                    os.system('cd ' + libPath + ' && install_name_tool -change "'+os.environ['OPENSSL_HOME']+'/lib/libcrypto.1.0.0.dylib" "@executable_path/../lib/libcrypto.1.0.0.dylib" "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/libChange.log 2>&1")
                                                                    os.system('cd ' + libPath + ' && install_name_tool -change "'+paths.shareLib+'/lib/libgeos_c.1.dylib" "@executable_path/../lib/libgeos_c.1.dylib" "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/binChange.log 2>&1")
                                                                    os.system('cd ' + libPath + ' && install_name_tool -change "'+paths.shareLib+'/lib/libproj.13.dylib" "@executable_path/../lib/libproj.13.dylib" "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/binChange.log 2>&1")
                                                                    os.system('cd ' + libPath + ' && install_name_tool -change "'+paths.shareLib+'/lib/libgeos-3.6.2.dylib" "@executable_path/../lib/libgeos-3.6.2.dylib" "./' + file + '" >> ' + paths.currentProject + "/" +version["fullVersion"] + "/logs/binChange.log 2>&1")
                                                                    os.system('cd ' + libPath + ' && install_name_tool -change "'+paths.shareLib+'/lib/libgdal.20.dylib" "@executable_path/../lib/libgdal.20.dylib" "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/binChange.log 2>&1")



                                                                # Lib/postgresql
                                                                postgresql = paths.currentProject + "/" + version["fullVersion"] + "/build/" + version["majorVersion"] + "/lib/postgresql"
                                                                print("Setting RPATH for lib/postgresql ...")
                                                                for file in os.listdir(postgresql):
                                                                    os.system('cd ' + postgresql + ' && install_name_tool -delete_rpath '+buildLocation+' -add_rpath @executable_path/../../lib "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/postgresqlRpath.log 2>&1")
                                                                    os.system('cd ' + postgresql + ' && install_name_tool -change "'+buildLocation+'/lib/libpq.5.dylib" "@executable_path/../../lib/libpq.5.dylib" "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/postgresqlChange.log 2>&1")
                                                                    os.system('cd ' + postgresql + ' && install_name_tool -change "'+os.environ['OPENSSL_HOME']+'/lib/libssl.1.0.0.dylib" "@executable_path/../../lib/libssl.1.0.0.dylib" "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/postgresqlChange.log 2>&1")
                                                                    os.system('cd ' + postgresql + ' && install_name_tool -change "'+os.environ['OPENSSL_HOME']+'/lib/libcrypto.1.0.0.dylib" "@executable_path/../../lib/libcrypto.1.0.0.dylib" "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/postgresqlChange.log 2>&1")
                                                                    os.system('cd ' + postgresql + ' && install_name_tool -change "'+paths.shareLib+'/lib/libgeos_c.1.dylib" "@executable_path/../lib/libgeos_c.1.dylib" "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/binChange.log 2>&1")
                                                                    os.system('cd ' + postgresql + ' && install_name_tool -change "'+paths.shareLib+'/lib/libproj.13.dylib" "@executable_path/../lib/libproj.13.dylib" "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/binChange.log 2>&1")
                                                                    os.system('cd ' + postgresql + ' && install_name_tool -change "'+paths.shareLib+'/lib/libgeos-3.6.2.dylib" "@executable_path/../lib/libgeos-3.6.2.dylib" "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/binChange.log 2>&1")
                                                                    os.system('cd ' + postgresql + ' && install_name_tool -change "'+paths.shareLib+'/lib/libgdal.20.dylib" "@executable_path/../lib/libgdal.20.dylib" "./' + file + '" >> ' + paths.currentProject + "/" + version["fullVersion"] + "/logs/binChange.log 2>&1")       


                                                                # Removing extra files
                                                                os.system("rm -rf postgresql-" + version["fullVersion"] + ".tar.gz postgis-" + postgisVersion + ".tar.gz")


                                                                # Generating zip file
                                                                print("Generating zip file ...")
                                                                os.system("cd " + paths.currentProject + "/" + version["fullVersion"] + " && tar -zcvf postgresql-osx.tar.gz build > " + paths.currentProject + "/" + version["fullVersion"] + "/logs/zip.log 2>&1")


                                                                print("\n*********************************************************************\n")
                                                                print("\n                           Process completed                         \n")
                                                                print("\n*********************************************************************\n")
                                                                # Final message
                                                                print("All binaries are placed at : "+ dirBuild)
                                                            
 
                                                                # Generating an email
                                                                print("Generating an email ...")
                                                                content = "Build completed successfully against "+ version["fullVersion"]
                                                                mail = smtplib.SMTP('smtp.gmail.com', 587)
                                                                mail.ehlo()
                                                                mail.starttls()
                                                                mail.login('semab.tariq@2ndquadrant.com', 'FDSA016016semab')
                                                                mail.sendmail('semab.tariq@2ndquadrant.com', 'semab.tariq@2ndquadrant.com', content )
                                                                mail.close()
                                                                print("Email sended to semab.tariq@2ndquadrant.com ..." )
                                                               
                                                            else:
                                                                print("Something went wrong with postgis installation ...")
                                                        else:
                                                            print("Something went wrong with postgis regression ...")
                                                    else:
                                                        print("Something went wrong with starting postgresql server ...")
                                                else:
                                                     print("Something went wrong with initializing postgresql server ...")
                                            else:
                                                print("Something went wrong with postgis build ...")
                                        else:
                                            print("Something went wrong with postgis configure ...")
                                    else:
                                        print("Something went wrong with postgresql installation ...")
                                else:
                                    print("Something went wrong with postgresql build ...")
                            else:
                                print("Something went wrong with postgresql configure ...")
                        else:
                            print("Something went wrong with Postgis unzipping ...")
                    else:
                        print("Something went wrong with Postgis downloading ...")
            else:
                print("Something went wrong with unzipping the postgresql")
        else:
            print("Something went wrong with downloading step please refer download.log file for more details")
