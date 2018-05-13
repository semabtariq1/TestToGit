import tarfile
import windows.pathVariables
import windows.currentDateTime



# Initializing path variable
pathVariable = windows.pathVariables.PathVarriables()
# Process ends


# Getting save date and time
savedDateTime = windows.currentDateTime.savedDateTime
# Process ends

class InstallPgsqlSrc:
    def unzipPgsqlSrc(self):
        # Unzipping PGSQL source code
        print("\nUnzipping the file...")
        fname = pathVariable.rootDirectory + "\\postgresql-10.3.tar.gz"
        tar = tarfile.open(fname, "r:gz")
        tempPathToExtract = pathVariable.rootDirectory + "\\workDir\\"+savedDateTime+"\\version\\src"
        tar.extractall(
            path=tempPathToExtract)
        tar.close()
        print("\nUnzipping completed")
        # Process completed