import os

import windows.pathVariables


# Initializing path variable file
pathvariable = windows.pathVariables.PathVarriables;
# Process ends


class Building:

    def startBuildProcess(self, need):
        # correct
        # buildTask = pathvariable.windowsCmd + ' /c ' + '""' + pathvariable.vsCommandPrompt64 + '" & cd ' + pathvariable.pgsqlCode + '\\'+need+ '\\src\\postgresql-'+need+'\\src\\tools\\msvc' ' &  ' + pathvariable.build + '"'
        # os.system(buildTask)
        # correct ends


        # Build output not showing now
        #buildTask = pathvariable.windowsCmd + ' /c ' + '""' + pathvariable.vsCommandPrompt64 + '" & cd ' + pathvariable.pgsqlCode + '\\' + need + '\\src\\postgresql-' + need + '\\src\\tools\\msvc  &  ' + pathvariable.build + ' > "' + pathvariable.pgsqlCode + '\\' + need + '\\logs\\build.log" 2>&1"'
        # os.system(buildTask)


        buildTask = pathvariable.windowsCmd + ' /c ' + '""' + pathvariable.vsCommandPrompt64 + '" & cd ' + pathvariable.pgsqlCode + '\\' + need + '\\src\\postgresql-' + need + '\\src\\tools\\msvc  &  ' + pathvariable.build + ' > "' + pathvariable.pgsqlCode + '\\' + need + '\\logs\\build.log" 2>&1"'

        result = os.system(buildTask)

        return result



