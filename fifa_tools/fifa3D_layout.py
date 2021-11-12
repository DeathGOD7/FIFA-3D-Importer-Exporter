# bl_info = {
# 	"name": "FIFA 3D IMPORTER/EXPORTER",
# 	"description": "RX3 Importer/Exporter (Updated by Death GOD 7)",
# 	"author": "Death GOD 7, arti-10",
# 	"version": (0, 67, 'alpha'),
# 	"blender": (2, 80, 0),
# 	"location": "Toolbar [N]",
# 	"warning": "",  # used for warning icon and text in addons panel
# 	"wiki_url": "",
# 	"tracker_url": "",
# 	"category": "Import-Export"
#    }

from fifa_tools import bl_info
vr = bl_info["version"]
version = (vr[0], vr[1], vr[2])
#version = (0, 67, 'alpha')

import bpy
import imp
import os
from bpy.props import *
from bpy.types import Operator
#import sys 

linux_path = '/media/2tb/Blender/blender-2.71-windows64'

# Detect different operating system

if os.name == 'nt':  # windows detected
	print('\nWindows Platform Detected')
	prePath = ''
else:
	prePath = linux_path + os.sep

# fifa_operators_path = 'fifa_tools' + os.sep + \
#     'scripts' + os.sep + 'fifa3D_operators.py'
# fifa_operators = imp.load_source(
# 	'fifa_operators', prePath + fifa_operators_path)

from fifa_tools.scripts import fifa3D_main
from fifa_tools.scripts import fifa3D_operators
from fifa_tools.scripts import fifa3D_functions
from fifa_tools.scripts import half

#from fifa_tools.scripts.fifa3D_operators import light_props as light_props

#fifa3D_operators.outregister()

version_text = 'v' + str(version[0]) + '.' + \
	str(version[1]) + '.' + str(version[2])

credit1 = version_text + ", FIFA 3D Importer / Exporter "
credit2 = "Maintained & Updated by Death GOD 7"
credit3 = "(Original Author : arti-10)"

game_version = " " # you can add number if you want which shows up in panel layout , removed by deathgod7
dev_status = 0

###VERTEX GROUP PANEL###

class FIFA_PT_CrowdSection(bpy.types.Panel):

	"""Creates a Panel in the Object properties window"""
	bl_label = "FIFA 3D IE - Stadium Crowd Tools"
	bl_idname = "FIFA_PT_CrowdSection"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "data"

	def draw(self, context):

		layout = self.layout
		scn = bpy.context.scene

		row = layout.row()
		row.label(icon='INFO', text='Crowd Assignment')
		if not context.object.name.split(sep='_')[0] == 'crowd':
			row = layout.row()
			row.label(
				text='Not a Crowd Object, select one to activate the panel')
		else:
			row = layout.row()
			row.prop(scn, 'crowd_type_enum')
			row.prop(scn, 'crowd_fullness_enum')
			row.operator("mesh.assign_crowd_type", icon='PLUS')

			row = layout.row()
			row.label(icon='INFO', text='Seat Alignment')
			row = layout.row()
			row.prop(scn, 'crowd_align_enum')
			row.operator("mesh.align_crowd_seats")

		col = layout.column()
		r3 = col.row()
		r3.alignment ='CENTER'
		r3.scale_y = 1.2
		r3.operator(
			"system.visit_github_url", text='Visit Github Wiki')
		r3.operator(
			"system.visit_thread_url", text='Visit Official Thread')

		r1 = col.row()
		r1.alignment = 'CENTER'
		r1.label(text=credit1)
		r2 = col.row()
		r2.alignment = 'CENTER'
		r2.label(text=credit2)
		r3 = col.row()
		r3.alignment = 'CENTER'
		r3.label(text=credit3)

# FACEGEN PANEL
# class FaceGenSection(bpy.types.Panel):
	# """Creates a Panel in the Object properties window"""
	# bl_label = "FIFA 3D IE - FaceGen Tools"
	# bl_idname = "facegen_panel"
	# bl_space_type = 'PROPERTIES'
	# bl_region_type = 'WINDOW'
	# bl_context = "data"
	# def draw(self,context):

		# layout=self.layout
		# scn=bpy.context.scene

		# row=layout.row()
		# row.label(icon='INFO',text='FaceGen Tools')
		# row=layout.row()
		# row.operator('mesh.ob_vertex_groups_separate')


# MAIN PANEL DEFINITION


# -------------------------------------------------------------------
#   SE7EN Functions
# -------------------------------------------------------------------



class FIFA_PT_Vertex_color_panel(bpy.types.Panel):

	"""Creates a Panel in the Object properties window"""
	bl_label = "FIFA 3D IE - Vertex Coloring Panel"
	bl_idname = "FIFA_PT_Vertex_color_panel"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "data"

	def draw(self, context):
		scn = bpy.context.scene

		layout = self.layout

		box = layout.box()
		box.label(text='Custom Face Painter', icon='INFO')
		row = box.row()
		col_l = row.column()
		col_r = row.column()

		row = col_l.row()

		row.template_color_picker(
			scn, 'vx_color', value_slider=True, lock=False, lock_luminosity=False)

		row = col_l.row()
		row.prop(scn, 'vx_color', text='')

		row = col_r.row()
		row = col_r.row()
		row = col_r.row()
		row = col_r.row()
		row = col_r.row()
		row.prop(scn, 'vx_color_hex')
		row.operator("mesh.color_assign", icon='TRIA_UP', text='')
		row.operator('mesh.color_get_hex', icon='TRIA_DOWN', text='')
		row = col_r.row()
		row.scale_y = 2
		row.operator('mesh.paint_faces')
		row = layout.row()

		box = layout.box()
		box.label(text='Auto Painter', icon='INFO')
		col = box.column()
		row = col.row()
		row.scale_y = 1.4
		row.prop(scn, 'autopaint_modes')
		row = col.row()
		row.scale_y = 1.4
		row.operator('mesh.auto_paint_mesh')

		col = layout.column()
		r3 = col.row()
		r3.alignment ='CENTER'
		r3.scale_y = 1.2
		r3.operator(
			"system.visit_github_url", text='Visit Github Wiki')
		r3.operator(
			"system.visit_thread_url", text='Visit Official Thread')

		r1 = col.row()
		r1.alignment = 'CENTER'
		r1.label(text=credit1)
		r2 = col.row()
		r2.alignment = 'CENTER'
		r2.label(text=credit2)
		r3 = col.row()
		r3.alignment = 'CENTER'
		r3.label(text=credit3)


