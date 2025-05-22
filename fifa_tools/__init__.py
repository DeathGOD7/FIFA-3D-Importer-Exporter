# Filename : __init__.py
# Usage : Main file to load the full addon
# Author : Death GOD 7

bl_info = {
	"name": "FIFA 3D IMPORTER/EXPORTER",
	"description": "RX3 Importer/Exporter (Updated by Death GOD 7)",
	"author": "Death GOD 7, arti-10",
	"version": (0, 70, 'alpha'),
	"blender": (2, 80, 0),
	"location": "Toolbar [N]",
	"warning": "",  # used for warning icon and text in addons panel
	"wiki_url": "https://github.com/DeathGOD7/FIFA-3D-Importer-Exporter/wiki",
	"tracker_url": "",
	"category": "Import-Export"
   }

import bpy
import os
import sys
import platform
import datetime

# --------------- Main Var ----------------
pythonVer = platform.python_version()
pythonArc = platform.architecture()[0]
addonLoc = bpy.utils.user_resource('SCRIPTS', path="addons")

vr = bl_info["version"]
version = (vr[0], vr[1], vr[2])
version_text = 'v' + str(version[0]) + '.' + \
	str(version[1]) + '.' + str(version[2])

credit1 = version_text + ", FIFA 3D Importer / Exporter "
credit2 = "Maintained & Updated by Death GOD 7"
credit3 = "(Original Author : arti-10)"

game_version = " 3D " # you can add number if you want which shows up in panel layout , removed by deathgod7
dev_status = 0

# -----------------------------------------

# --------------- Dir Initialize ----------------
# --------------- Dir Initialize ----------------
maindir = os.path.join(os.path.expanduser("~"), "Documents", "SE7EN", "FIFA3D")

# maindir = os.path.join(os.environ["USERPROFILE"], "Documents", "SE7EN", "FIFA3D")

logdir = os.path.join(maindir, 'Logs')
texdir = os.path.join(maindir, 'Textures')
libsdir = os.path.join(maindir, 'Libs')
updatesdir = os.path.join(maindir, 'Updates')

x = datetime.datetime.now()
logfilename = x.strftime("%Y-%m-%d")
logfile = os.path.join(logdir, f"{logfilename}.log")

subdirlist = [maindir, logdir, texdir, libsdir, updatesdir]
# -----------------------------------------

# --------------- Import Addon ----------------
from fifa_tools.scripts.utils import PackageManager, DependencyManager, ConfigManager, Logger, LogType

for x in subdirlist:
	if not os.path.exists(x):
		os.makedirs(x)

configManager = ConfigManager("FIFA3DIE")
packageManager = PackageManager(configManager)
dependencyManager = DependencyManager(configManager)
logFile = Logger()

isFirstRun = configManager.config['SETTINGS'].getboolean('First_Run')

import fifa_tools.scripts.fifa3D_layout as fifa3D_layout

# -----------------------------------------

def register():
	print("FIFA 3D Importer/Exporter " + version_text)
	print("Python Version: " + pythonVer + " " + pythonArc)
	print("Addon Location: " + addonLoc)
	print("FIFA 3D Directory: " + maindir)
	print("Registering FIFA 3D Importer/Exporter")
	fifa3D_layout.register()
	print("FIFA 3D Importer/Exporter registered successfully")

def unregister():
	print("Unregistering FIFA 3D Importer/Exporter")
	fifa3D_layout.unregister()
	print("FIFA 3D Importer/Exporter unregistered successfully")

if __name__ == "__main__":
	register()