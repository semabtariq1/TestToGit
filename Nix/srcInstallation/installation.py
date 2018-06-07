import os
import paths

path = paths.Path()

class Install:
    def unzipPostgresql(self, version):
        result = os.system("tar -xf postgresql-"+version+".tar.gz --directory "+path.currentProject +"/"+version +"/src")
        return result

    def installdReadline(self, needed):
        result = os.system("sudo apt-get install libreadline6 libreadline6-dev > " + path.currentProject + "/" + needed + "/logs/downloadReadLine.log 2>&1")
        return result

    def installAnyLibrary(self, needed, command):
        result = os.system(command)
        return result