class FIFA_PT_lights_panel(bpy.types.Panel):
	bl_label = "FIFA 3D IE - Light Configuration Panel"
	bl_idname = "FIFA_PT_lights_panel"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "data"

	def draw(self, context):
		ob = context.object
		layout = self.layout

		if ob.type == 'EMPTY' and ob.name[0:7] == 'LIGHTS_':
			box = layout.box()
			box.label(icon='INFO', text='Emit Box Properties')
			col = box.column()

			for attr in dir(ob.emitbox_props):
				if attr in light_props:
					row = col.row()
					# row.alignment='EXPAND'
					row.label(text=attr)
					split = row.split()
					#split.alignment = 'CENTER'
					split.scale_x = 1
					split.prop(ob.emitbox_props, attr, text='')

			box = layout.box()
			box.label(icon='INFO', text='Action Render Properties')
			actionrend_col = box.column()

			for k in range(len(light_props)):
				op = light_props[k]

				if op.__class__.__name__ == 'str':
					try:
						val = getattr(ob.actionrender_props, op)
						row = actionrend_col.row()
						row.label(text=op)
						split = row.split()
						split.scale_x = 1
						split.prop(ob.actionrender_props, op, text='')
					except:
						print('Bump')

				elif op.__class__.__name__ == 'list':
					try:
						val = getattr(ob.actionrender_props, op[0])
						row = actionrend_col.row()
						row.label(text=op[0])
						split = row.split()
						# split_scale_x=0.4

						split.prop(ob.actionrender_props, op[0], text='')

						if val == 'lynxVbeam.fx':
							sect = 2
						else:
							sect = 1

						if val:
							row = actionrend_col.row()
							subbox = row.box()
							subbox.label(
								icon='SETTINGS', text=op[0] + ' properties')
							subboxcol = subbox.column()
							for subprop in op[sect]:
								print(subprop)
								row = subboxcol.row()
								row.label(text=subprop)
								split = row.split()
								split_scale_x = 0.4
								split.prop(
									ob.actionrender_props, subprop, text='')
					except:
						print('')
		
		col = layout.column()
		r3 = col.row()
		r3.alignment ='CENTER'
		r3.scale_y = 1.2
		r3.operator(
			"system.visit_github_url", text='Visit Github Wiki')
		r3.operator(
			"system.visit_thread_url", text='Visit Official Thread')

		r1 = col.row()
		r1.alignment = 'CENTER'
		r1.label(text=credit1)
		r2 = col.row()
		r2.alignment = 'CENTER'
		r2.label(text=credit2)
		r3 = col.row()
		r3.alignment = 'CENTER'
		r3.label(text=credit3)


class FIFA_PT_FifaImporter(bpy.types.Panel):
	"""Create category in N-Menu"""
	bl_category = "FIFA 3D I/E"

	"""Creates a Panel in Scene properties window"""
	bl_label = "FIFA" + game_version + "3D Importer"
	bl_idname = "FIFA_PT_FifaImporter"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	#bl_context = "scene"

	###MAIN PANEL INTERFACE###
	def draw(self, context):
		scn = context.scene

		layout = self.layout

		row = layout.row()
		row.label(icon='INFO', text='Main File')
		box = layout.box()

		col = box.column()
		col.alignment = 'EXPAND'
		row = col.row()
		row.alignment = 'RIGHT'
		# row.scale_x=0.5
		row.label(text='  Game Version')
		row.prop(scn, 'game_enum', text='')
		row = col.row()
		row.alignment = 'EXPAND'
		col.separator()
		row.prop(scn, 'model_import_path')
		row = col.row()

		innerbox = row.box()
		innerbox.scale_x = 0.7
		innerbox.label(text='All Models')
		col = innerbox.column()
		col.scale_y = 1.2
		col.prop(scn, 'geometry_flag')
		col.prop(scn, 'trophy_flag')
		col.prop(scn, 'bone_groups_flag')

		innerbox = row.box()
		innerbox.scale_x = 0.7
		innerbox.label(text='Stadiums Only')
		col = innerbox.column()
		col.scale_y = 1.2
		col.prop(scn, 'materials_flag')
		col.prop(scn, 'props_flag')
		col.prop(scn, 'collision_flag')

		col = row.column()

		innerbox = col.box()
		innerbox.scale_x = 0.7
		innerbox.label(text='Faces Only')
		innerbox.prop(scn, 'bones_flag')

		row = layout.row()
		row.label(icon='INFO', text='Additional Model Files')
		box = layout.box()
		col = box.column()

		row = col.row()
		row.prop(scn, 'hair_import_path')
		row = col.row()
		row.prop(scn, 'obj_path')
		row = col.row()
		row.prop(scn, 'crwd_import_path')
		row = col.row()
		row.prop(scn, 'lnx_import_path')

		row = layout.row()
		row.label(text='Texture Files', icon='INFO')
		box = layout.box()
		col = box.column()
		row = col.row()
		row.prop(scn, 'stadium_texture_import_path')
		row = col.row()
		row.prop(scn, 'face_texture_import_path')
		row = col.row()
		row.prop(scn, 'hair_texture_import_path')
		row = col.row()
		row.prop(scn, 'eyes_texture_import_path')
		
		row = col.row()
		row.alignment = 'CENTER'
		row.scale_y = 1.2
		sc1 = row.column()
		sc1.enabled = not scn.materials_flag
		sc1.prop(scn, 'create_materials_flag')
		sc2 = row.column()
		sc2.operator("mesh.assign_materials")
		sc2.enabled = False

		#r0 = layout.col()
		r0 = layout.row()
		r0.alignment = 'CENTER'
		r0.scale_y = 1.2
		r0.operator("mesh.fifa_import")

		col = layout.column()
		r3 = col.row()
		r3.alignment ='CENTER'
		r3.scale_y = 1.2
		r3.operator(
			"system.visit_github_url", text='Visit Github Wiki')
		r3.operator(
			"system.visit_thread_url", text='Visit Official Thread')

		r1 = col.row()
		r1.alignment = 'CENTER'
		r1.label(text=credit1)
		r2 = col.row()
		r2.alignment = 'CENTER'
		r2.label(text=credit2)
		r3 = col.row()
		r3.alignment = 'CENTER'
		r3.label(text=credit3)


