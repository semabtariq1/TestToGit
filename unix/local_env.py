import platform
import os

os_name = platform.system()

projectName = '11_10_9.6_9.5'

pl_languages = "/Applications/2ndQuadrant/PostgreSQL/pl-languages"
python_home = "/Users/2ndquadrant/2UDA/Python-3.4.4/inst"
openssl_home = "/Users/2ndquadrant/2UDA/openssl-1.0.2g/inst"
shareLib = "/Users/2ndquadrant/pythonAutomation/srcBuild"
signingPasswordRoot = '/Users/2ndquadrant/semabHome/automation/codesign/signing'
bitrockInstallation = '/Applications/BitRockInstallBuilderProfessional16'
omnidbUrl = 'https://omnidb.org/dist/2.16.0/omnidb-app_2.16.0-mac.dmg'
projectFileName = 'PGInstaller.xml'


if os_name == "Linux":
    pl_languages = "/opt/2ndQuadrant/PostgreSQL/pl-languages"
    python_home = "/opt/Python-3.4.4/inst"
    openssl_home = "/opt/openssl-1.0.2g/inst"
    shareLib = "/opt/PGInstaller/Python-automation-code/linux_share_lib1"
    signingPasswordRoot = '/opt/semabHome/automation/postgres-installer-private/signing'
    bitrockInstallation = '/opt/semabHome/bitrock/installation/'

else:
    """ Variables that are used to call linux machine and execute build code are ipAddr, userName, buildCode """


""" Some general variables should not be modified in any case """
root = os.path.dirname(os.path.abspath(__file__))
