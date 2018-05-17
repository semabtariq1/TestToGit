import os
import windows.pathVariables


# Initializing path variables
pathVariables = windows.pathVariables.PathVarriables()
# Process ends


class InstallSoftware:
    def installSoftware(self, softwareName, command):
        print("\nInstalling "+softwareName+ " ...")
        os.system(command)
        print(softwareName+ " Installed successfully ")