class FIFA_PT_FifaExporter(bpy.types.Panel):
	"""Create category in N-Menu"""
	bl_category = "FIFA 3D I/E"

	bl_label = 'FIFA' + game_version + '3D Exporter'
	bl_idname = 'FIFA_PT_FifaExporter'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	#bl_context = 'scene'

	def draw(self, context):
		scn = context.scene
		layout = self.layout

		#Enable if any export option selected
		if (scn.stadium_export_flag or scn.trophy_export_flag or scn.face_edit_flag or scn.gen_overwriter_flag):
			isExportActive = True
		else:
			isExportActive = False
		
		#region Info Panel

		# Information Panel
		row1 = layout.row(align=True)
		row1.label(icon='INFO', text='Export Information Panel')
		box = layout.box()
		col = box.column()
		row = col.row()
		if isExportActive != True:
			row.label(text='[INFO] All good here. Ready to export.')
		row.alignment = 'EXPAND'

		conflictFound = False

		# Error Prompts
		if (scn.stadium_export_flag and scn.trophy_export_flag) and not (scn.face_edit_flag or scn.gen_overwriter_flag):
			row.label(text='[ERROR] Model Export conflict found.')
			row = col.row()
			row.label(text='[ERROR] Check your export flags.')
			row = col.row()
			conflictFound = True
		
		elif (scn.face_edit_flag and scn.gen_overwriter_flag) and not (scn.stadium_export_flag or scn.trophy_export_flag):
			row.label(text='[ERROR] File Overwriter conflict found.')
			row = col.row()
			row.label(text='[ERROR] Check your export flags.')
			row = col.row()
			conflictFound = True

		elif (scn.stadium_export_flag or scn.trophy_export_flag) and (scn.face_edit_flag or scn.gen_overwriter_flag):
			row.label(
				text='[ERROR] Exporting and Overwriting both enabled.')
			row = col.row()
			row.label(text='[ERROR] Check your export flags.')
			row = col.row()
			conflictFound = True

		# Valid Notifications
		if scn.stadium_export_flag and not(scn.trophy_export_flag or scn.gen_overwriter_flag or scn.face_edit_flag):
			row.label(text='[INFO] Stadium Export enabled.')
			row = col.row()

		if scn.trophy_export_flag and not (scn.stadium_export_flag or scn.gen_overwriter_flag or scn.face_edit_flag):
			row.label(text='[INFO] Trophy/Ball Export enabled.')
			row = col.row()

		if scn.face_edit_flag and not (scn.stadium_export_flag or scn.gen_overwriter_flag or scn.trophy_export_flag):
			row.label(text='[INFO] Face Editing Mode enabled.')
			row = col.row()

		if scn.gen_overwriter_flag and not (scn.face_edit_flag or scn.stadium_export_flag or scn.trophy_export_flag):
			row.label(text='[INFO] General Overwriting Mode enabled.')
			row = col.row()

		#endregion

		# New Exporter
		row = layout.row(align=True)
		row.label(icon='INFO', text="File Exporter")
		box = layout.box()
		col = box.column()
		row = col.row()
		row.alignment = 'RIGHT'
		row.label(text='  Game Version')
		row.prop(scn, 'game_enum', text='')

		row = col.row()
		row.scale_y = 1.2
		row.alignment = 'EXPAND'
		row.prop(scn, 'stadium_export_flag')
		row.prop(scn, 'trophy_export_flag')

		row = col.row()
		row.prop(scn, 'export_path')

		if scn.stadium_export_flag:

			box = col.box()
			box.label(text='Stadium Properties', icon='INFO')
			row = box.row()
			split = row.split()
			split.scale_x = 1.5
			split.prop(scn, 'stadium_version', text='Time')
			split = row.split()
			split.scale_x = 1.5
			split.prop(scn, 'stadium_time', text='Weather')
			split = row.split()
			split.alignment = 'RIGHT'
			split.scale_x = 1.5
			split.label(text='File Id')
			split.prop(scn, 'file_id', text='')
		elif scn.trophy_export_flag:
			box = col.box()
			box.label(text='Trophy/Ball Properties', icon='INFO')
			row = box.row()
			row.label(text='File Id')
			row.prop(scn, 'file_id', text='')

		row = col.row()
		row.scale_y = 1.2

		if scn.trophy_export_flag:
			txt = "TROPHY / BALL EXPORT"
		else:
			txt = "STADIUM EXPORT"
		
		row.operator("mesh.fifa_export", text=txt)
		row.operator('mesh.texture_export')
		row.operator('mesh.crowd_export')
		row.operator('mesh.lights_export')

		# if scn.stadium_export_flag and scn.trophy_export_flag:
		# 	row.enabled = False
		# elif (scn.stadium_export_flag or scn.trophy_export_flag) and (scn.face_edit_flag or scn.gen_overwriter_flag):
		# 	row.enabled = False

		if conflictFound:
			row.enabled = False

		# Basic Exporter Overwriter
		row = layout.row(align=True)

		row.label(icon='INFO', text='File Overwriter')
		box = layout.box()
		col = box.column()

		row = col.row()
		row.scale_y = 1.2
		row.prop(scn, 'gen_overwriter_flag')
		row.prop(scn, 'face_edit_flag')
		if scn.face_edit_flag:
			box = col.box()
			box.label(text='Face Editing Options', icon='INFO')
			col1 = box.column()
			row = col1.row()
			row.alignment = 'EXPAND'
			row.prop(scn, 'face_edit_head_flag')
			row.prop(scn, 'face_edit_hair_flag')
		elif scn.gen_overwriter_flag:
			box = col.box()
			box.label(text='General Overwriting Options', icon='INFO')
			col1 = box.column()
			row = col1.row()
			row.alignment = 'EXPAND'
			row.prop(scn, 'trophy_flag')

		row = col.row()
		row.prop(scn, 'export_path')

		# Export row
		row = col.row()
		row.operator('mesh.texture_export')
		if scn.face_edit_flag:
			txt = "FACE MODEL EXPORT"
		else:
			txt = "OVERWRITE"
		row.operator("mesh.fifa_overwrite", text=txt)
		
		# if scn.face_edit_flag and scn.gen_overwriter_flag:
		# 	row.enabled = False
		# elif (scn.stadium_export_flag or scn.trophy_export_flag) and (scn.face_edit_flag or scn.gen_overwriter_flag):
		# 	row.enabled = False

		if conflictFound:
			row.enabled = False

		col = layout.column()
		r3 = col.row()
		r3.alignment ='CENTER'
		r3.scale_y = 1.2
		r3.operator(
			"system.visit_github_url", text='Visit Github Wiki')
		r3.operator(
			"system.visit_thread_url", text='Visit Official Thread')

		r1 = col.row()
		r1.alignment = 'CENTER'
		r1.label(text=credit1)
		r2 = col.row()
		r2.alignment = 'CENTER'
		r2.label(text=credit2)
		r3 = col.row()
		r3.alignment = 'CENTER'
		r3.label(text=credit3)


