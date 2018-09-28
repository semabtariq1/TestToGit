""" ------------------------------------------------------------
config --- Configuration file for building postgreSQL on Unix

config file provide you different options to controll 
postgreSQL building process. With different switches you can
enable or disable the additional features. you can find the
supported features list bellow
. Openssl
. Gssapi 
. Python 
. Ldap
. Zlib
. Icu 

Note:
This build code only handles those features which are 
provided by default if you want to add any feature which is 
not listed above then you need to modify the actuall code to
handle that extra feature from build-nix file  

This file is purely written in python. For more details about 
this file please drop an email at semab.tariq@2ndquadrant.com

PGInstaller/config.py

------------------------------------------------------------ """

import json


""" Class called config_file will be responsible of holding all 
the configuration related properties """
 
class config_file:


    """ This is the most important step for anyone who wants
    to build postgresQL. All you need to do is to provide
    different paths according to your system """
    
    """ Paths that you must change """

    python_home = "path to inst directory"
    openssl_home = "path to inst directory"
    share_lib = "path to where ypu have all the prebuild binaries"


    """ In addition if you want to controll 2 different 
    machines at the same time then you need to set
    these paths as well 
   
    Note:
    We are using Linux and MacOS plateforms to run build 
    at the same time """


    """ credential of Linux machine """

    linux_box = "username@ip" 
    build_code_linux = "path to Unix where you clone build code"

    """ credential of MacOS machine """

    mac_address = "username@ip"
    mac_build_path = "Path where you want to place builds"


    """ PostgreSQL configure options 
    1 = enable
    0 = disable """

    openssl = 1
    gssapi = 1
    python = 1
    ldap = 1
    zlib = 1
    icu = 1


    """ postgreSQL_info is a json array which will hold
    all the information about postgreSQL
    which is going to build """

    postgreSQL_info = '{"postgreSQL_version": [{"full_version": "10.4", "major_version": "10", "miner_version" : "4",' \
                 ' "url" : "https://ftp.postgresql.org/pub/source/v10.4/postgresql-10.4.tar.gz"} ] }'
    postgreSQL_info_decoded = json.loads(postgreSQL_info)


    """ PostGIS is a spatial database extender for 
    PostgreSQL object-relational database. 
    It adds support for geographic objects allowing 
    location queries to be run in SQL. 
   
    As said this is the additional feature you can always 
    controll it by providing 1 or 0 (enable or disable) to 
    postgis_required variable by default it is enable

    Note:
    Postgis will be only available for stable releases 
    of postgreSQL """

    postgis_required = 1
    postgis_download_url = "https://download.osgeo.org/postgis/source/postgis-2.4.4.tar.gz"
    postgis_full_version = "2.4.4"


    """ email_info is an json array if you want build result 
    in your email then you need to provide your 
    credential accordingly 

    Note:
    If you wish to use Gmail then To use this facility 
    you must enable 
    allow less secure apps from your emails settings
    
    Visit this link to get more details
    https://support.google.com/a/answer/6260879?hl=en """

    email_info = '{"email": [{"from" : "your email", "to" : "to whom you want to send", "sender_password": "your password"} ] }'
    email_info_decoded = json.loads(email_info)
