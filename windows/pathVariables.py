# This class will contain all the hard coded paths

import os
import windows.currentDateTime

# Find VsCommand Window path
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
# Process completed


# Getting saved date time
savedDateTime = windows.currentDateTime.savedDateTime
# Process ends

class PathVarriables:

    vsCommandPrompt64 = (find("VsDevCmd.bat", "C:\\Program Files (x86)\\Microsoft Visual Studio\\"))
    windowsCmd = 'C:\\Windows\\system32\\cmd.exe'
    rootDirectory = os.path.dirname(os.path.abspath(__file__))
    pgSqlMsvc = os.path.dirname(os.path.abspath(__file__))+"\\workDir\\"+savedDateTime+"\\version\\src\\postgresql-10.3\\src\\tools\\msvc"
    pgsqlCode = os.path.dirname(os.path.abspath(__file__)) + "\\workDir\\"+savedDateTime

    build = "build"
    regression = "vcregress check"
    install = 'install "'+ rootDirectory+'\\workDir\\'+savedDateTime