class FIFA_PT_FifaStadium_Tools(bpy.types.Panel):
	"""Create category in N-Menu"""
	bl_category = "FIFA 3D I/E"

	bl_label = 'FIFA' + game_version + 'Stadium Tools'
	bl_idname = 'FIFA_PT_FifaStadium_Tools'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	#bl_context = 'scene'

	def draw(self, context):
		scn = context.scene
		layout = self.layout
		row = layout.row()
		row.label(icon='INFO', text='Stadium Tools')
		bigbox = layout.box()
		col = bigbox.column()
		row = col.row()
		row.scale_y = 1.2
		row.prop(scn, 'prop_enum')
		split = row.split()
		split.scale_x = 0.3
		split.operator("system.add_prop")
		row = col.row()
		row.scale_y = 1.2
		row.operator("system.add_stad_groups")
		row = col.row()
		split = row.split()
		col = split.column()

		row = layout.row()
		row.label(icon='INFO', text='Crowd Seat Creator')

		row = layout.row()

		row.scale_y = 1.2
		row.operator('mesh.crowd_create_seats')

		col = layout.column()
		r3 = col.row()
		r3.alignment ='CENTER'
		r3.scale_y = 1.2
		r3.operator(
			"system.visit_github_url", text='Visit Github Wiki')
		r3.operator(
			"system.visit_thread_url", text='Visit Official Thread')

		r1 = col.row()
		r1.alignment = 'CENTER'
		r1.label(text=credit1)
		r2 = col.row()
		r2.alignment = 'CENTER'
		r2.label(text=credit2)
		r3 = col.row()
		r3.alignment = 'CENTER'
		r3.label(text=credit3)


