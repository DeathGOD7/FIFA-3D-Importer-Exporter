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
addonLoc = bpy.utils.user_resource('SCRIPTS', "addons")

vr = bl_info["version"]
version = (vr[0], vr[1], vr[2])
version_text = 'v' + str(version[0]) + '.' + \
	str(version[1]) + '.' + str(version[2])
# -----------------------------------------

# --------------- Dir Initialize ----------------
maindir = os.path.expanduser('~\Documents\SE7EN\FIFA 3D')

logdir = maindir + '\Logs'
texdir = maindir + '\Textures'
libsdir = maindir + "\Libs"

x = datetime.datetime.now()
logfilename = x.strftime("%Y-%m-%d")
logfile = logdir + f"\\{logfilename}.log"



subdirlist = [maindir, logdir, texdir, libsdir]
# -----------------------------------------

# --------------- Import Addon ----------------
from fifa_tools import se7en_helper

for x in subdirlist:
	if not os.path.exists(x):
		os.makedirs(x)

if not os.path.exists(f'{maindir}\FIFA3DIE.ini'):
	se7en_helper.CreateConfig("FIFA3DIE")

config = se7en_helper.ReadConfig('FIFA3DIE')
if (config['SETTINGS'].getboolean('First_Run')):
	se7en_helper.InstallPythonNET()

from fifa_tools import fifa3D_layout
from fifa_tools.scripts.fifa3D_logger import logger
globalLogFile = logger()
# -----------------------------------------

def register():
	fifa3D_layout.register()
	print("\nRegistering FIFA 3D Importer/Exporter")

def unregister():
	fifa3D_layout.unregister()
	print("\nUnregistering FIFA 3D Importer/Exporter")

if __name__ == "__main__":
	register()