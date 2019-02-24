""" Please specify the paths for each variable according to your machine """

import platform

os_name = platform.system()


pl_languages = ""
python_home = ""
openssl_home = ""
shareLib = ""
mac_build_path = ""


if os_name == "Linux":
    pl_languages = ""
    python_home = ""
    openssl_home = ""
    shareLib = ""
    mac_address = ""

else:
    """ Variables that are used to call linux machine and execute build code are ipAddr, userName, buildCode """

    ipAddr = ""
    userName = ""
    buildCode = ""
    installer_build = ""
    mac_oldbk = ""
    installer_code = ""

password = ""
with open(share_lib +"/emailPassword.txt") as file:
    password = file.readline().replace('\n', "")
