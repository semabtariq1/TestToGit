# 1 for needed 0 for not needed
import json

class ConfigFile:

    postgresql = 1
    # change v to something understandable
    pgVersions = '{"v": [{"fullVersion": "11beta4", "majorVersion": "11", "minerVersion" : "beta4",' \
                 ' "url" : "https://borka.postgresql.org/staging/c45d6bda7b8a165a9b7de5a1d9a5ba5b11f7cea9/postgresql-11beta4.tar.gz"} ] }'
    decoded = json.loads(pgVersions)


    postgis = '{"postgisV": [{"fullVersion": "2.4.4", "majorVersion": "4", "minerVersion" : "4",' \
                 ' "url" : "https://download.osgeo.org/postgis/source/postgis-2.4.4.tar.gz"} ] }'
    decodedPostgis = json.loads(postgis)



