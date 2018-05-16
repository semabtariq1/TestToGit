import os
import windows.pathVariables


# Initializing path variables
pathVariables = windows.pathVariables.PathVarriables()
# Process ends


class InstallPython:
    def installPython(self):
        print("Installing Python")
        # installing python
        path = pathVariables.windowsCmd+" /c cd "+pathVariables.rootDirectory
        command = ' && python-3.3.0.amd64.msi /qn'
        os.system(path+command)
        print("Python installed")
        # #Process ends