import fifa_tools
import os
import configparser

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

#FIFA3DIE
def CreateConfig(cfgname, section="SETTINGS", ext="ini"):
	print("Config file is missing. Creating new one....")
	config = configparser.ConfigParser()
	config[str(section)] = {}
	defKey= "First_Run"
	defVal = "True"
	config[str(section)][str(defKey)] = str(defVal)
	print("Config file created. Writing data....")
	with open(f"{fifa_tools.maindir}\{cfgname}.{ext}",'w') as configfile:
		config.write(configfile)

	return config

def WriteConfig(cfgname, key, value, section="SETTINGS", ext="ini"):
	if not os.path.exists(f'{fifa_tools.maindir}\{cfgname}.{ext}'):
		config = CreateConfig(cfgname, section, ext)
	else:
		config = ReadConfig(cfgname, ext)

	config[str(section)][str(key)] = str(value)

	with open(f"{fifa_tools.maindir}\{cfgname}.{ext}",'w') as configfile:
		config.write(configfile)

	return config

def ReadConfig(cfgname, ext="ini"):
	config = configparser.ConfigParser()
	config.read(f"{fifa_tools.maindir}\{cfgname}.{ext}")

	return config

from fifa_tools import package_manager

def InstallPythonNET():
	print(f"Installing {correctFile}")
	package_manager.install(f"{pyNET}\{correctFile}")
	print(f"Installed PythonNET 2.5.2")
	WriteConfig("FIFA3DIE", "First_Run", "False")

