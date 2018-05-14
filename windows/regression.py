import os

import windows.pathVariables


# Initializing path variable file
pathvariable = windows.pathVariables.PathVarriables;
# Process ends


class Regression:
    def startRegresstion(self, need):
        #path = pathvariable.windowsCmd + ' /c ' + '""' + pathvariable.vsCommandPrompt64 + '" & cd ' + pathvariable.pgSqlMsvc + ' &  ' + pathvariable.regression + '"'
        #os.system(path)
        regressionTask = pathvariable.windowsCmd + ' /c ' + '""' + pathvariable.vsCommandPrompt64 + '" & cd ' + pathvariable.pgsqlCode + '\\' + need + '\\src\\postgresql-' + need + '\\src\\tools\\msvc' ' &  ' + pathvariable.regression + '"'
        os.system(regressionTask)