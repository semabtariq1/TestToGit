import threading
import time
import platform
import os
import config
import smtplib
import email
from local_env import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

os.system("clear")


# File which store all the output messages
output_file = open("output.txt", "a")
output_file.write("\n\n----- Running pre build steps -----\n\n")
output_file.close()

# Getting values from system
output_file = open("output.txt", "a")
output_file.write("Getting required values from system ...\n")
output_file.close()
current_date_time = time.strftime("%Y%m%d%H%M%S")
root = os.path.dirname(os.path.abspath(__file__))

try:
    time.sleep(3)
except:
    print("User cancle the execution ...")
    os.system("cd "+ root +" && rm -rf output.txt")
    quit()

# Initializing classes
output_file = open("output.txt", "a")
output_file.write("Initializing classes ...\n")
output_file.close()

config_file = config.config_file()


# Detecting operating system
os_name = platform.system();
output_file = open("output.txt", "a")
output_file.write("Detected operating system is ... "+ os_name +"\n")
output_file.close()
# setting and Modifying variables according to detected OS
download_keyword = "curl -O"
if os_name == "Linux":
    download_keyword = "wget"
else:
    # Thread class
    class thread(threading.Thread):
        def run(self):
            os.system('ssh '+ linux_box +' "cd '+ build_code_linux +' && python3 build-nix.py"')
    thread_to_call_linux_machine = thread()
    thread_to_call_linux_machine.start()

try:
    time.sleep(2)
except:
    print("User cancle the execution ...")
    os.system("cd "+ root +" && rm -rf output.txt")
    quit()

# Global variables
build_result = "null"

# Custom functions
# Generate an attached email
def send__email_with_output_file():
    
    for email in config_file.email_info_decoded['email']:
        
          msg = MIMEMultipart()
          msg['From'] = email['from']
          msg['To'] = email['to']
          if build_result == 0:
              msg['Subject'] = "Build process completed successfully for "+ os_name
              body = "see following attached file for more details ..."
          else:
              msg['Subject'] = "Build process failed for " +os_name
              body = "See following attached output file for more error details ..."

          msg.attach(MIMEText(body, 'plain'))
          filename = "output.txt"
          attachment = open( root +"/output.txt", "rb")
          part = MIMEBase('application', 'octet-stream')
          part.set_payload((attachment).read())
          encoders.encode_base64(part)
          part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
          msg.attach(part)

          server = smtplib.SMTP('smtp.gmail.com', 587)
          server.starttls()
          server.login(email['from'], email['sender_password'])
          text = msg.as_string()
          server.sendmail(email['from'], email['to'], text)
          server.quit()


# Sending build to mac 
def send_build_to_mac(tar_file_path, log_file_path):
    if os_name == "Linux":
        os.system('scp '+ tar_file_path +' '+ mac_address +':'+ mac_build_path +' > '+ log_file_path +'/copy_binary_to_osx.log 2>&1')

def copy_build(tar_file_path, log_file_path):
    os.system('cp '+ tar_file_path +' '+ mac_build_path +' > '+ log_file_path +'/copy_osx_build.log 2>&1')

