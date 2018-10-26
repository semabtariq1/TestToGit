import os
import time
import platform
import tarfile
import sys
import config
import smtplib
import requests
import shutil
from distutils.dir_util import copy_tree
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


os.system("cls")


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
    quit()


# Initializing classes
output_file = open("output.txt", "a")
output_file.write("Initializing classes ...\n")
output_file.close()
config_file = config.config_file()


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
              msg['Subject'] = "Build process completed successfully for Windows"
              body = "see following attached file for more details ..."
          else:
              msg['Subject'] = "Build process failed for Windows"
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


try:

    output_file = open("output.txt", "a")
    output_file.write("Setting up folder structure ...\n")
    output_file.close()
    time.sleep(2)
	
	
    for postgreSQL_version in config_file.postgreSQL_info_decoded['postgreSQL_version']:
        dir_src = root +"\\work_dir\\"+ current_date_time + "\\"+ postgreSQL_version['full_version'] +"\\src"
        if not os.path.exists(dir_src):
            os.makedirs(dir_src)
            output_file = open("output.txt", "a")
            output_file.write(dir_src +"\n")
            output_file.close()
			
        dir_logs = root +"\\work_dir\\"+ current_date_time + "\\"+ postgreSQL_version['full_version'] +"\\logs"    
        if not os.path.exists(dir_logs):
            os.makedirs(dir_logs)
            output_file = open("output.txt", "a")
            output_file.write(dir_logs +"\n")
            output_file.close()
			
        dir_build = root +"\\work_dir\\"+ current_date_time + "\\"+ postgreSQL_version['full_version'] +"\\build\\"+ postgreSQL_version['major_version']
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
        current_project = root +"\\work_dir\\"+ current_date_time
        cd_path = ""
        postgreSQL_build_location = current_project + "\\" + postgreSQL_version["full_version"] +"\\build\\"+ postgreSQL_version["major_version"]
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
        os.environ['PATH'] = postgreSQL_build_location +"\\bin;"+ config_file.share_lib +"\\openssl\\bin;"+ config_file.share_lib +"\\zlib\\bin;"+ config_file.share_lib +"\\icu\\bin64;"+ config_file.pl_languages +"\\perl-5.26\\bin;" + os.environ['PATH']
        os.environ['PERL5LIB'] = dir_src +"\\postgresql-"+ postgreSQL_version['full_version'] +"\\src\\tools\\msvc"
        print(os.environ['PERL5LIB'])
        time.sleep(2)

		
        output_file = open("output.txt", "a")
        output_file.write("\n\n----- Running build steps -----\n\n")
        output_file.close()
		
		
		# Downloading postgreSQL source code
        output_file = open("output.txt", "a")
        output_file.write("Downloading PostgreSQL "+ postgreSQL_version['full_version'] +" source code ...\n") 
        output_file.close()  
        r = requests.get(postgreSQL_version["url"])
        with open('postgresql-'+ postgreSQL_version["full_version"] +'.tar.gz', 'wb') as f:  
            f.write(r.content)

         
        # Unzipping postgreSQL
        output_file = open("output.txt", "a")
        output_file.write("Unzipping postgreSQL source code ...\n")
        output_file.close()
        cd_path = root + "\\postgresql-" + postgreSQL_version['full_version'] + ".tar.gz"
        tar = tarfile.open(cd_path, "r:gz")
        tar.extractall(path=root + "\\work_dir\\" + current_date_time + "\\" + postgreSQL_version['full_version'] + "\\src")
        tar.close()
			
			
        # Generating envoirnment files
        output_file = open("output.txt", "a")
        output_file.write("Generating envoirnment file\n")
        output_file.close()
        f = open(root +"\\work_dir\\"+ current_date_time +"\\"+ postgreSQL_version['full_version'] +"\\src\\postgresql-"+ postgreSQL_version['full_version'] +"\\src\\tools\\msvc\\buildenv.pl", "w+")
        f.write("$ENV{PATH}=$ENV{PATH} . ';"+ config_file.external_path +"';")
        f.close()
        time.sleep(3)
        
		
	    # Adding paths in config_default.pl file
        output_file = open("output.txt", "a")
        output_file.write("Updating config_default.pl file\n")
        output_file.close()
        number = 0
        config_default = root +"\\work_dir\\"+ current_date_time +"\\"+ postgreSQL_version['full_version'] +"\\src\\postgresql-"+ postgreSQL_version['full_version'] +"\\src\\tools\\msvc\\config_default.pl"
        file = open(config_default)
        line = file.read().splitlines()
        for li in line:
            if 'python' in li:
                if config_file.python == 1:
                    line[number] = "    python    => '"+ config_file.python_home +"',    # --with-python=<path>"
                    open(config_default, 'w').write('\n'.join(line))
				
            elif "openssl" in li:
                if config_file.openssl == 1:
                    line[number] = "    openssl   => '"+ config_file.share_lib +"\\openssl',    # --with-openssl=<path>"
                    open(config_default, 'w').write('\n'.join(line))
				
                    # Copying Openssl binaries in build
                    src = config_file.share_lib +"\\openssl"
                    dest = current_project +"\\"+ postgreSQL_version['full_version'] +"\\build\\"+ postgreSQL_version['major_version']
                    copy_tree(src, dest)
				
            elif "icu" in li:
                if config_file.icu == 1:
                    line[number] = "    icu       => '"+ config_file.share_lib +"\\icu',    # --with-icu=<path>"
                    open(config_default, 'w').write('\n'.join(line))
				
                    # Copying icu binaries in build
                    src = config_file.share_lib +"\\icu\\bin64\\"
                    dest = current_project +"\\"+ postgreSQL_version['full_version'] +"\\build\\"+ postgreSQL_version['major_version'] +"\\bin"
                    copy_tree(src, dest)
				
            elif "perl" in li:
                if config_file.perl == 1:
                    line[number] = "    perl       => '"+ config_file.pl_languages +"\\perl-5.26',             # --with-perl=<path>"
                    open(config_default, 'w').write('\n'.join(line))
			
            elif "tcl" in li:
                if config_file.tcl == 1:
                    line[number] = "    tcl       => '"+ config_file.pl_languages +"\\Tcl-8.6',             # --with-tcl=<path>"
                    open(config_default, 'w').write('\n'.join(line))
				
            elif "zlib" in li:
                if config_file.zlib == 1:
                    line[number] = "    zlib      => '"+ config_file.share_lib +"\\zlib'    # --with-zlib=<path>"
                    open(config_default, 'w').write('\n'.join(line))
				
                    # Copying Zlib binaries in build
                    src = config_file.share_lib +"\\zlib"
                    dest = current_project +"\\"+ postgreSQL_version['full_version'] +"\\build\\"+ postgreSQL_version['major_version']
                    copy_tree(src, dest)
				
            number += 1;
        file.close()
	
	
        output_file = open("output.txt", "a")
        output_file.write("Running make on postgreSQL ...\n")
        output_file.close()
        cd_path = root +"\\work_dir\\"+ current_date_time +"\\"+ postgreSQL_version['full_version'] +"\\src\\postgresql-"+ postgreSQL_version['full_version'] +"\\src\\tools\\msvc"
        result_build = os.system(config_file.windows_cmd +' /c '+'" cd /d '+ config_file.vs_command_prompt_x64 +' && vcvarsall amd64 && cd /d '+ cd_path +' && build > '+ dir_logs +'\\postgreSQL_build.log 2>&1"')
    
	
        if result_build == 0:
            output_file = open("output.txt", "a")
            output_file.write("Running make check on PostgreSQL ...\n")
            output_file.close()
            result_regression = os.system(config_file.windows_cmd +' /c '+'" cd /d '+ config_file.vs_command_prompt_x64 +' && vcvarsall amd64 && cd /d '+ cd_path +' && vcregress check > '+ dir_logs +'\\postgreSQL_regression.log 2>&1"')
        
		
            if result_regression != 0:
                output_file = open("output.txt", "a")
                output_file.write("Running make install on PostgreSQL ...\n")
                output_file.close()
                result_installation = os.system(config_file.windows_cmd +' /c '+'" cd /d '+ config_file.vs_command_prompt_x64 +' && vcvarsall amd64 && cd /d '+ cd_path +' && install '+ postgreSQL_build_location +' > '+ dir_logs +'\\postgreSQL_installation.log 2>&1"')
            
			
                if result_installation == 0:
				    # Adding postgis binaries
                    if config_file.postgis_required == 1:
                        output_file = open("output.txt", "a")
                        output_file.write("Adding postgis support ...\n")
                        output_file.close()
                        src = config_file.share_lib +"\\postgis-"+ postgreSQL_version['major_version']
                        dest = current_project +"\\"+ postgreSQL_version['full_version'] + "\\build\\" + postgreSQL_version['major_version']
                        copy_tree(src, dest)
						
						
			            # Running post build steps
                        output_file = open("output.txt", "a")
                        output_file.write("\n\n----- Running post build steps -----\n\n")   
                        output_file.close()
			
			      
				        # copying documentation into installation directory
                        output_file = open("output.txt", "a")
                        output_file.write("copying documentation files ...\n")   
                        output_file.close()
                        src = current_project +"\\" + postgreSQL_version['full_version'] +"\\src\\postgresql-" + postgreSQL_version['full_version'] \
                              + "\\doc\\src\\sgml\\html"
                        dest = current_project +"\\"+ postgreSQL_version['full_version'] +"\\build\\"+ postgreSQL_version['major_version'] +"\\doc"
                        copy_tree(src, dest)
                        time.sleep(3)
				
                        output_file = open("output.txt", "a")
                        output_file.write("copying scripts into build ...\n") 						
                        output_file.close()      				        
                        src = config_file.share_lib +"\\scripts"
                        dest = current_project +"\\" + postgreSQL_version['full_version'] +"\\build\\" + postgreSQL_version['major_version']
                        copy_tree(src, dest)
 
						# Generating final zip
                        shutil.make_archive(current_project +"\\Windows-"+ postgreSQL_version["full_version"], 'zip', current_project + "\\" + postgreSQL_version["full_version"] +"\\build")
						
						
                        build_result = 0
						
except Exception as e:
    print(e)
finally:
    output_file.close()
    send__email_with_output_file()