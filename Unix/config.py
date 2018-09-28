import json


class config_file:

    # Setting variables 
    linux_box = "build@54.169.212.98"
    build_code_linux = "/opt/semabHome/build-unix/PGInstaller/Unix"
    python_home = "/opt/Python-3.4.4/inst"
    openssl_home = "/opt/openssl-1.0.2g/inst"
    share_lib = "/opt/PGInstaller/Python-automation-code/linux_share_lib1"
    mac_address = "2ndquadrant@208.52.185.118"
    mac_build_path = "/Users/2ndquadrant/semabHome/releaseBuilds/test_dir"

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

    email_info = '{"email": [{"from" : "semab.tariq@2ndquadrant.com", "to" : "semab.tariq@2ndquadrant.com", "sender_password": "your password"} ] }'
    email_info_decoded = json.loads(email_info)
