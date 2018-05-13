import requests
import sys

class PullPython:
    def PullPython(self):
        # Downloading python
        print("Downloading Python");
        link = "https://www.python.org/ftp/python/3.3.0/python-3.3.0.amd64.msi"
        file_name = "python-3.3.0.amd64.msi"
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
