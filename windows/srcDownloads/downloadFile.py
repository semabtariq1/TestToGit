import requests
import sys

class DownloadFile:
    def downloadFile(self,link, fileName):
        try:
            # Downloading diff
            print("\nDownloading "+fileName+ " ..." )

            with open(fileName, "wb") as f:
                print
                "Downloading %s" % fileName
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
        except:
            print("Network issue found ... ")
            sys.exit(0)

        # Process completed
