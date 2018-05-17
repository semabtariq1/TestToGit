import tarfile
import windows.pathVariables
import windows.currentDateTime
import windows.configFile


# Initiliing configuration file
configFile = windows.configFile.ConfigFile();
# Process ends

# Initializing path variable
pathVariable = windows.pathVariables.PathVarriables()
# Process ends


# Getting save date and time
savedDateTime = windows.currentDateTime.savedDateTime
# Process ends

class InstallPgsqlSrc:
    def unzipPgsqlSrc(self):
        # Unzipping PGSQL source code

        print("\nUnzipping the version ...", version['fullVersion'])
        fname = pathVariable.rootDirectory + "\\postgres-"+version['fullVersion']+".tar.gz"
        tar = tarfile.open(fname, "r:gz")
        tempPathToExtract = pathVariable.rootDirectory + "\\workDir\\"+savedDateTime+"\\"+version['fullVersion']+"\\src"
        tar.extractall(path=tempPathToExtract)
        tar.close()
        print("\nUnzipping completed")
        # Process completed