class FIFA_PT_FifaHelping_Tools(bpy.types.Panel):
	"""Create category in N-Menu"""
	bl_category = "FIFA 3D I/E"

	bl_label = 'FIFA' + game_version + 'Helping Tools'
	bl_idname = 'FIFA_PT_FifaHelping_Tools'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	#bl_context = 'scene'

	def draw(self, context):
		scn = context.scene
		layout = self.layout

		# row.scale_y=1.5
		col = layout.column()
		row = col.row()
		row.scale_y = 1.4
		row.operator("system.fix_relative_paths")
		row.operator('system.clean_temp_dir')
		row = col.row()
		row.scale_y = 1.4
		row.operator('mesh.remove_meshes')
		row = col.row()
		row.scale_y = 1.4
		row.operator("mesh.clean_paths")
		row.operator("mesh.hide_props")

		col = layout.column()
		r3 = col.row()
		r3.alignment ='CENTER'
		r3.scale_y = 1.2
		r3.operator(
			"system.visit_github_url", text='Visit Github Wiki')
		r3.operator(
			"system.visit_thread_url", text='Visit Official Thread')

		r1 = col.row()
		r1.alignment = 'CENTER'
		r1.label(text=credit1)
		r2 = col.row()
		r2.alignment = 'CENTER'
		r2.label(text=credit2)
		r3 = col.row()
		r3.alignment = 'CENTER'
		r3.label(text=credit3)


if dev_status:
	class FIFA_PT_DeveloperPanel(bpy.types.Panel):
		"""Create category in N-Menu"""
		bl_category = "FIFA 3D I/E"

		"""Creates a Panel in Scene properties window"""
		bl_label = "FIFA" + game_version + "Developer Panel"
		bl_idname = "FIFA_PT_DeveloperPanel"
		bl_space_type = 'VIEW_3D'
		bl_region_type = 'UI'
		#bl_context = "scene"

		def draw(self, context):
			scn = context.scene

			layout = self.layout
			box = layout.box()
			box.label(icon='INFO', text='Bath Importer')
			row = box.row()
			row.prop(scn, 'batch_import_path')
			row = box.row()
			row.prop(scn, 'batch_radius')
			row = box.row()
			row.operator("mesh.batch_import", text="BATCH IMPORT")
			box = layout.box()
			box.label(icon='INFO', text='Rx3 Unlocker')
			row = box.row()
			row.operator("system.rx3_unlock", text="UNLOCK")

			col = layout.column()
			r3 = col.row()
			r3.alignment ='CENTER'
			r3.scale_y = 1.2
			r3.operator(
				"system.visit_github_url", text='Visit Github Wiki')
			r3.operator(
				"system.visit_thread_url", text='Visit Official Thread')

			r1 = col.row()
			r1.alignment = 'CENTER'
			r1.label(text=credit1)
			r2 = col.row()
			r2.alignment = 'CENTER'
			r2.label(text=credit2)
			r3 = col.row()
			r3.alignment = 'CENTER'
			r3.label(text=credit3)


###SCENE CUSTOM PROPERTIES###
# IMPORT PROPERTIES
###PATHS###
# Model Paths
bpy.types.Scene.model_import_path = bpy.props.StringProperty(
	name="3D Model File",
	description='Select .rx3 model file for importing',
	subtype='FILE_PATH',
)
bpy.types.Scene.hair_import_path = bpy.props.StringProperty(
	name="Hair File",
	description='Select additional .rx3 model file',
	subtype='FILE_PATH'
)
bpy.types.Scene.crwd_import_path = bpy.props.StringProperty(
	name="Crowd File",
	description='Select additional .rx3 stadium crowd file',
	subtype='FILE_PATH'
)
bpy.types.Scene.lnx_import_path = bpy.props.StringProperty(
	name="Lights File",
	description='Select additional lnx stadium light file',
	subtype='FILE_PATH'
)
bpy.types.Scene.obj_path = bpy.props.StringProperty(
	name="FaceGen .obj File",
	description='Select .obj facegen model for importing',
	subtype='FILE_PATH',
)
# Texture Paths
bpy.types.Scene.stadium_texture_import_path = bpy.props.StringProperty(
	name="Stadium Texture File",
	description='Select .rx3 texture file for importing',
	subtype='FILE_PATH',
)
bpy.types.Scene.hair_texture_import_path = bpy.props.StringProperty(
	name="Hair Texture File",
	description='Select .rx3 texture file for importing',
	subtype='FILE_PATH',
)
bpy.types.Scene.face_texture_import_path = bpy.props.StringProperty(
	name="Face Texture File",
	description='Select .rx3 texture file for importing',
	subtype='FILE_PATH',
)
bpy.types.Scene.eyes_texture_import_path = bpy.props.StringProperty(
	name="Eye Texture File",
	description='Select .rx3 texture file for importing',
	subtype='FILE_PATH'
)


###FLAGS###
# IMPORT FLAGS
bpy.types.Scene.geometry_flag = bpy.props.BoolProperty(
	name="Import Geometry",
	description='Select wether to Import Geometry or not',
	default=False
)

##MISC PROPS##
bpy.types.Scene.vx_color = bpy.props.FloatVectorProperty(
	name='Vertex Color',
	subtype='COLOR',
	default=(1.0, 1.0, 1.0),
	max=1.0,
	min=0
)

bpy.types.Scene.vx_color_hex = bpy.props.StringProperty(
	name='Hex Repr',
)