try:

    output_file = open("output.txt", "a")
    output_file.write("Setting up folder structure ...\n")
    output_file.close()
    time.sleep(2)
    for postgreSQL_version in config_file.postgreSQL_info_decoded['postgreSQL_version']:
        dir_src = root +"/work_dir/"+ current_date_time + "/"+ postgreSQL_version['full_version'] +"/src"
        if not os.path.exists(dir_src):
            os.makedirs(dir_src)
            output_file = open("output.txt", "a")
            output_file.write(dir_src +"\n")
            output_file.close()
        dir_logs = root +"/work_dir/"+ current_date_time + "/"+ postgreSQL_version['full_version'] +"/logs"    
        if not os.path.exists(dir_logs):
            os.makedirs(dir_logs)
            output_file = open("output.txt", "a")
            output_file.write(dir_logs +"\n")
            output_file.close()
        dir_build = root +"/work_dir/"+ current_date_time + "/"+ postgreSQL_version['full_version'] +"/build/"+ postgreSQL_version['major_version']
        if not os.path.exists(dir_build):
            os.makedirs(dir_build)
            output_file = open("output.txt", "a")
            output_file.write(dir_build +"\n")
            output_file.close()
        time.sleep(2)


        # Initializing variables
        output_file = open("output.txt", "a")
        output_file.write("Inintializing variables ...\n")
        output_file.close()
        current_project = root +"/work_dir/"+ current_date_time
        cd_path = ""
        tar_file_path = current_project + "/" + postgreSQL_version["full_version"] +"/build/Postgresql-"+ os_name +"-"+ postgreSQL_version['full_version'] +".tar.gz"       
        time.sleep(2)
      
        # Saving system paths variable value to reset it again 
        output_file = open("output.txt", "a")
        output_file.write("Saving current state of system path variable ...\n")
        output_file.close()
        system_PATH = os.environ['PATH']

        time.sleep(2)

        # Setting systems path variables
        output_file = open("output.txt", "a")
        output_file.write("Setting system path variables ...\n")
        output_file.close()
        os.environ['PYTHON_HOME'] = python_home
        os.environ['OPENSSL_HOME'] = openssl_home
        os.environ['PATH'] = dir_build +"/bin:"+ os.environ['PYTHON_HOME'] +"/bin:"+ os.environ['OPENSSL_HOME'] +"/bin:"+ share_lib +"/bin:"+ pl_languages +"/perl-5.26/bin:"+ os.environ['PATH']  
        os.environ['LD_LIBRARY_PATH'] = os.environ['PYTHON_HOME'] +"/lib:"+ os.environ['OPENSSL_HOME'] +"/lib:"+ share_lib +"/lib:"+ pl_languages +"/perl-5.26/lib"
        os.environ['LDFLAGS'] = "-Wl,-rpath,"+ dir_build +" -L"+ os.environ['PYTHON_HOME'] +"/lib -L"+ os.environ['OPENSSL_HOME'] +"/lib -L"+ share_lib +"/lib -L"+ pl_languages +"/perl-5.26/lib "
        os.environ['CPPFLAGS'] = "-I"+ os.environ['PYTHON_HOME'] +"inlclude/python3.4m -I"+ os.environ['OPENSSL_HOME'] +"/include -I"+ share_lib +"/include"
        os.environ['PYTHON'] = os.environ['PYTHON_HOME'] +"/bin/python3"

        time.sleep(2)

        # Custom function
        def post_build_steps():
		    
            time.sleep(2)
            output_file = open("output.txt", "a")
			
            # Running post build steps
            output_file.write("\n\n----- Running post build steps -----\n\n")   
            output_file.close()
            
                                                                    
            time.sleep(3)     
                                                                     
            # Copyig lib from share_lib to build
            output_file = open("output.txt", "a")
            output_file.write("Copying libraries from share_lib in build ...\n")
            output_file.close()
            source = share_lib +"/lib/*"
            result_copy = os.system("cp -rv "+ source +" "+ dir_build +"/lib/ > "+ dir_logs +"/copy_share_lib.log 2>&1")
            if result_copy == 0:
                                                                   
                # Copying share/gdal from share_lib to build
                output_file = open("output.txt", "a")
                output_file.write("Copying share/gdal from share_lib into build ...\n")
                output_file.close()
                source = share_lib +"/share/gdal"
                result_copy = os.system("cp -rv "+ source +" "+ dir_build +"/share/ > "+ dir_logs +"/copy_gdal_share_lib.log 2>&1")

                if result_copy == 0:
                                                                            
                    # Copy share/proj from share_lib to build 
                    output_file = open("output.txt", "a")
                    output_file.write("Copying share/proj from share_lib into build ...\n")
                    output_file.close()
                    source = share_lib +"/share/proj"
                    result_copy = os.system("cp -rv "+ source +" "+ dir_build +"/share/ > "+ dir_logs + "/copy_proj_share_lib.log 2>&1")
 
                    if result_copy == 0:
                                                                                
                        # Copyin openssl into build
                        output_file = open("output.txt", "a")
                        output_file.write("Copying openssl libraries into build ...\n")
                        output_file.close()
                        source = openssl_home +"/lib/*"
                        result_copy = os.system("cp -rv "+ source +" "+ dir_build +"/lib/ > "+ dir_logs +"/copy_openssl_share_lib.log 2>&1")

                        if result_copy == 0:
                                                    
                            if os_name == "Linux":
                                                                                        
                                # Setting runtime paths for linux
                                # PostgreSQL_bin
                                output_file = open("output.txt", "a")
                                output_file.write("Setting runtime paths for for bin ...\n")
                                output_file.close()
                                for file in os.listdir(dir_build +"/bin"):
                                    os.system('cd '+ dir_build +'/bin && chrpath -r "\${ORIGIN}/../lib/" ./'+ file +" >> "+ dir_logs +"/postgreSQL_bin_rpaths.log 2>&1")

                                # PostgreSQL_lib
                                output_file = open("output.txt", "a")
                                output_file.write("Setting runtime paths for lib ...\n")
                                output_file.close()
                                for file in os.listdir(dir_build +"/lib"):
                                    os.system('cd '+ dir_build +'/lib && chrpath -r "\${ORIGIN}/../lib/" ./'+ file +" >> "+ dir_logs +"/postgreSQL_lib_rpaths.log 2>&1")

                                # PostgreSQL_lib/postgresql
                                output_file = open("output.txt", "a")
                                output_file.write("Setting RPATH for lib/postgresql ...\n")
                                output_file.close()
                                for file in os.listdir(dir_build +"/lib/postgresql"):
                                    os.system('cd '+ dir_build +'/lib/postgresql && chrpath -r "\${ORIGIN}/../../lib/" ./'+ file + " >> "+ dir_logs +"/postgreSQL_postgress_rpaths.log 2>&1")


                            else:
                                # Setting run time parhs for MacOS 
                                # Bin
                                output_file = open("output.txt", "a")
                                output_file.write("Setting runtime path for bin ...\n")
                                output_file.close()
                                for file in os.listdir(dir_build +"/bin"):
                                    os.system('cd '+ dir_build +'/bin && install_name_tool -delete_rpath '+ dir_build +' -add_rpath @executable_path/../lib "./'+ file +'" >> '+ dir_logs +"/postgreSQL_bin_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/bin && install_name_tool -change "'+ dir_build +'/lib/libpq.5.dylib" "@executable_path/../lib/libpq.5.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_bin_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/bin && install_name_tool -change "'+ os.environ['OPENSSL_HOME'] +'/lib/libssl.1.0.0.dylib" "@executable_path/../lib/libssl.1.0.0.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_bin_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/bin && install_name_tool -change "'+ os.environ['OPENSSL_HOME'] +'/lib/libcrypto.1.0.0.dylib" "@executable_path/../lib/libcrypto.1.0.0.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_bin_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/bin && install_name_tool -change "'+ share_lib +'/lib/libgeos_c.1.dylib" "@executable_path/../lib/libgeos_c.1.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_bin_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/bin && install_name_tool -change "'+ share_lib +'/lib/libproj.13.dylib" "@executable_path/../lib/libproj.13.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_bin_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/bin && install_name_tool -change "'+ share_lib +'/lib/libgeos-3.6.2.dylib" "@executable_path/../lib/libgeos-3.6.2.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_bin_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/bin && install_name_tool -change "'+ share_lib +'/lib/libgdal.20.dylib" "@executable_path/../lib/libgdal.20.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_bin_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/bin && install_name_tool -change "'+ share_lib +'/lib/libicui18n.62.dylib" "@executable_path/../lib/libicui18n.62.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_bin_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/bin && install_name_tool -change "'+ share_lib +'/lib/libicuuc.62.dylib" "@executable_path/../lib/libicuuc.62.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_bin_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/bin && install_name_tool -change "'+ share_lib +'/lib/libicudata.62.dylib" "@executable_path/../lib/libicudata.62.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_bin_rpath.log 2>&1")

                                # Lib
                                output_file = open("output.txt", "a")
                                output_file.write("Setting runtime path for lib ...\n")
                                output_file.close()
                                for file in os.listdir(dir_build +"/lib"):
                                    os.system('cd '+ dir_build +'/lib && install_name_tool -delete_rpath '+ dir_build +' -add_rpath @executable_path/../lib "./'+ file +'" >> '+ dir_logs +"/postgreSQL_lib_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib && install_name_tool -change "'+ dir_build +'/lib/libpq.5.dylib" "@executable_path/../lib/libpq.5.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_lib_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib && install_name_tool -change "'+ os.environ['OPENSSL_HOME'] +'/lib/libssl.1.0.0.dylib" "@executable_path/../lib/libssl.1.0.0.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_lib_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib && install_name_tool -change "'+ os.environ['OPENSSL_HOME'] +'/lib/libcrypto.1.0.0.dylib" "@executable_path/../lib/libcrypto.1.0.0.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_lib_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib && install_name_tool -change "'+ share_lib +'/lib/libgeos_c.1.dylib" "@executable_path/../lib/libgeos_c.1.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_lib_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib && install_name_tool -change "'+ share_lib +'/lib/libproj.13.dylib" "@executable_path/../lib/libproj.13.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_lib_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib && install_name_tool -change "'+ share_lib +'/lib/libgeos-3.6.2.dylib" "@executable_path/../lib/libgeos-3.6.2.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_lib_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib && install_name_tool -change "'+ share_lib +'/lib/libgdal.20.dylib" "@executable_path/../lib/libgdal.20.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_lib_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib && install_name_tool -change "'+ share_lib +'/lib/libicui18n.62.dylib" "@executable_path/../lib/libicui18n.62.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_lib_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib && install_name_tool -change "'+ share_lib +'/lib/libicuuc.62.dylib" "@executable_path/../lib/libicuuc.62.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_lib_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib && install_name_tool -change "'+ share_lib +'/lib/libicudata.62.dylib" "@executable_path/../lib/libicudata.62.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_lib_rpath.log 2>&1")

                                # Lib/postgresql
                                output_file = open("output.txt", "a")
                                output_file.write("Setting runtime path for lib/postgresql ...\n")
                                output_file.close()
                                for file in os.listdir(dir_build +"/lib/postgresql"):  
                                    os.system('cd '+ dir_build +'/lib/postgresql && install_name_tool -delete_rpath '+ dir_build +' -add_rpath @executable_path/../../lib "./'+ file +'" >> '+ dir_logs +"/postgreSQL_postgresql_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib/postgresql && install_name_tool -change "'+ dir_build +'/lib/libpq.5.dylib" "@executable_path/../../lib/libpq.5.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_postgresql_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib/postgresql && install_name_tool -change "'+ os.environ['OPENSSL_HOME'] +'/lib/libssl.1.0.0.dylib" "@executable_path/../../lib/libssl.1.0.0.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_postgresql_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib/postgresql && install_name_tool -change "'+ os.environ['OPENSSL_HOME'] +'/lib/libcrypto.1.0.0.dylib" "@executable_path/../../lib/libcrypto.1.0.0.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_postgresql_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib/postgresql && install_name_tool -change "'+ share_lib +'/lib/libgeos_c.1.dylib" "@executable_path/../lib/libgeos_c.1.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_postgresql_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib/postgresql && install_name_tool -change "'+ share_lib +'/lib/libproj.13.dylib" "@executable_path/../lib/libproj.13.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_postgresql_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib/postgresql && install_name_tool -change "'+ share_lib +'/lib/libgeos-3.6.2.dylib" "@executable_path/../lib/libgeos-3.6.2.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_postgresql_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib/postgresql && install_name_tool -change "'+ share_lib +'/lib/libgdal.20.dylib" "@executable_path/../lib/libgdal.20.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_postgresql_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib/postgresql && install_name_tool -change "'+ share_lib +'/lib/libicui18n.62.dylib" "@executable_path/../lib/libicui18n.62.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_postgresql_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib/postgresql && install_name_tool -change "'+ share_lib +'/lib/libicuuc.62.dylib" "@executable_path/../lib/libicuuc.62.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_postgresql_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib/postgresql && install_name_tool -change "'+ share_lib +'/lib/libicudata.62.dylib" "@executable_path/../lib/libicudata.62.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_postgresql_rpath.log 2>&1")
                                    os.system('cd '+ dir_build +'/lib/postgresql && install_name_tool -change "/Users/2ndquadrant/pl-languages/perl-5.26/lib/CORE/libperl.dylib" "@executable_path/../../pl-languages/perl-5.26/lib/CORE/libperl.dylib" "./'+ file +'" >> '+ dir_logs +"/postgreSQL_postgresql_rpath.log 2>&1")

                            # Generating zip file
                            output_file = open("output.txt", "a")
                            output_file.write("Generating zip file ...\n")
                            output_file.close()
                            os.system("cd "+ current_project +"/"+ postgreSQL_version["full_version"] +"/build && tar -zcvf Postgresql-"+ os_name +"-"+ postgreSQL_version['full_version'] +".tar.gz "+ postgreSQL_version["major_version"] +" > "+ dir_logs +"/postgreSQL_build_zip.log 2>&1")

                            # Final message
                            output_file = open("output.txt", "a")
                            output_file.write("\n\nAll binaries are placed at : "+ dir_build +"\n")
                            output_file.close()

                            output_file = open("output.txt", "a")
                            output_file.write("Restoring system PATH ...\n")
                            output_file.close()
                            os.environ['PATH'] = system_PATH
                            time.sleep(2)

                            output_file = open("output.txt", "a")
                            output_file.write("\n\nBuild is completed successfully\n\n")
                            output_file.close()
         
                            return True
                
                        else:
                            output_file = open("output.txt", "a")
                            output_file.write("Copying openssl/lib to build fails see copy_openssl_share_lib.log for more details ...\n")
                            output_file.close()
                            build_result = 1
                    else:
                        output_file = open("output.txt", "a")
                        output_file.write("Copying share/proj to build fails see copy_proj_share_lib.log for more details ...\n")
                        output_file.close()
                        build_result = 1
                else:
                    output_file = open("output.txt", "a")
                    output_file.wite("Copying share/gdal to build fails see copy_gdal_share_lib.log for more details ...\n")
                    output_file.close()
                    build_result = 1
            else:
                output_file = open("output.txt", "a")
                output_file.write("Copying lib from share library to build fails see copy_share_lib.log for more details ...\n")
                output_file.close()
                build_result = 1
		
	
        output_file = open("output.txt", "a")	
        output_file.write("\n\n----- Running build steps -----\n\n")
        output_file.close()
    
        time.sleep(3)
       
        output_file = open("output.txt", "a")
    
        # Downloading postgreSQL source code
        output_file = open("output.txt", "a")
        output_file.write("Downloading PostgreSQL "+ postgreSQL_version['full_version'] +" source code ...\n") 
        output_file.close()
        result_postgreSQL_download = os.system(download_keyword +" "+ postgreSQL_version["url"] +" > "+ dir_logs +"/postgreSQL_download.log 2>&1")

        if result_postgreSQL_download == 0:
        
            # Unzipping postgreSQL
            output_file = open("output.txt", "a")
            output_file.write("Unzipping postgreSQL source code ...\n")
            output_file.close()
            result_postgreSQL_unzip = os.system("tar xzf postgresql-"+ postgreSQL_version["full_version"] +".tar.gz --directory "+ dir_src)
        
            # Removing source file .tar.gz
            os.system("cd "+ root +" && rm -rf postgresql-"+ postgreSQL_version['full_version'] +".tar.gz")

            if result_postgreSQL_unzip == 0:
            
                # Running configure on PostgreSQL
                output_file = open("output.txt", "a")
                output_file.write("Checking for required configure options for postgreSQL ...\n")
                output_file.close()
                configure_with = ""
                configure_flags = ""
                if config_file.pl_tcl == 1:
                   configure_with = " --with-tcl --with-tclconfig="+ pl_languages +"/Tcl-8.6/lib "
                   os.environ['TCLSH'] = pl_languages +"/Tcl-8.6/lib"               
 
                if config_file.openssl == 1:
                    configure_with = configure_with +" --with-openssl "

                if config_file.gssapi == 1:
                    configure_with = configure_with +" --with-gssapi "
            
                if config_file.python == 1:
                    configure_with = configure_with +" --with-python "

                if config_file.ldap == 1:
                    configure_with = configure_with +" --with-ldap "

                if config_file.zlib == 1:
                    configure_with = configure_with +" --with-zlib "

                if config_file.icu == 1:
                    configure_with = configure_with +" --with-icu "
                    configure_flags = configure_flags +" ICU_CFLAGS='-I"+ share_lib +"/include' ICU_LIBS='-L"+ share_lib +"/lib -licui18n -licuuc -licudata' "

                if config_file.pl_perl == 1:
                    configure_with = configure_with +" --with-perl "

                time.sleep(2)
                output_file = open("output.txt", "a")
                output_file.write("Running configure on postgreSQL ...\n")
                output_file.close()
                cd_path = dir_src +"/postgresql-"+ postgreSQL_version["full_version"]
                result_postgreSQL_configure = os.system("cd "+ cd_path +" && ./configure "+ configure_with + configure_flags +" --prefix="+ current_project +"/"+ postgreSQL_version["full_version"] +"/build/"+ postgreSQL_version['major_version'] +" > "+ dir_logs +"/postgreSQL_configure.log 2>&1") 
            
                if result_postgreSQL_configure == 0:
                
                    # Running build on postgreSQL
                    output_file = open("output.txt", "a")
                    output_file.write("Running make on postgreSQL ...\n")
                    output_file.close()
                    cd_path = dir_src +"/postgresql-"+ postgreSQL_version["full_version"]
                    result_postgreSQL_build = os.system("cd "+ cd_path +" && make world > "+ dir_logs +"/postgreSQL_build.log 2>&1")
        
                    if result_postgreSQL_build == 0:
      
                        # Running postgreSQL regression
                        output_file = open("output.txt", "a")
                        output_file.write("Running make check on PostgreSQL ...\n")
                        output_file.close()
                        cd_path = dir_src +"/postgresql-"+ postgreSQL_version["full_version"]
                        result_postgreSQL_regression = os.system("cd "+ cd_path +" && make check > "+ dir_logs +"/postgreSQL_regression.log 2>&1")

                        if result_postgreSQL_regression == 0:
                         
                            # Running postgreSQL install
                            output_file = open("output.txt", "a")
                            output_file.write("Running make install on PostgreSQL ...\n")
                            output_file.close()
                            cd_path = dir_src +"/postgresql-"+ postgreSQL_version["full_version"]
                            result_postgreSQL_install = os.system("cd "+ cd_path +" && make install-world > "+ dir_logs +"/postgreSQL_install.log 2>&1")

                            if result_postgreSQL_install == 0:
                         
                                time.sleep(2)

                                output_file = open("output.txt", "a")
                                output_file.write("\nChecking for addtional required features -----\n")
                                output_file.close()

                                time.sleep(3)


                                if config_file.postgis_required == 1:
 
                                    # Downloading postgis
                                    output_file = open("output.txt", "a")
                                    output_file.write("Downloading postgis ... "+ config_file.postgis_full_version +"\n")
                                    output_file.close()
                                    result_postgis_download = os.system(download_keyword +" "+ config_file.postgis_download_url +" > "+ dir_logs +"/postgis_download.log 2>&1")
                                    
                                    if result_postgis_download == 0:
                                        
                                        # Unzipping postgis
                                        output_file = open("output.txt", "a")
                                        output_file.write("Unzipping postgis ...\n")
                                        output_file.close()
                                        result_postgis_unzip = os.system("tar xzf postgis-"+ config_file.postgis_full_version +".tar.gz --directory "+ dir_src)

                                        # Deleting postgis.tar file
                                        os.system("cd "+ root +" && rm -rf postgis-"+ config_file.postgis_full_version +".tar.gz")

                                        if result_postgis_unzip == 0:
  
                                            # Running configure on postgis
                                            output_file = open("output.txt", "a")
                                            output_file.write("Running configure on postgis ...\n")
                                            output_file.close()
                                            cd_path = dir_src +"/postgis-"+ config_file.postgis_full_version
                                            result_postgis_Configure = os.system("cd "+ cd_path +" && ./configure --prefix="+ share_lib +" --with-pgconfig="+ dir_build +"/bin/pg_config --with-gdalconfig=" + share_lib + "/bin/gdal-config  --with-geosconfig="+ share_lib +"/bin/geos-config --with-projdir="+ share_lib +" --with-xml2config="+ share_lib +"/bin/xml2-config > "+ dir_logs +"/postgis_configure.log 2>&1")
                                      
                                            if result_postgis_Configure == 0:
                                                output_file = open("output.txt", "a")
                                                output_file.write("Running make on postgis ...\n")
                                                output_file.close()
                                                cd_path = dir_src +"/postgis-"+ config_file.postgis_full_version
                                                result_postgis_build = os.system("cd "+ cd_path +" && make > "+ dir_logs +"/postgis_build.log 2>&1")

                                                if result_postgis_build == 0:
 
                                                    # Running regression tests on postgis
                                                    output_file = open("output.txt", "a")
                                                    output_file.write("Running make check on postgis ...\n")
                                                    output_file.close()
                                                    result_init_db = os.system("cd "+ dir_build +"/bin && ./initdb -D data > "+ dir_logs +"/postgresql_init.log 2>&1")
 
                                                    if result_init_db == 0:
                                                        
                                                        # Starting the postgreSQL service
                                                        result_postgreSQL_start = os.system("cd "+ dir_build +"/bin && ./pg_ctl -D data start > "+ dir_logs +"/postgreSQL_start.log 2>&1")

                                                        if result_postgreSQL_start == 0:
                                                        
                                                            # Running make check on postgis
                                                            cd_path = dir_src +"/postgis-"+ config_file.postgis_full_version
                                                            result_postgis_regression = os.system("cd "+ cd_path +" && make check > "+ dir_logs +"/postgis_regression.log 2>&1")
                                                            
                                                            if result_postgis_regression == 0:
    
                                                                # Stopping postgreSQL service                                                            
                                                                result_postgreSQL_stop = os.system("cd "+ dir_build +"/bin && ./pg_ctl -D data stop > "+ dir_logs +"/postgreSQL_stop.log 2>&1")

                                                                if result_postgreSQL_stop != 0:
                                                     
                                                                    output_file = open("output.txt", "a")
                                                                    output_file.write("Could not able to stop postgreSQL service see postgreSQL_stop.log for more details ...\n")
                                                                    output_file.close()
                                                                    exit()
 
                                                                os.system("cd "+ dir_build +" && rm -rf data")
    
                                                                # Running make install on postgis
                                                                output_file = open("output.txt", "a")
                                                                output_file.write("Running make install on postgis ...\n")
                                                                output_file.close()
                                                                cd_path = dir_src +"/postgis-"+ config_file.postgis_full_version
                                                                result_postgis_install = os.system("cd "+ cd_path +" && make install > "+ dir_logs +"/postgis_install.log 2>&1")
	
                                                                if result_postgis_install == 0:
                                                                    output_file.close()
                                                                    if post_build_steps():
                                                                        build_result = 0
                                                                        
                                                                else:
                                                                    output_file = open("output.txt", "a")
                                                                    output_file.write("Postgis installation fails see postgis_install.log for more details ...\n")
                                                                    output_file.close()
                                                                    build_result = 1
                                                            else:
                                                                output_file = open("output.txt", "a")
                                                                output_file.write("Postgis regression fails see postgis_regression.log for more details ...\n")
                                                                output_file.close()
                                                                build_result = 1
                                                        else:
                                                            output_file = open("output.txt", "a")
                                                            output_file.write("Could not start postgreSQL service see postgreSQL_start.log for more details ...\n")
                                                            output_file.close()
                                                            build_result = 1
                                                    else:
                                                        output_file = open("output.txt", "a")
                                                        output_file.write("PostgreSQL initdb fails see postgreSQL_init.log for more details ...\n")
                                                        output_file.close()
                                                        build_result = 1
                                                else:
                                                    output_file = open("output.txt", "a")
                                                    output_file.write("Postgis build fails see postgis_build.log for more details ...\n")
                                                    output_file.close()
                                                    build_result = 1
                                            else:
                                                output_file = open("output.txt", "a")
                                                output_file.write("Postgis configure fails see postgis_configure.log for more details ...\n")
                                                output_file.close()
                                                build_result = 1
                                        else:
                                            output_file = open("output.txt", "a")
                                            output_file.write("postgis unzipping fails ...\n")
                                            output_file.close()
                                            build_result = 1
                                    else:
                                        output_file = open("output.txt", "a")
                                        output_file.write("Postgis downloading fails see postgis_download.log for more detals ...\n")
                                        output_file.close()
                                        build_result = 1
                                else:
                                    output_file = open("output.txt", "a")
                                    output_file.write("Nothing to do now ...\n")
                                    output_file.close()
                                    if post_build_steps():
                                        build_result = 0
                                        
                            else:
                                output_file = open("output.txt", "a")
                                output_file.write("PostgreSQL installations fails see postgreSQL_install.log for more details ...\n")
                                output_file.close()
                                build_result = 1
                        else:
                            output_file = open("output.txt", "a")
                            output_file.write("PostgreSQL regression fails see postgreSQL_regression.log for more details ...\n")
                            output_file.close()
                            build_result = 1
                    else:
                        output_file = open("output.txt", "a")
                        output_file.write("PostgreSQL build fails see postgreSQL_build.log for more details ...\n")
                        output_file.close()
                        build_result = 1
                else:
                    output_file = open("output.txt", "a")
                    output_file.write("PostgreSQL configure fails see postgreSQL_configure.log for more details ...\n")
                    output_file.close()
                    build_result = 1
            else:
                output_file = open("output.txt", "a")
                output_file.write("PostgreSQL unzipping failed ...\n")
                output_file.close()
                build_result = 1
        else:
            output_file = open("output.txt", "a")
            output_file.write("PostgreSQL source code downloading is failed ...\n")
            output_file.close()
            build_result = 1

