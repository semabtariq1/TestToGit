import os

import windows.pathVariables


# Initializing path variable file
pathvariable = windows.pathVariables.PathVarriables;
# Process ends


class Regression:
    def startRegresstion(self, need):
        # Working fine
        # regressionTask = pathvariable.windowsCmd + ' /c ' + '""' + pathvariable.vsCommandPrompt64 + '" & cd ' + pathvariable.pgsqlCode + '\\' + need + '\\src\\postgresql-' + need + '\\src\\tools\\msvc' ' &  ' + pathvariable.regression + '"'
        # os.system(regressionTask)

        regressionTask = pathvariable.windowsCmd + ' /c ' + '""' + pathvariable.vsCommandPrompt64 + '" & cd ' + pathvariable.pgsqlCode + '\\' + need + '\\src\\postgresql-' + need + '\\src\\tools\\msvc  &  ' + pathvariable.regression + ' > "' + pathvariable.pgsqlCode + '\\' + need + '\\logs\\regress.log" 2>&1"'
        os.system(regressionTask)
        #print(regressionTask)