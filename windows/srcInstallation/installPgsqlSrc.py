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
        for need in configFile.fullPgsqlVersion:
            print("\nUnzipping the version ...", need)
            fname = pathVariable.rootDirectory + "\\postgresql-"+need+".tar.gz"
            tar = tarfile.open(fname, "r:gz")
            tempPathToExtract = pathVariable.rootDirectory + "\\workDir\\"+savedDateTime+"\\"+need+"\\src"
            tar.extractall(
                path=tempPathToExtract)
            tar.close()
            print("\nUnzipping completed")
        # Process completed