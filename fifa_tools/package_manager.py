import os
import sys
import subprocess
 
# path to python.exe
python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
 
# upgrade pip
subprocess.call([python_exe, "-m", "ensurepip"])
subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])

def install(pkgName):
	subprocess.call([python_exe, "-m", "pip", "install", pkgName])

def uninstall(pkgName):
	subprocess.call([python_exe, "-m", "pip", "uninstall", pkgName])
