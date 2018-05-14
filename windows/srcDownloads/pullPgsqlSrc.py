import windows.configFile
import windows.pathVariables
import requests
import sys



# Importing configuration and path variable file
configFile = windows.configFile.ConfigFile();
pathVariableFile = windows.pathVariables.PathVarriables();
# Process completed


class PullPgsqlSourceCode:


    def pullCode(self):
        # pre download steps

        for need in configFile.fullPgsqlVersion:
            print("Downloading PGSQL source code for ", need);
            link = "https://ftp.postgresql.org/pub/source/v"+need+"/postgresql-"+need+".tar.gz"
            file_name = "postgresql-"+need+".tar.gz"
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



