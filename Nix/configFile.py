# 1 for needed 0 for not needed
import json

class ConfigFile:

    postgresql = 1
    # change v to something understandable
    pgVersions = '{"v": [{"fullVersion": "10.3", "majorVersion": "10", "minerVersion" : "3",' \
                 ' "url" : "https://ftp.postgresql.org/pub/source/v10.4/postgresql-10.4.tar.gz"} ] }'
    decoded = json.loads(pgVersions)

    diff = ["1", "https://excellmedia.dl.sourceforge.net/project/gnuwin32/diffutils/2.8.7-1/diffutils-2.8.7-1.exe",
              "diffutils-2.8.7-1.exe"]

    python = ["1", "https://www.python.org/ftp/python/3.3.0/python-3.3.0.amd64.msi",
              "python-3.3.0.amd64.msi"]
