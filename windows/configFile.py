# 1 for needed 0 for not needed
import json

class ConfigFile:

    pgSql = 1

    pgVersions = '{"v": [{"fullVersion": "10.4", "majorVersion": "10", "minerVersion" : "4"},  {"fullVersion": "9.6.9", "majorVersion": "9.6", "minerVersion" : "9"} ] }'
    decoded = json.loads(pgVersions)

    perl = 0

    deff = 0

    zlib = 0

    openssl = 0

    python = 0
