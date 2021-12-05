# Filename : archive_handler.py
# Usage : Used in extracting or compressing files in tar.gz (DeathGOD7 Custom File)
# Author : Death GOD 7


import os
import shutil
import zlib
import zipfile

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

if os.path.exists(".\\FIFA 3D Importer Exporter v0.70.0a.zip"):
	os.remove(".\\FIFA 3D Importer Exporter v0.70.0a.zip")
zipf = zipfile.ZipFile('FIFA 3D Importer Exporter v0.70.0a.zip', 'w', zipfile.ZIP_DEFLATED)
zipdir('./fifa_tools', zipf)
zipf.close()

with open("Test Count.txt", "r+") as f:
	count = int(f.read())
	count = count + 1
	f.seek(0)
	f.write(str(count))



