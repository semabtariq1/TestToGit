import os

import windows.pathVariables


# Initializing path variable file
pathvariable = windows.pathVariables.PathVarriables;
# Process ends


class Installation:
    def startInstation(self):
        path = pathvariable.windowsCmd + ' /c ' + '""' + pathvariable.vsCommandPrompt64 + '" & cd ' + pathvariable.pgSqlMsvc + ' &  ' + pathvariable.install + '"'
        os.system(path)
