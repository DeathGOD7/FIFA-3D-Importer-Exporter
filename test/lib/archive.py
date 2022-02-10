# Filename : archive_handler.py
# Usage : Used in extracting or compressing files in tar.gz (DeathGOD7 Custom File)
# Author : Death GOD 7

import tarfile
import os

def compress(path, archivename, ext=None):
	if ext != None:
		files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) if f.endswith(f".{ext}")]
	else:
		files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

	print(f"Compressing : {files}")

	with tarfile.open(f"{path}\{archivename}.tar.gz","w:gz") as tar:
		for file in files:
			tar.add(os.path.basename(file))
	
	print(f"Files Compressed.")

def decompress(archivename, path = ""):
	if tarfile.is_tarfile(archivename):
		if path == "":
			outdir = "."
		else:
			outdir = path

		if archivename.endswith("tar.gz"):
			tar = tarfile.open(archivename, "r:gz")
			tar.extractall(outdir)
			tar.close()
		elif archivename.endswith("tar"):
			tar = tarfile.open(archivename, "r:")
			tar.extractall(outdir)
			tar.close()
	else:
		print(f"Given file is not tar file.")

xas = "E:\\SE7EN\\Github\\FIFA 3D Importer Exporter\\test\\lib\\"
compress(xas, "FIFA3D_Libs", "dll")