bpy.types.Scene.prop_enum = bpy.props.EnumProperty(
	items=[('rooffireworks', 'Roof Fireworks', 'Rooffireworks'),
		   ('Confetti Cannon', 'Confetti Cannon', 'Confetti Cannon'),
		   ('chair_folding_blue_cushion',
			'Folding Blue Chair', 'Folding Blue Chair'),
		   ('slc_ballboy', 'Ballboy', 'Ballboy'),
		   ('slc_benchplayeraway', 'Away Bench Player', 'Away Bench Player'),
		   ('slc_benchplayerhome', 'Home Bench Player', 'Home Bench Player'),
		   ('slc_camera_sitting', 'Camera Sitting', 'Camera Sitting'),
		   ('slc_camera_standing', 'Camera Standing', 'Camera Standing'),
		   ('slc_camera_handheld', 'Camera Handheld', 'Camera Handheld'),
		   ('slc_generic', 'Generic', 'Generic'),
		   ('slc_manageraway', 'Away Manager', 'Away Manager'),
		   ('slc_managerhome', 'Home Manager', 'Home Manager'),
		   ('slc_medicalofficer', 'Medical Officer', 'Medical Officer'),
		   ('slc_photographer', 'Photographer', 'Photographer'),
		   ('slc_police', 'Police', 'Police'),
		   ('slc_steward', 'Steward', 'Steward'),
		   ('slc_assistantmanageraway',
			'Assistant Manager Away', 'Assistant Manager Away'),
		   ('slc_assistantmanagerhome',
			'Assistant Manager Home', 'Assistant Manager Home'),
		   ('slc_tournamentofficial', 'Tournament Prop', 'Tournament Prop')
		   ],
	name="Available Props")

# Crowd Panel properties
bpy.types.Scene.crowd_align_enum = bpy.props.EnumProperty(
	items=[('0', 'Cursor Location', 'Cursor Location'),
		   ('1', 'X', 'X'),
		   ('2', 'Y', 'Y'),
		   ('3', '-X', '-X'),
		   ('4', '-Y', '-Y')
		   ],
	name="Seat Alignment")


# Autopaint Modes
bpy.types.Scene.autopaint_modes = bpy.props.EnumProperty(
	items=[('0', 'Mode 1', 'Stadium Mode'),
		   ('1', 'Mode 2', '2nd Mode'),
		   ('2', 'Tangents/Bitangents', '2nd Mode')],
	name="AutoPaint Modes")


bpy.types.Scene.crowd_type_enum = bpy.props.EnumProperty(
	items=[('hardcoreHome_', 'hardcoreHome', 'hardcoreHome'),
		   ('metalcoreHome_', 'metalcoreHome', 'metalcoreHome'),
		   ('heavyHome_', 'heavyHome', 'heavyHome'),
		   ('popHome_', 'popHome', 'popHome'),
		   ('folkHome_', 'folkHome', 'folkHome'),
		   ('chickenAway_', 'chickenAway', 'chickenAway'),
		   ('deadAway_', 'deadAway', 'deadAway')],
	name='Crowd Type')

bpy.types.Scene.crowd_fullness_enum = bpy.props.EnumProperty(
	items=[('full_1', 'Full', 'Full'),
		   ('almostFull_1', 'Almost Full', 'Almost Full'),
		   ('halfFull_1', 'Half Full', 'Half Full'),
		   ('almostEmpty_1', 'Almost Empty', 'Almost Empty'),
		   ('empty_1', 'Empty', 'Empty')],
	name='Crowd Fullness')

bpy.types.Scene.game_enum = bpy.props.EnumProperty(
	items=[('0', 'FIFA 13', 'FIFA 13'),
		   ('1', 'FIFA 14', 'FIFA 14'),
		   ('2', 'FIFA 15', 'FIFA 15')],
	default='2',
	name="Game Version")

bpy.types.Scene.bones_flag = bpy.props.BoolProperty(
	name="Import Bones",
	description='View Bones, WIP',
	default=False
)
bpy.types.Scene.bone_groups_flag = bpy.props.BoolProperty(
	name="Import Bone Groups",
	description='Creates Vertex Groups for each bone vertex',
	default=False
)
bpy.types.Scene.props_flag = bpy.props.BoolProperty(
	name="Import Props",
	description='Import Props [STADIUM ONLY]',
	default=False
)
bpy.types.Scene.collision_flag = bpy.props.BoolProperty(
	name="Import Collision",
	description='Turn on if you want to import Collision Geometry [STADIUM ONLY]',
	default=False
)
bpy.types.Scene.materials_flag = bpy.props.BoolProperty(
	name="Import Materials",
	description='Leave off if you do not have any proper stadium texture container selected. Turn it On otherwise.[STADIUM ONLY]',
	default=False
)

bpy.types.Scene.create_materials_flag = bpy.props.BoolProperty(
	name="Create Materials from Texture Files",
	description='Turn On if you want to create materials from textures',
	default=False
)
bpy.types.Scene.trophy_flag = bpy.props.BoolProperty(
	name="Indices Method",
	description='If the vertices show up correctly but the faces are screwed, check/uncheck that and reimport. When using the overwriter, leave it as it would be when the model was imported correctly.',
	default=False
)
# EXPORT PROPERTIES
bpy.types.Scene.stadium_export_flag = bpy.props.BoolProperty(
	name="Stadium",
	default=False
)


bpy.types.Scene.file_id = bpy.props.IntProperty(
	name='Id',
	default=0,
	min=0,
	max=500
)
bpy.types.Scene.stadium_version = bpy.props.EnumProperty(
	items=[('1', 'Day', 'Day'),
		   ('3', 'Night', 'Night')],
	name="Stadium Version")

bpy.types.Scene.stadium_time = bpy.props.EnumProperty(
	items=[('0', 'Fine Weather', 'Fine Weather'),
		   ('1', 'Overcast', 'Overcast'),
		   ('2', 'Rainy Weather', 'Rainy Weather'),
		   ('3', 'Snow', 'Snow')],
	name="Stadium Time")

bpy.types.Scene.trophy_export_flag = bpy.props.BoolProperty(
	name="Trophy/Ball",
	default=False
)


