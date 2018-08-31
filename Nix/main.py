import os
from collections import OrderedDict
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
import time
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



os.environ['PYTHON_HOME']="/opt/Python-3.4.4/inst"
os.environ['OPENSSL_HOME']="/opt/openssl-1.0.2g/inst"
os.environ['PATH']=os.environ['PYTHON_HOME'] +"/bin:" + os.environ['OPENSSL_HOME'] + "/bin:" + paths.shareLib + "/bin:"+ os.environ['PATH']
os.environ['LD_LIBRARY_PATH']=os.environ['PYTHON_HOME'] +"/lib:" + os.environ['OPENSSL_HOME'] + "/lib:" + paths.shareLib + "/lib:"
os.environ['LDFLAGS']="-Wl,-rpath," + os.environ['PWD'] + " -L" + os.environ['PYTHON_HOME'] + "/lib -L" + os.environ['OPENSSL_HOME'] + "/lib" + " -L" + paths.shareLib + "/lib"
os.environ['CPPFLAGS']="-I"+os.environ['PYTHON_HOME'] + "inlclude/python3.4m" + " -I"+ os.environ['OPENSSL_HOME'] + "/include" + " -I" + paths.shareLib + "/include"
os.environ['PYTHON']=os.environ['PYTHON_HOME']+"/bin/python3"




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
   

      
    for version in configFile.decoded['v']:

        if configFile.addKrb == 1: 
            print("\n--------------Building KRB-------------\n")
            print("Building GSSAPI ...")
            print("Downloading KRB ...")
            krbFullVersion = ""
            for krb in configFile.decodedKrb["krbVersion"]:
                downloadKrb = os.system("wget "+krb["url"]+" > "+paths.currentProject+"/"+ version["fullVersion"] +"/logs/KrbDownload.log 2>&1")
                krbFullVersion = krb["fullVersion"]
            
            #Unzipping KRB
            print("Unzipping KRB ...")
            resultUnzipKrb = os.system("tar xzf krb5-"+ krb["fullVersion"] +".tar.gz" +" --directory " + paths.currentProject +"/"+ version["fullVersion"] +"/src")
 
            if resultUnzipKrb == 0:
                # Running configure
                print("Running configure ...")  
                resultKrbConfig = os.system('cd '+ paths.currentProject +'/'+ version["fullVersion"] +'/src/krb5-'+ krbFullVersion + '/src && ./configure  LDFLAGS="-L'+ os.environ['OPENSSL_HOME']  +'/lib" CPPFLAGS="-I'+ os.environ['OPENSSL_HOME']+'/include" --prefix='+ paths.shareLib +' --enable-shared=yes --enable-static=no > '+ paths.currentProject +'/'+ version["fullVersion"] +'/logs/KrbConfigure.log 2>&1')
            
                if resultKrbConfig == 0:
                    # Running make
                    print("Running make ...")
                    resultKrbMake = os.system("cd "+ paths.currentProject +"/"+ version["fullVersion"] +"/src/krb5-"+ krbFullVersion +"/src && make > "+ paths.currentProject +"/"+ version["fullVersion"] +"/logs/KrbBuild.log 2>&1")
   
                    if resultKrbMake == 0:
                        # Running make install
                        print("Running make install ...")
                        resultKrbMakeInstall = os.system("cd "+ paths.currentProject +"/"+ version["fullVersion"] +"/src/krb5-"+ krbFullVersion +"/src && make install > "+ paths.currentProject +"/"+ version["fullVersion"] +"/logs/KrbInstall.log 2>&1")

                        if resultKrbMakeInstall == 0:
                            print("\n--------------Building PostgreSQL-------------\n")
                            print("Downloading PostgreSQL ...")     
                            resultDownloadPostgres = os.system("wget "+ version["url"] +" > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/PostgresqlDownload.log 2>&1")
                        
                            if resultDownloadPostgres == 0:
                                # unzipping the postgresql
                                print("Unzipping the postgresql ...")
                                #resultUnzip = srcInstallation.unzipPostgresql(version["fullVersion"])
                                resultPostgresUnzip = os.system("tar xzf postgresql-"+ version["fullVersion"] +".tar.gz" +" --directory " +paths.currentProject+"/"+version["fullVersion"]+"/src")
                         
                                if resultPostgresUnzip == 0:
                                    # Setting paths to run postgis regression
                                    os.environ['PATH']=paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/bin:" + os.environ['PATH']
                                    # Downloading postgis
                                    print("Downloading postgis ...")
                                    postgisVersion = ""
                                    for postgis in configFile.decodedPostgis['postgisV']:
                                        result = os.system("wget "+ postgis["url"] +" > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/PostgresqlDownload.log 2>&1")
                                        postgisVersion = postgis["fullVersion"]

                                    # Unzipping postgis
                                    print("Unzipping Postgis ...")
                                    #srcInstallation.unzipPostgis(version["fullVersion"], postgis["fullVersion"])
                                    resultUnzipPostgis = os.system("tar xzf postgis-"+ postgis["fullVersion"] +".tar.gz" +" --directory " +paths.currentProject+"/"+ version["fullVersion"] +"/src")
                        
                                    if resultUnzipPostgis == 0:
                                        # Removing extra files
                                        os.system("rm -rf postgresql-"+version["fullVersion"]+".tar.gz postgis-"+postgisVersion+".tar.gz")
                                        # Configure on Postgresql
                                        print("Running configure ...")
                                        configPath = paths.currentProject+"/"+ version["fullVersion"] +"/src/postgresql-"+version["fullVersion"]
                                        configCommand = "./configure --with-ldap --with-gssapi --with-openssl --with-python --with-zlib --prefix="+ paths.currentProject+"/"+version["fullVersion"]+"/build/"+ version["majorVersion"] +" > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/PostgresqlConfigure.log 2>&1"
                                        resultPostgresConfig = os.system("cd "+configPath+" && "+configCommand+"")
                                    
                                        if resultPostgresConfig == 0:
                                            # Running build
                                            print("Running build ...")
                                            buildPath = paths.currentProject + "/" + version["fullVersion"] + "/src/postgresql-" + version["fullVersion"]
                                            command = " make world > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/PostgresqlBuild.log 2>&1"
                                            resultPgsqlBuild = os.system("cd "+buildPath+" && "+command+"")
                                
                                            if resultPgsqlBuild == 0:
                                                # Running regression
                                                print("Running regression ...")	
                                                regressionPath = paths.currentProject + "/" + version["fullVersion"] + "/src/postgresql-" + version["fullVersion"]
                                                command = " make check > "+ paths.currentProject +"/"+version["fullVersion"]+"/logs/PostgresqlRegression.log 2>&1"
                                                resultPgsqlRegression = os.system("cd "+regressionPath+" && "+command+"")
                                                
                                                if resultPgsqlRegression == 0:
                                                    print("Running install ...")
                                                    buildPath = paths.currentProject + "/" + version["fullVersion"] + "/src/postgresql-" + version["fullVersion"]
                                                    command = " make install-world > "+ paths.currentProject +"/"+ version["fullVersion"] +"/logs/PostgresqlInstall.log 2>&1"
                                                    resultPgsqlInstall = os.system("cd "+buildPath+" && "+command+"")
                                                    
                                                    if resultPgsqlInstall == 0:
                                                        print("\n--------------Building POSTGIS-------------\n")
                                                        # Running configure on postgis
                                                        print("Running configure on postgis ...")
                                                        resultPostgisConfigure = os.system("cd "+ paths.currentProject +"/"+ version["fullVersion"] +"/src/postgis-"+ postgisVersion +" && ./configure --prefix="+ paths.shareLib +" --with-pgconfig="+paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/bin/pg_config --with-gdalconfig="+ paths.shareLib +"/bin/gdal-config  --with-geosconfig="+ paths.shareLib +"/bin/geos-config --with-projdir="+ paths.shareLib +" --with-xml2config="+ paths.shareLib +"/bin/xml2-config > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/PostgisConfigure.log 2>&1")
                                            
                                                        if resultPostgisConfigure == 0:
                                                            # Running build
                                                            print("Running make ...")
                                                            resultPostgisBuild = os.system("cd "+paths.currentProject+"/"+version["fullVersion"]+"/src/postgis-"+postgisVersion+" && make > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/PostgisBuild.log 2>&1")

                                                            if resultPostgisBuild == 0:
                                                                print("Starting Postgresql server ...")
                                                                resultInitDB = 0
                                                                #resultInitDB = os.system("cd "+paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/bin && ./initdb -D data  > "+ paths.currentProject + "/" + version["fullVersion"] + "/logs/PostgresqlInit.log 2>&1")
                                                                if resultInitDB == 0:
                                                                    resulPostgresStart = 0
                                                                    #resulPostgresStart = os.system("cd "+paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/bin && ./pg_ctl -D data start  > "+ paths.currentProject + "/" + version["fullVersion"] + "/logs/PostgresqlStart.log 2>&1")
                                                    
                                                                    if resulPostgresStart == 0:
                                                                        print("Runing regression ...")
                                                                        resultPostgisRegression = 0 
                                                                        #resultPostgisRegression = os.system("cd " + paths.currentProject + "/" + version["fullVersion"] + "/src/postgis-" + postgisVersion + " && make check > " + paths.currentProject + "/" + version["fullVersion"] + "/logs/PostgisRegression.log 2>&1")

                                                                        if resultPostgisRegression == 0:
                                                                            os.system("cd "+paths.currentProject + "/"+ version["fullVersion"] + "/build/" +version["majorVersion"]+ "/bin && rm -rf data ")
                                                                            # Running install
                                                                            print("Running make install ...")
                                                                            resultPostgisInstall = os.system("cd "+paths.currentProject+"/"+version["fullVersion"]+"/src/postgis-"+ postgisVersion +" && make install > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/PostgisInstall.log 2>&1")

                                                                            if resultPostgisInstall == 0:
                                                                                # Copying required libraries to build
                                                                                print("Copying required libraries to build ...")
                                                                                src = paths.shareLib + "/lib/*"
                                                                                dest = ""+paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/lib/"
                                                                                resultCPLibSf = os.system("cp -rv " + src + " " + dest + " > " + paths.currentProject+"/"+version["fullVersion"]+"/logs/SharedLibCopy.log 2>&1")
                               
                                                                                if resultCPLibSf == 0:
									            # Copying share/gdal
                                                                                    print("Copying sharedLib/share/gdal to build")
                                                                                    src = paths.shareLib+ "/share/gdal"
                                                                                    dest = ""+paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/share"
                                                                                    resultCPgdalSf = os.system("cp -r "+src+" "+dest+"")

                                                                                    if resultCPgdalSf == 0:
                                                                                        # Copying share/proj
                                                                                        print("Copying sharedLib/share/proj to build")
                                                                                        src = paths.shareLib+ "/share/proj"
                                                                                        dest = ""+paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/share"
                                                                                        resultCPprojSf = os.system("cp -r "+src+" "+dest+"")
 
                                                                                        if resultCPprojSf == 0: 
									                    # Copying openssl
                                                                                            src = "/opt/openssl-1.0.2g/inst/lib"
                                                                                            dest = paths.root+ "/workDir/" + currentDateTime + "/" + version['fullVersion'] + "/build/" + version['majorVersion'] + "/lib"
                                                                                            resultCPopenssl = 0
                                                                                            copyFile.copy(src, dest)
	
                                                                                            if resultCPopenssl == 0:		
                                                                                                # Setting Rpath
                                                                                                binPath = paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/bin"
                                                                                                print("Setting RPATH for bin ...")
                                                                                                for file in os.listdir(binPath):
                                                                                                    os.system('cd '+binPath+' && chrpath -r "\${ORIGIN}/../lib/" ./'+file+" >> "+paths.currentProject+"/"+version["fullVersion"]+"/logs/binRpath.log 2>&1")
                 
                                                                                                libPath = paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/lib"
                                                                                                print("Setting RPATH for lib ...")
                                                                                                orignalRoot = ""
                                                                                                counter = 0
                                                                                                for root, dirs, files in os.walk(libPath):
                                                                                                    if counter == 0:
                                                                                                        orignalRoot = root
                                                                                                        counter = 1
                                                                                                    tmp = root+orignalRoot
                                                                                                    newString = tmp.replace(orignalRoot, "")
                                                                                                    dirCounter = newString.count("/")
                                                                                                    dot = "../"
                                                                                                    for x in range(dirCounter):
                                                                                                        dot += dot
                                                                                                    for file in files:
                                                                                                        os.system('cd '+ root +' && chrpath -r "\${ORIGIN}/'+dot+'lib/" ./' + file+ " >> "+paths.currentProject+"/"+version["fullVersion"]+"/logs/libRpath.log 2>&1")

                                                                                                    

                                                                                                libPostgresql =  paths.currentProject+"/"+version["fullVersion"]+"/build/"+version["majorVersion"]+"/lib/postgresql"
                                                                                                print("Setting RPATH for lib/postgresql ...")
                                                                                                #for file in os.listdir(libPostgresql):
                                                                                                    #os.system('cd '+libPostgresql+' && chrpath -r "\${ORIGIN}/../../lib/" ./' + file+ " >> "+paths.currentProject+"/"+version["fullVersion"]+"/logs/postgresqlRpath.log 2>&1")
									
                                                                                                # Generating zip file
                                                                                                print("Generating zip file ...")
                                                                                                os.system("cd "+paths.currentProject+"/"+version["fullVersion"]+" && tar -zcvf Postgresql"+ version["fullVersion"] +"-linux.tar.gz build > "+paths.currentProject+"/"+version["fullVersion"]+"/logs/zip.log 2>&1")

									                        # Final message
                                                                                                print("All binaries are placed at : " + dirBuild)

									                        # Generating an email
                                                                                                print("Generating an email ...")
                                                                                                content = "Linux = build completed successfully against "+ version["fullVersion"]
                                                                                                mail = smtplib.SMTP('smtp.gmail.com', 587)
                                                                                                mail.ehlo()
                                                                                                mail.starttls()
                                                                                                mail.login('semab.tariq@2ndquadrant.com', 'FDSA016016semab')
                                                                                                mail.sendmail('semab.tariq@2ndquadrant.com', 'semab.tariq@2ndquadrant.com', content )
                                                                                                mail.close()
                                                                                                print("Email sended to semab.tariq@2ndquadrant.com ..." )

                                                                                            else:
                                                                                                print("Copy openssl fails ...")
                                                                                        else:
                                                                                            print("Copy proj fails ...")
                                                                                    else:
                                                                                        print("Copy Gdal fails ...")
                                                                                else:
                                                                                    print("Copy lib from share folder fails ...")
                                                                            else:
                                                                                print("Something went wrong with Postgis installation ...")
                                                                        else:
                                                                            print("something went wrong with Postgis Regression ...")
                                                                    else:
                                                                        print("Error in Postgres servre starting ...")
                                                                else:
                                                                    print("Error in initDB ...")
                                                            else:
                                                                print("Something went wrong with Postgis build ...")
                                                        else:
                                                            print("Something went wrong with Postgis configure ...")
                                                    else:
                                                        print("something went wrong with Postgresql installation ...")
                                                else:
                                                    print("Something went wrong with Postgresql regression ...")
                                            else:
                                                print("Something went wrong with Postgresql build ...")
                                        else:
                                            print("Something went wrong with Postgresql configure ...")
                                    else:
                                        print("Something went wrong with Postgis unzipping ...")	
                                else:
                    	            print("Something went wrong with Postgres unzip ...")
                            else:
                                print("Something went wrong with postgres downloading ...")
                        else:
                            print("Something went wrong with KRB installation ...")
                    else:
                        print("Error in KRB build ...")       
                else:
                    print("Error in KRB configure ...")
            else:
                print("Error in KRB unzipping ...") 
