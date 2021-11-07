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
from fifa_tools import fifa3D_layout
fifa3D_layout.register()

def register():
    print("\nInitializing Fifa 3D Importer/Exporter")

def unregister():
    print("\nUnregistering Fifa 3D Importer/Exporter")

if __name__ == "__main__":
    register()