# OVERWRITE PROPERTIES
bpy.types.Scene.gen_overwriter_flag = bpy.props.BoolProperty(
	name="General Overwriting Mode",
	default=False
)
bpy.types.Scene.face_edit_flag = bpy.props.BoolProperty(
	name="Face Editing Mode",
	default=False
)
bpy.types.Scene.face_edit_head_flag = bpy.props.BoolProperty(
	name="Head Model",
	default=False
)
bpy.types.Scene.face_edit_hair_flag = bpy.props.BoolProperty(
	name="Hair Model",
	default=False
)

bpy.types.Scene.export_path = bpy.props.StringProperty(
	name="Export Directory",
	subtype='DIR_PATH'
)

bpy.types.Scene.fifa_import_loc = bpy.props.FloatVectorProperty(
	name='Import Location',
	default=(0.0, 0.0, 0.0)
)

# development mode props
bpy.types.Scene.batch_import_path = bpy.props.StringProperty(
	name="Batch Import Path",
	subtype='DIR_PATH'
)

bpy.types.Scene.batch_radius = bpy.props.IntProperty(
	name='Radius',
	default=0,
	min=0,
	max=100
)


# LIGHT PROPERTIES
class emitbox_propertygroup(bpy.types.PropertyGroup):
	fAngularVelocityAdoption = FloatProperty(
		name='fAngularVelocityAdoption', min=0, max=100, precision=1)
	fSizeMean = FloatProperty(name='fSizeMean', min=0, max=5000, precision=1)
	fSizeSpread = FloatProperty(
		name='fSizeSpread', min=0, max=1000, precision=1)
	fVelocityAdoption = FloatProperty(
		name='fVelocityAdoption', min=0, max=100, precision=1)
	iEmitRate = IntProperty(name='fSizeSpread', min=0, max=10000, step=1)
	vVelocitySpread = FloatVectorProperty(
		name='vVelocitySpread', default=(0.3, 0.3, 0.3), size=3, max=1.0, min=0, precision=2)
	bInject = BoolProperty(name='bInject', default=True)


