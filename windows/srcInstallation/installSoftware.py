import os
import tarfile

import pathVariables

import currentDateTime


# Initializing path variables
pathVariable = pathVariables.PathVarriables()
# Process ends


# Getting save date and time
savedDateTime = currentDateTime.savedDateTime
# Process ends


class InstallSoftware:
    def installSoftware(self, softwareName, command):
        print("\nInstalling "+softwareName+ " ...")
        os.system(command)
        os.system("exit")
        print(softwareName+ " Installed successfully ")

    # Seperatte function for unzip rar
    def unzipPostgres(self, version):
        print("\nUnzipping postgres "+ version+ " ...")
        fname = pathVariable.rootDirectory + "\\postgres-" + version + ".tar.gz"
        tar = tarfile.open(fname, "r:gz")
        tempPathToExtract = pathVariable.rootDirectory + "\\workDir\\" + savedDateTime + "\\" + version + "\\src"
        tar.extractall(path=tempPathToExtract)
        tar.close()
        print("\nUnzipping completed")

    def unzipQuantile(self):
        print("\nUnzipping Quantile ... ")
        fname = pathVariable.rootDirectory + "\\quantile-master.zip"
        tar = tarfile.open(fname, "r:gz")
        tempPathToExtract = pathVariable.rootDirectory + "\\winShareLib\\quantile"
        tar.extractall(path=tempPathToExtract)
        tar.close()
        print("\nUnzipping completed")