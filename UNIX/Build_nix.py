import time
import platform
import os
import Config_file

try:

    os.system("clear")


    print("\n\n----- Running pre build steps -----\n\n")


    time.sleep(3)

    # Initializing classes
    print("Initializing classes ...")
    config_file = Config_file.config_file()

    time.sleep(2)

    # Detecting operating system
    os_name = platform.system();
    print("Detected operating system is ... "+ os_name)

    # setting and Modifying variables according to detected OS
    download_keyword = "curl -O"
    if os_name == "Linux":
        download_keyword = "wget"

    time.sleep(2)

    # Getting values from system
    print("Getting required values from system ...")
    current_date_time = time.strftime("%Y%m%d%H%M%S")
    root = os.path.dirname(os.path.abspath(__file__))

    time.sleep(2)

    print("Setting up folder structure ...")
    time.sleep(2)
    for postgreSQL_version in config_file.postgreSQL_info_decoded['postgreSQL_version']:
        dir_src = root +"/work_dir/"+ current_date_time + "/"+ postgreSQL_version['full_version'] +"/src"
        if not os.path.exists(dir_src):
            os.makedirs(dir_src)
            print(dir_src)
        dir_logs = root +"/work_dir/"+ current_date_time + "/"+ postgreSQL_version['full_version'] +"/logs"    
        if not os.path.exists(dir_logs):
            os.makedirs(dir_logs)
            print(dir_logs)
        dir_build = root +"/work_dir/"+ current_date_time + "/"+ postgreSQL_version['full_version'] +"/build/"+ postgreSQL_version['major_version']
        if not os.path.exists(dir_build):
            os.makedirs(dir_build)
            print(dir_build)

        time.sleep(2)
 
        # Initializing variables
        print("Inintializing variables ...")
        current_project = root +"/work_dir/"+ current_date_time
        cd_path = ""
        postgreSQL_build_location = current_project + "/" + postgreSQL_version["full_version"] +"/build/"+ postgreSQL_version["major_version"]
        postgreSQL_bin_path = current_project + "/" + postgreSQL_version["full_version"] +"/build/"+ postgreSQL_version["major_version"] +"/bin"
        postgreSQL_lib_path = current_project + "/" + postgreSQL_version["full_version"] +"/build/"+ postgreSQL_version["major_version"] +"/lib"    
        postgreSQL_share_path = current_project + "/" + postgreSQL_version["full_version"] +"/build/"+ postgreSQL_version["major_version"] +"/share"    
 
        time.sleep(2)
      
        # Saving system paths variable value to reset it again 
        print("Saving current state of system path variable ...")
        system_PATH = os.environ['PATH']

        time.sleep(2)

        # Setting systems path variables
        print("Setting system path variables ...")
        os.environ['PYTHON_HOME'] = config_file.python_home
        os.environ['OPENSSL_HOME'] = config_file.openssl_home
        os.environ['PATH'] = postgreSQL_build_location +"/bin:"+ os.environ['PYTHON_HOME'] +"/bin:"+ os.environ['OPENSSL_HOME'] +"/bin:"+ config_file.share_lib +"/bin:"+ os.environ['PATH']
        os.environ['LD_LIBRARY_PATH'] = os.environ['PYTHON_HOME'] +"/lib:"+ os.environ['OPENSSL_HOME'] +"/lib:"+ config_file.share_lib +"/lib:"
        os.environ['LDFLAGS'] = "-Wl,-rpath,"+ postgreSQL_build_location +" -L"+ os.environ['PYTHON_HOME'] +"/lib -L"+ os.environ['OPENSSL_HOME'] +"/lib -L"+ config_file.share_lib +"/lib"
        os.environ['CPPFLAGS'] = "-I"+ os.environ['PYTHON_HOME'] +"inlclude/python3.4m -I"+ os.environ['OPENSSL_HOME'] +"/include -I"+ config_file.share_lib +"/include"
        os.environ['PYTHON'] = os.environ['PYTHON_HOME'] +"/bin/python3"

        time.sleep(2)

 
        print("\n\n----- Running build steps -----\n\n")
    
    
        time.sleep(3)

    
        # Downloading postgreSQL source code
        print("Downloading PostgreSQL "+ postgreSQL_version['full_version'] +" source code ...")
        result_postgreSQL_download = os.system(download_keyword +" "+ postgreSQL_version["url"] +" > "+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_download.log 2>&1")

        if result_postgreSQL_download == 0:
        
            # Unzipping postgreSQL
            print("Unzipping postgreSQL source code ...")
            result_postgreSQL_unzip = os.system("tar xzf postgresql-"+ postgreSQL_version["full_version"] +".tar.gz --directory "+ current_project +"/"+ postgreSQL_version["full_version"] +"/src")
        
            # Removing source file .tar.gz
            os.system("cd "+ root +" && rm -rf postgresql-"+ postgreSQL_version['full_version'] +".tar.gz")

            if result_postgreSQL_unzip == 0:
            
                # Running configure on PostgreSQL
                print("Checking for required configure options for postgreSQL ...")
                configure_with = ""
                if config_file.with_openssl == 1:
                    configure_with = configure_with +" --with-openssl "
                if config_file.with_gssapi == 1:
                    configure_with = configure_with +" --with-gssapi "
                if config_file.with_python == 1:
                    configure_with = configure_with +" --with-python "
                if config_file.with_ldap == 1:
                    configure_with = configure_with +" --with-ldap "
                if config_file.with_zlib == 1:
                    configure_with = configure_with +" --with-zlib "
                if config_file.with_icu == 1:
                    configure_with = configure_with +" --with-icu "
                time.sleep(2)
                print("Running configure on postgreSQL ...")
                cd_path = current_project +"/"+ postgreSQL_version["full_version"] +"/src/postgresql-"+ postgreSQL_version["full_version"]
                result_postgreSQL_configure = os.system("cd "+ cd_path +" && ./configure "+ configure_with +" ICU_CFLAGS='-I"+ config_file.share_lib +"/include' ICU_LIBS='-L"+ config_file.share_lib +"/lib -licui18n -licuuc -licudata' --prefix="+ current_project +"/"+ postgreSQL_version["full_version"] +"/build/"+ postgreSQL_version['major_version'] +" > "+ current_project +"/"+ postgreSQL_version['full_version'] +"/logs/postgreSQL_configure.log 2>&1") 
            
                if result_postgreSQL_configure == 0:
                
                    # Running build on postgreSQL
                    print("Running make on postgreSQL ...")
                    cd_path = current_project +"/"+ postgreSQL_version["full_version"] +"/src/postgresql-"+ postgreSQL_version["full_version"]
                    result_postgreSQL_build = os.system("cd "+ cd_path +" && make world > "+ current_project +"/"+ postgreSQL_version['full_version'] +"/logs/postgreSQL_build.log 2>&1")
        
                    if result_postgreSQL_build == 0:
      
                        # Running postgreSQL regression
                        print("Running make check on PostgreSQL ...")
                        cd_path = current_project +"/"+ postgreSQL_version["full_version"] +"/src/postgresql-"+ postgreSQL_version["full_version"]
                        result_postgreSQL_regression = os.system("cd "+ cd_path +" && make check > "+ current_project +"/"+ postgreSQL_version['full_version'] +"/logs/postgreSQL_regression.log 2>&1")

                        if result_postgreSQL_regression == 0:
                         
                            # Running postgreSQL install
                            print("Running make install on PostgreSQL ...")
                            cd_path = current_project +"/"+ postgreSQL_version["full_version"] +"/src/postgresql-"+ postgreSQL_version["full_version"]
                            result_postgreSQL_install = os.system("cd "+ cd_path +" && make install-world > "+ current_project +"/"+ postgreSQL_version['full_version'] +"/logs/postgreSQL_install.log 2>&1")

                            if result_postgreSQL_install == 0:
                         
                                time.sleep(2)

                                print("\nChecking for addtional required features -----\n")


                                time.sleep(3)

                                if config_file.postgis_required == 1:
 
                                    # Downloading postgis
                                    print("Downloading postgis ... "+ config_file.postgis_full_version)
                                    result_postgis_download = os.system(download_keyword +" "+ config_file.postgis_download_url +" > "+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgis_download.log 2>&1")
                                    
                                    if result_postgis_download == 0:
                                        
                                        # Unzipping postgis
                                        print("Unzipping postgis ...")
                                        result_postgis_unzip = os.system("tar xzf postgis-"+ config_file.postgis_full_version +".tar.gz --directory "+ current_project +"/"+ postgreSQL_version["full_version"] +"/src")

                                        # Deleting postgis.tar file
                                        os.system("cd "+ root +" && rm -rf postgis-"+ config_file.postgis_full_version +".tar.gz")

                                        if result_postgis_unzip == 0:
  
                                            # Running configure on postgis
                                            print("Running configure on postgis ...")
                                            cd_path = current_project +"/"+ postgreSQL_version["full_version"] +"/src/postgis-"+ config_file.postgis_full_version
                                            result_postgis_Configure = os.system("cd "+ cd_path +" && ./configure --prefix="+ config_file.share_lib +" --with-pgconfig="+ postgreSQL_bin_path +"/pg_config --with-gdalconfig=" + config_file.share_lib + "/bin/gdal-config  --with-geosconfig="+ config_file.share_lib +"/bin/geos-config --with-projdir="+ config_file.share_lib +" --with-xml2config="+ config_file.share_lib +"/bin/xml2-config > "+ current_project +"/"+ 
postgreSQL_version["full_version"] +"/logs/postgis_configure.log 2>&1")
                                      
                                            if result_postgis_Configure == 0:
                                                
                                                cd_path = current_project +"/"+ postgreSQL_version["full_version"] +"/src/postgis-"+ config_file.postgis_full_version
                                                result_postgis_build = os.system("cd "+ cd_path +" && make > "+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgis_build.log 2>&1")

                                                if result_postgis_build == 0:
 
                                                    # Running regression tests on postgis
                                                    print("Running make check on postgis ...")
                                                    result_init_db = os.system("cd "+ postgreSQL_bin_path +" && ./initdb -D data > "+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgresql_init.log 2>&1")
 
                                                    if result_init_db == 0:
                                                        
                                                        # Starting the postgreSQL service
                                                        result_postgreSQL_start = os.system("cd "+ postgreSQL_bin_path +" && ./pg_ctl -D data start > "+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_start.log 2>&1")

                                                        if result_postgreSQL_start == 0:
                                                        
                                                            # Running make check on postgis
                                                            cd_path = current_project +"/"+ postgreSQL_version["full_version"] +"/src/postgis-"+ config_file.postgis_full_version
                                                            result_postgis_regression = os.system("cd "+ cd_path +" && make check > "+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgis_regression.log 2>&1")
                                                            
                                                            if result_postgis_regression == 0:
                                                                
                                                                # Stopping postgreSQL service
                                                                result_postgreSQL_stop = os.system("cd "+ postgreSQL_bin_path +" && ./pg_ctl -D data stop > "+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_stop.log 2>&1")

                                                                if result_postgreSQL_stop != 0:
                              
                                                                    print("Could not able to stop postgreSQL service see postgreSQL_stop.log for more details ...")
                                                                    exit()
 
                                                                os.system("cd "+ postgreSQL_bin_path +" && rm -rf data")
    
                                                                # Running make install on postgis
                                                                print("Running make install on postgis ...")
                                                                cd_path = current_project +"/"+ postgreSQL_version["full_version"] +"/src/postgis-"+ config_file.postgis_full_version
                                                                result_postgis_install = os.system("cd "+ cd_path +" && make install > "+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgis_install.log 2>&1")
	
                                                                if result_postgis_install == 0:
          
                                                                    
                                                                    # Running post build steps
                                                                    print("\n\n----- Running post build steps -----\n\n")
     

                                                                    # Copyig lib from share_lib to build
                                                                    print("Copying libraries from share_lib in build ...")
                                                                    source = config_file.share_lib +"/lib/*"
                                                                    result_copy = os.system("cp -rv "+ source +" "+ postgreSQL_lib_path +"/ > "+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/copy_share_lib.log 2>&1")
     
                                                                    if result_copy == 0:
                                                                   
                                                                        # Copying share/gdal from share_lib to build
                                                                        print("Copying share/gdal from share_lib into build ...")
                                                                        source = config_file.share_lib +"/share/gdal"
                                                                        result_copy = os.system("cp -rv "+ source +" "+ postgreSQL_share_path +" > "+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/copy_gdal_share_lib.log 2>&1")

                                                                        if result_copy == 0:
                                                                            
                                                                            # Copy share/proj from share_lib to build 
                                                                            print("Copying share/proj from share_lib into build ...")
                                                                            source = config_file.share_lib +"/share/proj"
                                                                            result_copy = os.system("cp -rv "+ source +" "+ postgreSQL_share_path +" > "+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/copy_proj_share_lib.log 2>&1")
 
                                                                            if result_copy == 0:
                                                                                
                                                                                # Copyin openssl into build
                                                                                print("Copying openssl libraries into build")
                                                                                source = config_file.openssl_home +"/lib/*"
                                                                                result_copy = os.system("cp -rv "+ source +" "+ postgreSQL_lib_path +"/ > "+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/copy_openssl_share_lib.log 2>&1")

                                                                                if result_copy == 0:
                                                    
                                                                                    if os_name == "Linux":
                                                                                        
                                                                                        # Setting runtime paths for linux
                                                                                        # PostgreSQL_bin
                                                                                        print("Setting runtime paths for for bin ...")
                                                                                        for file in os.listdir(postgreSQL_bin_path):
                                                                                            os.system('cd '+ postgreSQL_bin_path +' && chrpath -r "\${ORIGIN}/../lib/" ./'+ file +" >> "+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_bin_rpaths.log 2>&1")

                                                                                        # PostgreSQL_lib
                                                                                        print("Setting runtime paths for lib ...")
                                                                                        for file in os.listdir(postgreSQL_lib_path):
                                                                                            os.system('cd '+ postgreSQL_lib_path +' && chrpath -r "\${ORIGIN}/../lib/" ./'+ file +" >> "+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_lib_rpaths.log 2>&1")

                                                                                        # PostgreSQL_lib/postgresql
                                                                                        print("Setting RPATH for lib/postgresql ...")
                                                                                        source = postgreSQL_lib_path +"/postgresql"
                                                                                        for file in os.listdir(source):
                                                                                            os.system('cd '+ source +' && chrpath -r "\${ORIGIN}/../../lib/" ./'+ file + " >> "+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_postgress_rpaths.log 2>&1")

                                                                                    else:
                                                                                        # Setting run time parhs for MacOS 
                                                                                        # Bin
                                                                                        print("Setting runtime path for bin ...")
                                                                                        for file in os.listdir(postgreSQL_build_location +"/bin"):
                                                                                            os.system('cd '+ postgreSQL_build_location +'/bin && install_name_tool -delete_rpath '+ postgreSQL_build_location +' -add_rpath @executable_path/../lib "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_bin_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/bin && install_name_tool -change "'+ postgreSQL_build_location +'/lib/libpq.5.dylib" "@executable_path/../lib/libpq.5.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_bin_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/bin && install_name_tool -change "'+ os.environ['OPENSSL_HOME'] +'/lib/libssl.1.0.0.dylib" "@executable_path/../lib/libssl.1.0.0.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_bin_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/bin && install_name_tool -change "'+ os.environ['OPENSSL_HOME'] +'/lib/libcrypto.1.0.0.dylib" "@executable_path/../lib/libcrypto.1.0.0.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_bin_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/bin && install_name_tool -change "'+ config_file.share_lib +'/lib/libgeos_c.1.dylib" "@executable_path/../lib/libgeos_c.1.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_bin_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/bin && install_name_tool -change "'+ config_file.share_lib +'/lib/libproj.13.dylib" "@executable_path/../lib/libproj.13.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_bin_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/bin && install_name_tool -change "'+ config_file.share_lib +'/lib/libgeos-3.6.2.dylib" "@executable_path/../lib/libgeos-3.6.2.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_bin_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/bin && install_name_tool -change "'+ config_file.share_lib +'/lib/libgdal.20.dylib" "@executable_path/../lib/libgdal.20.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_bin_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/bin && install_name_tool -change "'+ config_file.share_lib +'/lib/libicui18n.62.dylib" "@executable_path/../lib/libicui18n.62.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_bin_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/bin && install_name_tool -change "'+ config_file.share_lib +'/lib/libicuuc.62.dylib" "@executable_path/../lib/libicuuc.62.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_bin_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/bin && install_name_tool -change "'+ config_file.share_lib +'/lib/libicudata.62.dylib" "@executable_path/../lib/libicudata.62.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_bin_rpath.log 2>&1")

                                                                                        # Lib
                                                                                        print("Setting runtime path for lib ...")
                                                                                        for file in os.listdir(postgreSQL_build_location +"/lib"):
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib && install_name_tool -delete_rpath '+ postgreSQL_build_location +' -add_rpath @executable_path/../lib "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_lib_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib && install_name_tool -change "'+ postgreSQL_build_location +'/lib/libpq.5.dylib" "@executable_path/../lib/libpq.5.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_lib_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib && install_name_tool -change "'+ os.environ['OPENSSL_HOME'] +'/lib/libssl.1.0.0.dylib" "@executable_path/../lib/libssl.1.0.0.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_lib_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib && install_name_tool -change "'+ os.environ['OPENSSL_HOME'] +'/lib/libcrypto.1.0.0.dylib" "@executable_path/../lib/libcrypto.1.0.0.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_lib_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib && install_name_tool -change "'+ config_file.share_lib +'/lib/libgeos_c.1.dylib" "@executable_path/../lib/libgeos_c.1.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_lib_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib && install_name_tool -change "'+ config_file.share_lib +'/lib/libproj.13.dylib" "@executable_path/../lib/libproj.13.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_lib_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib && install_name_tool -change "'+ config_file.share_lib +'/lib/libgeos-3.6.2.dylib" "@executable_path/../lib/libgeos-3.6.2.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_lib_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib && install_name_tool -change "'+ config_file.share_lib +'/lib/libgdal.20.dylib" "@executable_path/../lib/libgdal.20.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_lib_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib && install_name_tool -change "'+ config_file.share_lib +'/lib/libicui18n.62.dylib" "@executable_path/../lib/libicui18n.62.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_lib_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib && install_name_tool -change "'+ config_file.share_lib +'/lib/libicuuc.62.dylib" "@executable_path/../lib/libicuuc.62.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_lib_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib && install_name_tool -change "'+ config_file.share_lib +'/lib/libicudata.62.dylib" "@executable_path/../lib/libicudata.62.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_lib_rpath.log 2>&1")

                                                                                        # Lib/postgresql
                                                                                        print("Setting runtime path for lib/postgresql ...")  
                                                                                        for file in os.listdir(postgreSQL_build_location +"/lib/postgresql"):  
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib/postgresql && install_name_tool -delete_rpath '+ postgreSQL_build_location +' -add_rpath @executable_path/../../lib "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_postgresql_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib/postgresql && install_name_tool -change "'+ postgreSQL_build_location +'/lib/libpq.5.dylib" "@executable_path/../../lib/libpq.5.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_postgresql_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib/postgresql && install_name_tool -change "'+ os.environ['OPENSSL_HOME'] +'/lib/libssl.1.0.0.dylib" "@executable_path/../../lib/libssl.1.0.0.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_postgresql_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib/postgresql && install_name_tool -change "'+ os.environ['OPENSSL_HOME'] +'/lib/libcrypto.1.0.0.dylib" "@executable_path/../../lib/libcrypto.1.0.0.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_postgresql_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib/postgresql && install_name_tool -change "'+ config_file.share_lib +'/lib/libgeos_c.1.dylib" "@executable_path/../../lib/libgeos_c.1.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_postgresql_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib/postgresql && install_name_tool -change "'+ config_file.share_lib +'/lib/libproj.13.dylib" "@executable_path/../../lib/libproj.13.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_postgresql_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib/postgresql && install_name_tool -change "'+ config_file.share_lib +'/lib/libgeos-3.6.2.dylib" "@executable_path/../../lib/libgeos-3.6.2.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_postgresql_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib/postgresql && install_name_tool -change "'+ config_file.share_lib +'/lib/libgdal.20.dylib" "@executable_path/../../lib/libgdal.20.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_postgresql_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib/postgresql && install_name_tool -change "'+ config_file.share_lib +'/lib/libicui18n.62.dylib" "@executable_path/../../lib/libicui18n.62.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_postgresql_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib/postgresql && install_name_tool -change "'+ config_file.share_lib +'/lib/libicuuc.62.dylib" "@executable_path/../../lib/libicuuc.62.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_postgresql_rpath.log 2>&1")
                                                                                            os.system('cd '+ postgreSQL_build_location +'/lib/postgresql && install_name_tool -change "'+ config_file.share_lib +'/lib/libicudata.62.dylib" "@executable_path/../../lib/libicudata.62.dylib" "./'+ file +'" >> '+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_postgresql_rpath.log 2>&1")

                                                                                    # Generating zip file
                                                                                    print("Generating zip file ...")
                                                                                    os.system("cd "+ current_project +"/"+ postgreSQL_version["full_version"] +" && tar -zcvf Postgresql"+ postgreSQL_version["full_version"] +"-linux-"+ postgreSQL_version['full_version'] +".tar.gz build > "+ current_project +"/"+ postgreSQL_version["full_version"] +"/logs/postgreSQL_build_zip.log 2>&1")

                                                                                    # Final message
                                                                                    print("\n\nAll binaries are placed at : "+ dir_build)

                                                                                    print("Restoring system PATH ...")
                                                                                    os.environ['PATH'] = system_PATH
                                                                                    time.sleep(2)
 
                                                                                    print("\n\nBuild is completed successfully\n\n")
                                                                                else:
                                                                                    print("Copying openssl/lib to build fails see copy_openssl_share_lib.log for more details ...")
                                                                            else:
                                                                                print("Copying share/proj to build fails see copy_proj_share_lib.log for more details ...")
                                                                        else:
                                                                            print("Copying share/gdal to build fails see copy_gdal_share_lib.log for more details ...")    
                                                                    else:
                                                                        print("Copying lib from share library to build fails see copy_share_lib.log for more details ...") 
                                                                else:
                                                                    print("Postgis installation fails see postgis_install.log for more details ...")
                                                            else:
                                                                print("Postgis regression fails see postgis_regression.log for more details ...")
                                                        else:
                                                            print("Could not start postgreSQL service see postgreSQL_start.log for more details ...")
                                                    else:
                                                        print("PostgreSQL initdb fails see postgreSQL_init.log for more details ...")  
                                                else:
                                                    print("Postgis build fails see postgis_build.log for more details ...")
                                            else:
                                                print("Postgis configure fails see postgis_configure.log for more details ...")
                                        else:
                                            print("postgis unzipping fails ...") 
                                    else:
                                        print("Postgis downloading fails see postgis_download.log for more detals ...") 
                                else:
                                    print("No additional module is required ...")
                            else:
                                print("PostgreSQL installations fails see postgreSQL_install.log for more details ...")
                        else:
                            print("PostgreSQL regression fails see postgreSQL_regression.log for more details ...") 
                    else:
                        print("PostgreSQL build fails see postgreSQL_build.log for more details ...")
                else:
                    print("PostgreSQL configure fails see postgreSQL_configure.log for more details ...")
            else:
                print("PostgreSQL unzipping failed ...")
        else:
            print("PostgreSQL source code downloading is failed ...")

except Exception as e:
    print(e)





