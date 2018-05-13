import os

import windows.pathVariables


# Initializing path variable file
pathvariable = windows.pathVariables.PathVarriables;
# Process ends


class Building:

    def startBuildProcess(self):
        buildTask = pathvariable.windowsCmd + ' /c ' + '""' + pathvariable.vsCommandPrompt64 + '" & cd ' + pathvariable.pgSqlMsvc + ' &  ' + pathvariable.build + '"'
        os.system(buildTask)
