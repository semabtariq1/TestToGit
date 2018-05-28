import os

import windows.pathVariables
#

# Initializing path variable file
pathvariable = windows.pathVariables.PathVarriables;
# Process ends

buildTask = pathvariable.windowsCmd + ' /c ' + '""' + pathvariable.temp + '" &&   echo semab"'
result = os.system(buildTask)



