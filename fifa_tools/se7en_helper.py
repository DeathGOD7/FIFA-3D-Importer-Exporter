import fifa_tools
from fifa_tools import package_manager
import os

# Blender 2.80.0 = Python 3.7.0
# Blender 2.93.5 = Python 3.9.2

pyV = fifa_tools.pythonVer.split(sep='.')
pyC = "cp" + pyV[0] + pyV[1]

pyArc = ""

pyNET = fifa_tools.addonLoc + r"\fifa_tools\redist\PythonNET"
files = os.listdir(pyNET)

correctFile = ""

if fifa_tools.pythonArc == "64bit":
	pyArc = "amd64"
else:
	pyArc = "win32"

for x in files:
	if (pyC in x) and (pyArc in x):
		correctFile = x

def installPythonNET():
	print(f"Installing {correctFile}")
	package_manager.install(f"{pyNET}\{correctFile}")
