# Removing zipped file after unzipping
import shutil
import time
import pathVariables


# Initializing Path variable file
pathVariable = pathVariables.PathVarriables()
# Process ends


print("Deleting extra files")
shutil.rmtree(pathVariable.rootDirectory+"\\setup")
time.sleep(3)
print("All extra files are removed")
# Process completed
