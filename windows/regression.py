import os

import windows.pathVariables


# Initializing path variable file
pathvariable = windows.pathVariables.PathVarriables;
# Process ends


class Regression:
    def startRegresstion(self):
        path = pathvariable.windowsCmd + ' /c ' + '""' + pathvariable.vsCommandPrompt64 + '" & cd ' + pathvariable.pgSqlMsvc + ' &  ' + pathvariable.regression + '"'
        os.system(path)