class actionrender_propertygroup(bpy.types.PropertyGroup):
	sShader = EnumProperty(name='sShader',
						   items=[('lynxGlare.fx', 'lynxGlare.fx', 'lynxGlare.fx'),
								  ('lynxVbeam.fx', 'lynxVbeam.fx', 'lynxVbeam.fx'),
								  ('lynx.fx', 'lynx.fx', 'lynx.fx')
								  ]
						   )
	sTexture = EnumProperty(name='sTexture',
							items=[('fx_glare_corona.dds', 'glare_corona', 'fx_glare_corona.dds'),
								   ('fx_glare_lensflare.dds', 'glare_lensflare', 'fx_glare_lensflare.dds'),
								   ('fx_glare_lensfold.dds', 'glare_lensfold', 'fx_glare_lensfold.dds'),
								   ('fx_glare_halogen.dds', 'glare_halogen', 'fx_glare_halogen.dds'),
								   ('fx_vbeam_noisebeam.dds', 'vbeam_noisebeam', 'fx_vbeam_noisebeam.dds'),
								   ('fx_glare_whitefalloff.dds', 'glare_whitefalloff', 'fx_glare_whitefalloff.dds')
								   ],

							)
	sTechnique = EnumProperty(name='sTechnique',
							  items=[('AdditiveBlend', 'AdditiveBlend', 'AdditiveBlend'),
									 ('AlphaBlend', 'AlphaBlend', 'AlphaBlend')
									 ]
							  )

	iType = IntProperty(name='iType', min=0, max=5, step=1, default=0)
	fTimeSpeed = FloatProperty(
		name='fTimeSpeed', min=0, max=0.5, step=0.001, default=0.001)
	iDepthBuffer = IntProperty(
		name='iDepthBuffer', min=0, max=5, step=1, default=1)
	iAlign = IntProperty(name='iAlign', min=0, max=5, step=1, default=0)
	iNoFadeFar = IntProperty(
		name='iNoFadeFar', min=0, max=5, step=1, default=0)
	iScreenSpace = IntProperty(
		name='iScreenSpace', min=0, max=5, step=1, default=0)
	fFadeDistance = FloatProperty(
		name='fFadeDistance', min=0, max=1, precision=2, step=0.01, default=0)
	fZBias = FloatProperty(
		name='fZBias', min=0, max=1, precision=2, step=0.01, default=0)

	fGlareSensitivityCenter = FloatProperty(
		name='fGlareSensitivityCenter', min=0, max=5, precision=2, step=0.01)
	fGlareSensitivityEdge = FloatProperty(
		name='fGlareSensitivityEdge', min=0, max=5, precision=2, step=0.01)
	fGlareSensitivityPower = FloatProperty(
		name='fGlareSensitivityPower', min=0, max=100, precision=2, step=0.01)
	fGlareBloomScale = FloatProperty(
		name='fGlareBloomScale', min=0, max=30, precision=2, step=0.01)
	fGlareBloomSpread = FloatProperty(
		name='fGlareBloomSpread', min=0, max=30, precision=2, step=0.01)
	fGlareBloomRate = FloatProperty(
		name='fGlareBloomRate', min=-1, max=1, precision=2, step=0.01)
	fGlareRotationRate = FloatProperty(
		name='fGlareRotationRate', min=-1, max=1, precision=2, step=0.01)
	fGlareSizeMultSpread = FloatProperty(
		name='fGlareSizeMultSpread', min=0, max=1, precision=2, step=0.1)

	fFlareMovementRate = FloatProperty(
		name='fFlareMovementRate', min=0, max=1, precision=4, step=0.0001)
	fFlareOffsetScale = FloatProperty(
		name='fFlareOffsetScale', min=0, max=1, precision=2, step=0.01)
	fFlareEndScale = FloatProperty(
		name='fFlareEndScale', min=0, max=30, precision=2, step=0.01)

	fVbeamAngle = FloatProperty(
		name='fVbeamAngle', min=0, max=360, precision=2, step=0.01)
	fVbeamAngleSpread = FloatProperty(
		name='fVbeamAngleSpread', min=0, max=20, precision=2, step=0.01)
	fVbeamLength = FloatProperty(
		name='fVbeamLength', min=0, max=10000, precision=2, step=1)
	fVbeamLengthSpread = FloatProperty(
		name='fVbeamLengthSpread', min=0, max=10000, precision=2, step=1)

	bUseColorRamp = BoolProperty(name='bUseColorRamp', default=False)
	vColorRamp = FloatVectorProperty(name='vColorRamp', default=(
		1, 1, 1, 1), size=4, max=5, min=0, precision=1, step=0.1)
	vColorRampTimes = FloatVectorProperty(name='vColorRampTimes', default=(
		0, 0, 0, 1), size=4, max=5, min=0, precision=1, step=0.1)
	iColorRampMode = IntProperty(name='iColorRampMode', min=0, max=1, step=1, default=0)

	bUseSizeRamp = BoolProperty(name='bUseSizeRamp', default=False)
	vSizeRamp = FloatVectorProperty(name='vSizeRamp', default=(
		1, 1, 1, 1), size=4, max=5, min=0, precision=1, step=0.1)
	vSizeRampTimes = FloatVectorProperty(name='vSizeRampTimes', default=(
		0, 0, 0, 1), size=4, max=5, min=0, precision=1, step=0.1)

	bUseSizeMult = BoolProperty(name='bUseSizeMult', default=False)
	fSizeMultX = FloatProperty(
		name='fSizeMultX', min=0, max=10, precision=2, step=0.01, default=4)
	fSizeMultY = FloatProperty(
		name='fSizeMultY', min=0, max=10, precision=2, step=0.01, default=4)

	bUseAnimTexture = BoolProperty(name='bUseAnimTexture', default=False)
	bUseLighting = BoolProperty(name='bUseLighting', default=False)
	bHalfSizeRender = BoolProperty(name='bHalfSizeRender', default=True)

	bStretchPerParticle = BoolProperty(
		name='bStretchPerParticle', default=False)

	bUseColorMult = BoolProperty(name='bUseColorMult', default=True)
	vColorMult = FloatVectorProperty(name='vColorMult', default=(
		1, 1, 1, 1), size=4, max=5, min=0, precision=2, step=0.01)
	vColorMultSpread = FloatVectorProperty(name='vColorMultSpread', default=(
		1, 1, 1, 1), size=4, max=5, min=0, precision=2, step=0.01)

	bUseGlareSeed = BoolProperty(name='bUseGlareSeed', default=True)

	bUseZFeather = BoolProperty(name='bUseZFeather', default=True)
	fZFeatherRange = FloatProperty(
		name='fZFeatherRange', min=0, max=50000, precision=1, step=0.1, default=10000)
	fNearFeatherRange = FloatProperty(
		name='fNearFeatherRange', min=0, max=10000, precision=1, step=0.1, default=0)
	fFarFeatherRange = FloatProperty(
		name='fFarFeatherRange', min=0, max=50000, precision=1, step=0.1, default=50000)
	fZFeatherOffset = FloatProperty(
		name='fZFeatherOffset', min=0, max=1, precision=2, step=0.01, default=1)
	fZFeatherFalloff = FloatProperty(
		name='fZFeatherFalloff', min=0, max=1, precision=2, step=0.01, default=1)

	vPivotShift = FloatVectorProperty(
		name='vPivotShift', default=(0, 0, 0), size=3, max=5, min=0, precision=2)


def make_annotations(cls):
	"""Converts class fields to annotations if running with Blender 2.8"""
	if bpy.app.version < (2, 80):
		return cls
	bl_props = {k: v for k, v in cls.__dict__.items() if isinstance(v, tuple)}
	if bl_props:
		if '__annotations__' not in cls.__dict__:
			setattr(cls, '__annotations__', {})
		annotations = cls.__dict__['__annotations__']
		for k, v in bl_props.items():
			annotations[k] = v
			delattr(cls, k)
	return cls

classes = [
	FIFA_PT_CrowdSection,
	FIFA_PT_Vertex_color_panel,
	FIFA_PT_lights_panel,
	FIFA_PT_FifaImporter,
	FIFA_PT_FifaExporter,
	FIFA_PT_FifaStadium_Tools,
	FIFA_PT_FifaHelping_Tools,
	#FIFA_PT_DeveloperPanel
	]

def register():
	fifa3D_operators.register()
	for cls in classes:
		make_annotations(cls) # what is this? Read the section on annotations above!
		bpy.utils.register_class(cls)


def unregister():  # note how unregistering is done in reverse
	fifa3D_operators.unregister()
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

make_annotations(emitbox_propertygroup) 
bpy.utils.register_class(emitbox_propertygroup)
make_annotations(actionrender_propertygroup) 
bpy.utils.register_class(actionrender_propertygroup)

# LIGHT PROPERTIES
bpy.types.Object.emitbox_props = bpy.props.PointerProperty(
	type=emitbox_propertygroup)
bpy.types.Object.actionrender_props = bpy.props.PointerProperty(
	type=actionrender_propertygroup)

if __name__ == "__main__":
	register()