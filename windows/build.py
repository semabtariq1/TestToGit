import os

import windows.pathVariables


# Initializing path variable file
pathvariable = windows.pathVariables.PathVarriables;
# Process ends


class Building:

    def startBuildProcess(self, need):
        #buildTask = pathvariable.windowsCmd + ' /c ' + '""' + pathvariable.vsCommandPrompt64 + '" & cd ' + pathvariable.pgSqlMsvc + ' &  ' + pathvariable.build + '"'
        buildTask = pathvariable.windowsCmd + ' /c ' + '""' + pathvariable.vsCommandPrompt64 + '" & cd ' + pathvariable.pgsqlCode + '\\'+need+ '\\src\\postgresql-'+need+'\\src\\tools\\msvc' ' &  ' + pathvariable.build + '"'

        #os.system(buildTask)
        os.system(buildTask)
        # print(buildTask)