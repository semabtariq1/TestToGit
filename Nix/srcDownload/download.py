import os
import paths

path = paths.Path()

class Download:
    def download(self, url, neened):
        result = os.system("wget "+ url +" > "+path.currentProject+ "/"+ neened+"/logs/download.log 2>&1")
        return result

