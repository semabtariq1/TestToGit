import platform
import os

os_name = platform.system()

projectName = '11_10_9.6_9.5'

pl_languages = "/Applications/2ndQuadrant/PostgreSQL/pl-languages"
python_home = "/Users/2ndquadrant/2UDA/Python-3.4.4/inst"
openssl_home = "/Users/2ndquadrant/2UDA/openssl-1.0.2g/inst"
shareLib = "/Users/2ndquadrant/pythonAutomation/srcBuild"
mac_build_path = "/Users/2ndquadrant/semabHome/main"


if os_name == "Linux":
    pl_languages = "/opt/2ndQuadrant/PostgreSQL/pl-languages"
    python_home = "/opt/Python-3.4.4/inst"
    openssl_home = "/opt/openssl-1.0.2g/inst"
    shareLib = "/opt/PGInstaller/Python-automation-code/linux_share_lib1"
    mac_address = "2ndquadrant@208.52.185.118"

else:
    """ Variables that are used to call linux machine and execute build code are ipAddr, userName, buildCode """

    ipAddr = "52.221.191.183"
    userName = "build"
    buildCode = "/opt/semabHome/postgresBuilds/dev/PGInstaller/unix"
    installer_build = "/Users/2ndquadrant/semabHome/temp-installer-code/Builds"
    mac_oldbk = "/Users/2ndquadrant/semabHome/oldbk/thurs12sept2018"
    installer_code = "/Users/2ndquadrant/semabHome/temp-installer-code"

password = ""
with open(shareLib +"/emailPassword.txt") as file:
    password = file.readline().replace('\n', "")

""" Some general variables should not be modified in any case """
root = os.path.dirname(os.path.abspath(__file__))
