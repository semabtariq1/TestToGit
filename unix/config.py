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
. Perl
. Tcl

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
from local_env import *

""" Class called config_file will be responsible of holding all 
the configuration related properties """
 


""" Variable if 0 Linux build machine will not be called and if 1 it will be called """

callLinuxBuildMachine = 0

""" PostgreSQL configure options 
1 = enable
0 = disable """

pl_tcl = 1
pl_perl = 1
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


# Installer properties
__RELEASE__ = 0
__BUILD_NUMBER__ = 1
__DEV_TEST__ = "release"
__DEBUG__ = 0


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

postgis_required = 0
postgis_download_url = "https://download.osgeo.org/postgis/source/postgis-2.4.4.tar.gz"
postgis_full_version = "2.4.4"


""" email_info is an json array if you want build result 
in your email then you need to provide your 
credential accordingly.
For email password you need to place an file in share library root named emailPassword.txt
and type your password in that file.

Note:
If you wish to use Gmail then To use this facility 
you must enable 
allow less secure apps from your emails settings
    
Visit this link to get more details
ttps://support.google.com/a/answer/6260879?hl=en """
print("pass = "+ password )
email_info = '{"email": [{"from" : "semab.tariq@2ndquadrant.com", "to" : "semab.tariq@2ndquadrant.com", "sender_password" : "'+ password +'" }]}'
email_info_decoded = json.loads(email_info)
