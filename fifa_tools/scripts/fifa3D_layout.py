# Filename : fifa3D_layout.py
# Usage : Defines the addon structure in Blender Sidebar
# Author : Death GOD 7


import bpy
import imp
import os
from bpy.props import *

import fifa_tools
from fifa_tools import game_version, credit1, credit2, credit3
from fifa_tools.scripts.utils import Logger
from fifa_tools.scripts import fifa3D_operators as main_operators

###SCENE CUSTOM PROPERTIES###
bpy.types.Scene.fifa3D_mode = bpy.props.EnumProperty(
	items=[
		('Legacy', 'Legacy', 'Legacy'),
		('Modern', 'Modern', 'Modern')
		],
	default='Modern',
	name="Mode")


### FIRST INSTALL PANEL
# Panel: First Install
class FIFA3D_PT_FirstInstall(bpy.types.Panel):
	"""Create category in N-Menu"""
	bl_category = "FIFA 3D I/E"

	"""Creates a Panel in Scene properties window"""
	bl_label = "FIFA" + game_version + "Initialization"
	bl_idname = "FIFA3D_PT_FirstInstall"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'

	@classmethod
	def poll(cls, context):
		from fifa_tools import isFirstRun
		return isFirstRun

	def draw(self, context):
		scn = context.scene
		layout = self.layout
		f3d_availablelibs = scn.f3d_availablelibs
		
		box = layout.box()
		box.label(icon='INFO', text='Info')
		col1 = box.column()
		col1.label(text = "Since this is your first time installing this addon.")
		col1.label(text = "Please follow the guide on how to install it properly.")
		col1.label(text = "1) Click on 'Install Python.NET'")
		col1.label(text = "2) Get the libs from github repo")
		col1.label(text = "3) Put it in your ..\\Documents\\SE7EN\FIFA3D\\Updates")
		col1.label(text = "4) Click refresh and choose the version")
		col1.label(text = "5) Click on 'Install Libs'")
		col1.label(text = "6) Voila! You installed both things")
		col1.label(text = "7) Now restart & enjoy the addon <3")
		

		box2 = layout.box()
		col2 = box2.column()

		col2.operator("fifa3d.install_pythonnet", icon='CONSOLE')

		row = box2.row()
		row.prop(f3d_availablelibs, "libs_selector", text="")
		row.operator("fifa3d.refresh_list", text="", icon='FILE_REFRESH')
		row.operator("fifa3d.install_libs", text="Install Libs", icon='IMPORT')


		col_btm = layout.column()
		col_btm.separator(factor=0.2)
		r_top = col_btm.row()
		r_top.alignment ='CENTER'
		r_top.scale_y = 1.2
		r_top.operator(
			"fifa3d.visit_github_url", text='Visit Github Wiki')
		r_top.operator(
			"fifa3d.visit_thread_url", text='Visit Official Thread')
		r_btm = col_btm.row()
		r_btm.alignment ='CENTER'
		r_btm.scale_y = 1.2
		r_btm.operator(
			"fifa3d.create_issue", text='Report Bug / Request Feature')

		col_btm.separator(factor=0.5)
		r1 = col_btm.row()
		r1.alignment = 'CENTER'
		r1.label(text=credit1)
		r2 = col_btm.row()
		r2.alignment = 'CENTER'
		r2.label(text=credit2)
		r3 = col_btm.row()
		r3.alignment = 'CENTER'
		r3.label(text=credit3)

### MAIN PANEL DEFINITION
# Shown after the first install panel is done
# This changes based on the mode selected
class FIFA3D_PT_MainPanel(bpy.types.Panel):
	"""Create category in N-Menu"""
	bl_category = "FIFA 3D I/E"

	"""Creates a Panel in Scene properties window"""
	bl_label = "FIFA" + game_version + "Main"
	bl_idname = "FIFA3D_PT_MainPanel"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'

	@classmethod
	def poll(cls, context):
		from fifa_tools import isFirstRun
		return not isFirstRun

	def draw(self, context):
		scn = context.scene
		layout = self.layout
		
		row = layout.row()
		row.alignment = "RIGHT"
		row.prop(scn, "fifa3D_mode", text="")


classes = [
	FIFA3D_PT_FirstInstall,
	FIFA3D_PT_MainPanel
]

def register():
	main_operators.register()
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():  # note how unregistering is done in reverse
	main_operators.unregister()
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)


if __name__ == "__main__":
	register()