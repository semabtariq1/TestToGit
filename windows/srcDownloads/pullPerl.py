import requests
import sys

class PullPerl:
    def pullPerl(self):
        # Downloading ActivePerl-5.24.3.2404-MSWin32-x64-404865.exe
        print("Downloading perl");
        link = "http://downloads.activestate.com/ActivePerl/releases/5.24.3.2404/ActivePerl-5.24.3.2404-MSWin32-x64-404865.exe"
        file_name = "ActivePerl-5.24.3.2404-MSWin32-x64-404865.exe"
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
