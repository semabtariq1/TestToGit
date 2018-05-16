import os
import windows.pathVariables


# Initializing path variables
pathVariables = windows.pathVariables.PathVarriables()
# Process ends


class InstallDiff:
    def installDiff(self):
        # Installing deff
        print("Installing Diff")
        path = pathVariables.windowsCmd+" /c cd "+pathVariables.rootDirectory
        command = ' && diffutils-2.8.7-1.exe /SILENT, /VERYSILENT'
        os.system(path+command)

        print("Diff installed")
        # Process ends
