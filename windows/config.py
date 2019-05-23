import json


class config_file:

    # Setting variables 
    vs_command_prompt_x64 = "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC"
    windows_cmd = 'C:\\Windows\\system32\\cmd.exe'
    share_lib = "C:\\build-python-dev\\PGInstaller\\windows\\winShareLib"
    python_home = share_lib +"\\extra_utils\\python33\\Python33"
	
    # External lib path please add space after each path
    pl_languages = "C:\\pl-languages"
    external_path = share_lib +"\\extra_utils\\bin"
    perl_path = "c:\\perl"
    
    # PostgreSQL configure options (1 for build 0 for do not build)
    openssl = 1
    python = 1
    zlib = 1
    icu = 1
    perl = 1
    tcl = 1

    # PostgreSQL source code info
    postgreSQL_info = '{"postgreSQL_version": [{"full_version": "12beta1", "major_version": "12", "miner_version" : "beta1",' \
                 ' "url" : "https://borka.postgresql.org/staging/fd55cfe2850e868d9841ece8bcb4faacd86bf09b/postgresql-12beta1.tar.gz"} ] }'
    postgreSQL_info_decoded = json.loads(postgreSQL_info)

    # Additional features (1 for required 0 for not required)
    postgis_required = 0
    postgis_download_url = "https://download.osgeo.org/postgis/source/postgis-2.4.4.tar.gz"
    postgis_full_version = "2.4.4"
	
	
    email_info = '{"email": [{"from" : "semab.tariq@2ndquadrant.com", "to" : "semab.tariq@2ndquadrant.com", "sender_password": "FDSA016016semab"} ] }'
    email_info_decoded = json.loads(email_info)