except Exception as e:
    print(e)
finally:
    output_file.close()
    send__email_with_output_file()
    if build_result == 0:
     
        if os_name == "Linux":
            
            send_build_to_mac(tar_file_path, dir_logs)
        else:
            copy_build(tar_file_path, dir_logs)       
            if thread_to_call_linux_machine.is_alive():
                thread_to_call_linux_machine.join()

            os.system("mkdir "+ mac_oldbk +"")
            os.system("cp -a "+ mac_build_path +"/  "+ mac_oldbk +"")
            for file in os.listdir(mac_oldbk):
                if file.find("Windows") != -1:
                    os.system("cd "+ mac_oldbk +" && cp "+ file +" "+ installer_build +"/Windows")
                if file.find("Linux") != -1:
                    os.system("cd "+ mac_oldbk +" && cp "+ file +" "+ installer_build +"/Linux")
                if file.find("Darwin") != -1:
                    os.system("cd "+ mac_oldbk +" && cp "+ file +" "+ installer_build +"/OSX") 
            
            # Regenerating installer properties file
            f = open(""+ installer_code +"/installer-properties.sh","w+")
            f.write("__PG_MAJOR_VERSION__="+ postgreSQL_version["major_version"] +"\n")
            f.write("__FULL_VERSION__="+ postgreSQL_version["full_version"] +"\n")
            if config_file.__RELEASE__ == 1:
                f.write("__EXTRA_VERSION_STRING__=undef\n")
            else:
                f.write("__EXTRA_VERSION_STRING__=internal\n")
            f.write("__RELEASE__="+ str(config_file.__RELEASE__) +"\n")
            f.write("__BUILD_NUMBER__="+ str(config_file.__BUILD_NUMBER__) +"\n")
            f.write("__DEV_TEST__="+ config_file.__DEV_TEST__ +"\n")
            f.write("__DEBUG__="+ str(config_file.__DEBUG__) +"\n")
            f.close()
           
    os.system("cd "+ root +" && rm -rf output.txt")
