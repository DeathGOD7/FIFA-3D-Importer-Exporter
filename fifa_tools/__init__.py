bl_info = {
	"name": "FIFA 3D IMPORTER/EXPORTER",
	"description": "RX3 Importer/Exporter (Updated by Death GOD 7)",
	"author": "Death GOD 7, arti-10",
	"version": (0, 67, 'alpha'),
	"blender": (2, 80, 0),
	"location": "Toolbar [N]",
	"warning": "",  # used for warning icon and text in addons panel
	"wiki_url": "",
	"tracker_url": "",
	"category": "Import-Export"
   }

import bpy
import os
from fifa_tools import fifa3D_layout
import datetime

x = datetime.datetime.now()

addonLoc = bpy.utils.user_resource('SCRIPTS', "addons")

vr = bl_info["version"]
version = (vr[0], vr[1], vr[2])
version_text = 'v' + str(version[0]) + '.' + \
	str(version[1]) + '.' + str(version[2])

maindir = os.path.expanduser('~\Documents\SE7EN\FIFA 3D')

logdir = maindir + '\Logs'
logfilename = x.strftime("%Y-%m-%d")
logfile = maindir + f'\Logs\{logfilename}.log'

texdir = maindir + '\Textures'

subdirlist = [maindir, logdir, texdir]

def register():
	for x in subdirlist:
		if not os.path.exists(x):
			os.makedirs(x)

	if not os.path.exists(logfile):
		f = open(logfile,'a+')
		f.writelines(f'Blender Version : {bpy.app.version_string}\n')
		f.writelines(f'Addon : FIFA 3D Importer/Exporter {version_text}\n')
		f.writelines(f'Author : Death GOD 7 , arti-10\n')
		f.writelines(f'Date : {logfilename}\n')
		f.writelines('-----------------------------------------------------------------\n')

	fifa3D_layout.register()
	print("\nRegistering FIFA 3D Importer/Exporter")

def unregister():
	fifa3D_layout.unregister()
	print("\nUnregistering FIFA 3D Importer/Exporter")

if __name__ == "__main__":
	register()