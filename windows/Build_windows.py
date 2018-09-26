import os
import time
import platform
import tarfile
import sys
import Config_file
import requests


try:

    os.system("cls")


    print("\n\n----- Running pre build steps -----\n\n")


    time.sleep(3)

    # Initializing classes
    print("Initializing classes ...")
    config_file = Config_file.config_file()

    time.sleep(2)

    # Detecting operating system
    os_name = platform.system();
    print("Detected operating system is ... "+ os_name)

    # Getting values from system
    print("Getting required values from system ...")
    current_date_time = time.strftime("%Y%m%d%H%M%S")
    root = os.path.dirname(os.path.abspath(__file__))

    time.sleep(2)
	
	# Defining custom functions
    def copy(self, src, dest):
        copy_tree(src, dest)
        return True

    print("Setting up folder structure ...")
    time.sleep(2)
    for postgreSQL_version in config_file.postgreSQL_info_decoded['postgreSQL_version']:
        dir_src = root +"\\work_dir\\"+ current_date_time + "\\"+ postgreSQL_version['full_version'] +"\\src"
        if not os.path.exists(dir_src):
            os.makedirs(dir_src)
            print(dir_src)
        dir_logs = root +"\\work_dir\\"+ current_date_time + "\\"+ postgreSQL_version['full_version'] +"\\logs"    
        if not os.path.exists(dir_logs):
            os.makedirs(dir_logs)
            print(dir_logs)
        dir_build = root +"\\work_dir\\"+ current_date_time + "\\"+ postgreSQL_version['full_version'] +"\\build\\"+ postgreSQL_version['major_version']
        if not os.path.exists(dir_build):
            os.makedirs(dir_build)
            print(dir_build)

        time.sleep(2)
		
		# Initializing variables
        print("Inintializing variables ...")
        current_project = root +"\\work_dir\\"+ current_date_time
        cd_path = ""
        postgreSQL_build_location = current_project + "\\" + postgreSQL_version["full_version"] +"\\build\\"+ postgreSQL_version["major_version"]
        
        time.sleep(2)
		
		# Saving system paths variable value to reset it again 
        print("Saving current state of system path variable ...")
        system_PATH = os.environ['PATH']
		
        time.sleep(2)

		# Setting systems path variables
        print("Setting system path variables ...")
        os.environ['PATH'] = postgreSQL_build_location +"\\bin;"+ config_file.share_lib +"\\openssl\\bin;"+ config_file.share_lib +"\\zlib\\bin;"+ config_file.share_lib +"\\icu\\bin64;" + os.environ['PATH']
        
        time.sleep(2)

		
        print("\n\n----- Running build steps -----\n\n")
		
		
		# Downloading postgreSQL source code
        print("Downloading PostgreSQL "+ postgreSQL_version['full_version'] +" source code ...")
        try:

            with open("postgresql-"+ postgreSQL_version['full_version'] +".tar.gz", "wb") as f:
                print
                "Downloading %s" % "postgresql-"+ postgreSQL_version['full_version'] +".tar.gz"
                response = requests.get(postgreSQL_version['url'], stream=True)
                total_length = response.headers.get('content-length')

                if total_length is None:  # no content length header
                    f.write(response.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=4096):
                        dl += len(data)
                        f.write(data)
                        done = int(50 * dl / total_length)
                        sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                        sys.stdout.flush()
        except Exception as e:
            print(e)
            sys.exit()
		
		# Unzipping postgreSQL source code
        print("\nUnzipping postgres "+ "postgresql-"+ postgreSQL_version['full_version'] +" ...")
        cd_path = root + "\\postgresql-" + postgreSQL_version['full_version'] + ".tar.gz"
        tar = tarfile.open(cd_path, "r:gz")
        tar.extractall(path=root + "\\work_dir\\" + current_date_time + "\\" + postgreSQL_version['full_version'] + "\\src")
        tar.close()
        print("\nUnzipping completed")
		
    # Generating envoirnment files
    print("Generating envoirnment file")
    f = open(root +"\\work_dir\\"+ current_date_time +"\\"+ postgreSQL_version['full_version'] +"\\src\\postgresql-"+ postgreSQL_version['full_version'] +"\\src\\tools\\msvc\\buildenv.pl", "w+")
    
    f.write("$ENV{PATH}=$ENV{PATH} . ';"+ config_file.external_path +"';")
    time.sleep(3)
    f.close()
    
	# Adding paths in config_default.pl file
    print("Updating config_default.pl file")
    number = 0
    config_default = root +"\\work_dir\\"+ current_date_time +"\\"+ postgreSQL_version['full_version'] +"\\src\\postgresql-"+ postgreSQL_version['full_version'] +"\\src\\tools\\msvc\\config_default.pl"
    file = open(config_default)
    line = file.read().splitlines()
    for li in line:
        if 'python' in li:
            line[number] = "    python    => '"+ config_file.python_home +"',    # --with-python=<path>"
            open(config_default, 'w').write('\n'.join(line))
        elif "openssl" in li:
            line[number] = "    openssl   => '"+ config_file.share_lib +"\\openssl',    # --with-openssl=<path>"
            open(config_default, 'w').write('\n'.join(line))
        elif "icu" in li:
            line[number] = "    icu       => '"+ config_file.share_lib +"\\icu',    # --with-icu=<path>"
            open(config_default, 'w').write('\n'.join(line))
        elif "zlib" in li:
            line[number] = "    zlib      => '"+ config_file.share_lib +"\\zlib'    # --with-zlib=<path>"
            open(config_default, 'w').write('\n'.join(line))
        number += 1;postgreSQL_version['full_version']
    file.close()
	
    print("\n\nRunning build ...")
    cd_path = root +"\\work_dir\\"+ current_date_time +"\\"+ postgreSQL_version['full_version'] +"\\src\\postgresql-"+ postgreSQL_version['full_version'] +"\\src\\tools\\msvc"
    result_build = os.system(config_file.windows_cmd +' /c '+'" cd /d '+ config_file.vs_command_prompt_x64 +' && vcvarsall amd64 && cd /d '+ cd_path +' && build > '+ dir_logs +'\\postgreSQL_build.log 2>&1"')
    
    if result_build == 0:
        print("\n\nRunning regression ...")
        result_regression = os.system(config_file.windows_cmd +' /c '+'" cd /d '+ config_file.vs_command_prompt_x64 +' && vcvarsall amd64 && cd /d '+ cd_path +' && vcregress check > '+ dir_logs +'\\postgreSQL_regression.log 2>&1"')
        if result_regression == 0:
            print("\n\nRunning instalation ...")
            result_installation = os.system(config_file.windows_cmd +' /c '+'" cd /d '+ config_file.vs_command_prompt_x64 +' && vcvarsall amd64 && cd /d '+ cd_path +' && install '+ postgreSQL_build_location +' > '+ dir_logs +'\\postgreSQL_installation.log 2>&1"')
            if result_installation == 0:
			    # copying documentation into installation directory
                print("copying documentation files ...")
                src = current_project +"\\" + postgreSQL_version['full_version'] +"\\src\\postgresql-" + postgreSQL_version['full_version'] \
                              + "\\doc\\src\\sgml\\html"
                dest = current_project +"\\"+ postgreSQL_version['full_version'] +"\\build\\"+ postgreSQL_version['full_version'] +"\\doc"
                copy(src, dest)
                time.sleep(3)
				
				# copying openssl and zlib into installation directory
                print("copying openssl, zlib, icu binaries into postgreSQL build ...")
                # openssl
                src = config_file.share_lib +"\\openssl"
                dest = current_project +"\\"+ postgreSQL_version['full_version'] +"\\build\\"+ postgreSQL_version['full_version']
                copy(src, dest)
                # zlib
                src = config_file.share_lib +"\\zlib"
                dest = current_project +"\\"+ postgreSQL_version['full_version'] +"\\build\\"+ postgreSQL_version['full_version']
                copy(src, dest)
		        # icu
                src = config_file.share_lib +"\\icu\\bin64\\"
                dest = current_project +"\\"+ postgreSQL_version['full_version'] +"\\build\\"+ postgreSQL_version['full_version'] +"\\bin"
                copy(src, dest)
                time.sleep(3)
				
				# Adding postgis binaries
                print("Adding postgis support ...")
                src = config_file.share_lib +"\\postgis-"+ postgreSQL_version['major_version']
                dest = current_project +"\\"+ postgreSQL_version['full_version'] + "\\build\\" + postgreSQL_version['full_version']
                copy(src, dest)
    
except Exception as e:
    print(e)
    sys.exit(0)