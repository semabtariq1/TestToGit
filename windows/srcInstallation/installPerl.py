import os

import windows.pathVariables


# Initializing path variables
pathVariables = windows.pathVariables.PathVarriables()
# Process ends


class InstallPerl:
    def silentInstallPerl(self):
        print("Installing perl")
        path = "start /B start cmd.exe @cmd /k cd " + pathVariables.rootDirectory
        command = ' && ActivePerl-5.24.3.2404-MSWin32-x64-404865.exe /qn+ APPDIR="C:\\apps\Perl" ^ /L*v ./install.log'
        os.system(path + command)
        print("Perl installed")
        #print(path+command)