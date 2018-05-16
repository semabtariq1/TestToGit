import os

import windows.pathVariables


# Initializing path variable file
pathvariable = windows.pathVariables.PathVarriables;
# Process ends


class Building:

    def startBuildProcess(self, need):
        buildTask = pathvariable.windowsCmd + ' /c ' + '""' + pathvariable.vsCommandPrompt64 + '" & cd ' + pathvariable.pgsqlCode + '\\'+need+ '\\src\\postgresql-'+need+'\\src\\tools\\msvc' ' &  ' + pathvariable.build + '"'
        os.system(buildTask)

        #buildTask = pathvariable.windowsCmd + ' /c echo semab & echo tariq"'
        # buildTask = pathvariable.windowsCmd + ' /c ' + '""' + pathvariable.vsCommandPrompt64 + '" & cd ' + pathvariable.pgsqlCode + '\\'+need+ '\\src\\postgresql-'+need+'\\src\\tools\\msvc' ' &  echo hello"'
        #
        # os.system(buildTask)
        #print(buildTask)