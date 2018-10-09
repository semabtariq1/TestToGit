import json


class config_file:

    # Setting variables 
    vs_command_prompt_x64 = "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC"
    windows_cmd = 'C:\\Windows\\system32\\cmd.exe'
    share_lib = "C:\\semabHome\\PGInstaller\\windows\\winShareLib"
    python_home = "C:\\semabHome\\PGInstaller\\windows\\winShareLib\\extra_utils\\python33\\Python33"
    # External lib path please add space after each path
    external_path = "C:\\semabHome\\PGInstaller\\windows\\winShareLib\\extra_utils\\bin"
    perl_path = "c:\\perl"
    
    # PostgreSQL configure options (1 for build 0 for do not build)
    with_openssl = 1
    with_gssapi = 1
    with_python = 0
    with_ldap = 1
    with_zlib = 1
    with_icu = 1

    # PostgreSQL source code info
    postgreSQL_info = '{"postgreSQL_version": [{"full_version": "10.4", "major_version": "10", "miner_version" : "4",' \
                 ' "url" : "https://ftp.postgresql.org/pub/source/v10.4/postgresql-10.4.tar.gz"} ] }'
    postgreSQL_info_decoded = json.loads(postgreSQL_info)

    # Additional features (1 for required 0 for not required)
    postgis_required = 1
    postgis_download_url = "https://download.osgeo.org/postgis/source/postgis-2.4.4.tar.gz"
    postgis_full_version = "2.4.4"
	
	