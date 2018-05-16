# Removig setup.exe files from root directory to setup folder
    # try:
    #
    #      print("removing files from root directory to setup folder required files")
    #      files = ['ActivePerl-5.24.3.2404-MSWin32-x64-404865.exe', 'diffutils-2.8.7-1.exe', 'postgresql-10.3.tar.gz', 'python-3.3.0.amd64.msi',
    #              'Win32OpenSSL-1_1_0h.exe', 'zlib-1.2.3.exe']
    #      # Creating setup folder
    #      directory = pathVariable.rootDirectory + "\\setup"
    #      if not os.path.exists(directory):
    #         os.makedirs(directory)
    #      # Process ends
    #
    #      for word in files:
    #          shutil.move(pathVariable.rootDirectory + "\\" + word, pathVariable.rootDirectory + "\\setup")
    #          #copy(pathVariable.rootDirectory + "\\" + word, pathVariable.rootDirectory + "\\setup")
    #      time.sleep(3)
    #      print("Files copied")
    #
    # except:
    #     print("No file to copy")
    # Process ends
import json

json_input = '{"persons": [{"name": "Brian", "city": "Seattle"}, {"name": "David", "city": "Amsterdam"} ] }'

try:
    decoded = json.loads(json_input)

    # Access data
    for x in decoded['persons']:
        print(x['name'])

except (ValueError, KeyError, TypeError):
    print
    "JSON format error"