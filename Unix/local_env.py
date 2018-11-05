import platform

os_name = platform.system()


pl_languages = "/Applications/2ndQuadrant/PostgreSQL/pl-languages"
python_home = "/Users/2ndquadrant/2UDA/Python-3.4.4/inst"
openssl_home = "/Users/2ndquadrant/2UDA/openssl-1.0.2g/inst"
share_lib = "/Users/2ndquadrant/pythonAutomation/srcBuild"
mac_build_path = "/Users/2ndquadrant/semabHome/main"


if os_name == "Linux":
    pl_languages = "/opt/2ndQuadrant/PostgreSQL/pl-languages"
    python_home = "/opt/Python-3.4.4/inst"
    openssl_home = "/opt/openssl-1.0.2g/inst"
    share_lib = "/opt/PGInstaller/Python-automation-code/linux_share_lib1"
    mac_address = "2ndquadrant@208.52.185.118"

else:
    linux_box = "build@54.169.212.98" 
    build_code_linux = "/opt/semabHome/build-unix-dev/PGInstaller/Unix"
    installer_build = "/Users/2ndquadrant/semabHome/temp-installer-code/Builds"
    mac_oldbk = "/Users/2ndquadrant/semabHome/oldbk/thurs12sept2018"
    installer_code = "/Users/2ndquadrant/semabHome/temp-installer-code"
