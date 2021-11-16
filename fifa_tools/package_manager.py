import os
import sys
import subprocess
from fifa_tools import se7en_helper
# path to python.exe
python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')

def checkFirstRun():
	config = se7en_helper.ReadConfig('FIFA3DIE')
	if (config['SETTINGS'].getboolean('First_Run')):
		# upgrade pip
		subprocess.call([python_exe, "-m", "ensurepip"])
		subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])

def install(pkgName):
	checkFirstRun()
	subprocess.call([python_exe, "-m", "pip", "install", pkgName])

def uninstall(pkgName):
	subprocess.call([python_exe, "-m", "pip", "uninstall", pkgName])
