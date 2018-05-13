import requests
import sys

class PullOpenSsl:
    def PullOpenSsl(self):
        # Downloading Openssl
        print("Downloading Openssl");
        link = "https://slproweb.com/download/Win32OpenSSL-1_1_0h.exe"
        file_name = "Win32OpenSSL-1_1_0h.exe"
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
