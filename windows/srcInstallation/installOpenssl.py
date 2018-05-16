import os
import windows.pathVariables


# Initializing path variables
pathVariables = windows.pathVariables.PathVarriables()
# Process ends


class InstallOpenssl:
    def installOpenssl(self):
        # Installing Openssl
        print("Installing Openssl")
        path = pathVariables.windowsCmd+" /c cd "+pathVariables.rootDirectory
        command = ' && Win32OpenSSL-1_1_0h.exe /SILENT, /VERYSILENT'
        os.system(path+command)
        print("Openssl installed")
        # Process ends