import os
import windows.pathVariables


# Initializing path variables
pathVariables = windows.pathVariables.PathVarriables()
# Process ends


class InstallZlib:
    def installZlib(self):
        # Installing Zlib
        #path = "start /B start cmd.exe @cmd /c cd "+pathVariables.rootDirectory
        path = pathVariables.windowsCmd+" /c cd "+pathVariables.rootDirectory
        command = ' && zlib-1.2.3.exe /SILENT, /VERYSILENT'
        os.system(path+command)
        # # Process ends