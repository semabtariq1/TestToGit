import windows.configFile
import windows.pathVariables
import time
import requests
import sys
import tarfile
import os



# Importing configuration and path variable file
configFile = windows.configFile.ConfigFile();
pathVariableFile = windows.pathVariables.PathVarriables();
# Process completed


class PullPgsqlSourceCode:


    def pullCodeAndUnzip(self):
        # Downloading PGSQL source code
        print("Downloading PGSQL source code");
        link = "https://ftp.postgresql.org/pub/source/v10.3/postgresql-10.3.tar.gz"
        file_name = "postgresql-10.3.tar.gz"
        with open(file_name, "wb") as f:
            print
            "Downloading %s" % file_name
            response = requests.get(link, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()
        print("\nDownloading completed");
        # Process completed



            # # Unzipping PGSQL source code
            # print("\nUnzipping the file total file size is 119 mb please be patience ")
            # fname = pathVariableFile.rootDirectory+"\\postgresql-10.3.tar.gz"
            # tar = tarfile.open(fname, "r:gz")
            # tempPathToExtract = pathVariableFile.rootDirectory+"\\Downloading\\Downloaded"
            # tar.extractall(
            #     path=tempPathToExtract)
            # tar.close()
            # print("\nUnzipping completed")
            # # Process completed

