# 1 for needed 0 for not needed
import json

class ConfigFile:

    pgSql = 1
    pgVersions = '{"v": [{"fullVersion": "10.4", "majorVersion": "10", "minerVersion" : "4"} ] }'
    decoded = json.loads(pgVersions)

    perl = ["0", "http://downloads.activestate.com/ActivePerl/releases/5.24.3.2404/ActivePerl-5.24.3.2404-MSWin32-x64-404865.exe",
              "ActivePerl-5.24.3.2404-MSWin32-x64-404865.exe"]

    diff = ["0", "https://excellmedia.dl.sourceforge.net/project/gnuwin32/diffutils/2.8.7-1/diffutils-2.8.7-1.exe",
              "diffutils-2.8.7-1.exe"]

    zlib = ["0", "https://excellmedia.dl.sourceforge.net/project/gnuwin32/zlib/1.2.3/zlib-1.2.3.exe",
              "zlib-1.2.3.exe"]

    openssl = ["0", "https://slproweb.com/download/Win32OpenSSL-1_1_0h.exe",
              "Win32OpenSSL-1_1_0h.exe"]

    python = ["0", "https://www.python.org/ftp/python/3.3.0/python-3.3.0.amd64.msi",
              "python-3.3.0.amd64.msi"]
