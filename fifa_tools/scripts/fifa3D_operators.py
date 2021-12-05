# Filename : fifa3D_operators.py
# Usage : All operators that are registered in blender
# Author : Death GOD 7
# Decompiled by Death GOD 7 from original fifa15_operators.pyc

import bpy, os, webbrowser, imp, math, sys, struct
from bpy.types import NodeOutputFileSlotLayer, Operator
from builtins import dir as class_dir
from mathutils import Vector, Euler, Matrix
from math import radians
from shutil import copyfile
from xml.dom import minidom
from time import gmtime, strftime

linux_path = '/media/2tb/Blender/blender-2.71-windows64'
if os.name == 'nt':
	prePath = ''
else:
	prePath = linux_path + os.sep
# fifa_main_path = 'fifa_tools' + os.sep + 'scripts' + os.sep + 'fifa3D_main.py'
# fifa_main = imp.load_source(
# 	'fifa_main', prePath + fifa_main_path)
#fifa_main = imp.load_compiled('fifa_main', 'fifa_tools' + os.sep + 'scripts' + os.sep + 'fifa3D_main.pyc')
# fifa_func_path = 'fifa_tools' + os.sep + 'scripts' + os.sep + 'fifa3D_functions.py'
# fifa_func = imp.load_source(
# 	'fifa_func', prePath + fifa_func_path)
#fifa_func = imp.load_compiled('fifa_func', 'fifa_tools' + os.sep + 'scripts' + os.sep + 'fifa3D_functions.pyc')

# from fifa_func import general_helper as gh
# from fifa_func import texture_helper as tex_gh
# from fifa_main import sig, crowdGroup

import fifa_tools
from fifa_tools.scripts import fifa3D_se7en , fifa3D_helper
import fifa_tools.scripts.fifa3D_functions as fifa_func
from fifa_tools.scripts.fifa3D_functions import general_helper as gh
from fifa_tools.scripts.fifa3D_functions import texture_helper as tex_gh
import fifa_tools.scripts.fifa3D_main as fifa_main
from fifa_tools.scripts.fifa3D_main import sig, crowdGroup
from fifa_tools.scripts.fifa3D_logger import *

f = 0
e = 0
ddsheader = '10'
materials = []
tex_names = []
objectcount = 0
files = []
#dir = fifa_tools.texdir + '\\'
#dir = os.path.realpath(dir)

texture_slotType_dict = {
	0: 'diffuseTexture', 
	1: 'ambientTexture', 
	2: 'coeffMap', 
	3: 'normalMap', 
	4: 'cubicEnvMap', 
	5: 'incandescenceMap', 
	6: 'alphamask', 
	7: 'noiseTexture', 
	8: 'pitchLinesMap', 
	9: 'diffuseTexture'}

light_props = [
 [
  'sShader', ['fGlareSensitivityCenter', 'fGlareSensitivityEdge', 'fGlareSensitivityPower', 'fGlareSizeMultSpread', 'fGlareBloomScale', 'fGlareBloomSpread', 'fGlareBloomRate', 'fGlareRotationRate', 'fFlareMovementRate', 'fFlareOffsetScale', 'fFlareEndScale'], ['fVbeamAngle', 'fVbeamAngleSpread', 'fVbeamLength', 'fVbeamLengthSpread']],
 'sTexture',
 'sTechnique',
 [
  'bUseColorRamp', ['vColorRamp', 'vColorRampTimes']],
 [
  'bUseSizeRamp', ['vSizeRamp', 'vSizeRampTimes']],
 [
  'bUseSizeMult', ['fSizeMultX', 'fSizeMultY']],
 [
  'bUseColorMult', ['vColorMult', 'vColorMultSpread', 'iColorRampMode']],
 [
  'bUseZFeather', ['fZFeatherRange', 'fNearFeatherRange', 'fFarFeatherRange', 'fZFeatherFalloff', 'fZFeatherOffset']],
 'bStretchPerParticle',
 'bUseAnimTexture',
 'bUseLighting',
 'bHalfSizeRender',
 'bUseGlareSeed',
 'vPivotShift',
 'fAngularVelocityAdoption',
 'fSizeMean',
 'fSizeSpread',
 'iEmitRate',
 'bInject',
 'vVelocitySpread',
 'fVelocityAdoption',
 'iType',
 'iDepthBuffer',
 'iAlign',
 'iNoFadeFar',
 'iScreenSpace',
 'fFadeDistance',
 'fZBias',
 'fTimeSpeed']
group_names = [
 'Pitch',
 'MainStadium',
 'Alpha3_NoShadowCast',
 'Alpha3',
 'Alpha2',
 'Roof',
 'Alpha',
 'MainStadium_NoShadowCast',
 'AdBoard',
 'AdBoard_NoShadowCast',
 'EnvironmentSkirt',
 'Banner_NoShadowCast',
 'Jumbotron',
 'SidelineProps',
 'TournamentDressing_NoShadowCast',
 'StadiumWear_NoShadowCast',
 'Sky',
 'Weather_NoShadowCast']
group_names_15 = group_names + [
 'CrowdNet',
 'Default',
 'Pitch_NoShadowCast',
 'TournamentDressing',
 'Exterior',
 'Exterior_NoShadowCast',
 'Exterior_ShadowAlpha',
 'Roof_NoShadowCast',
 'Roof_ShadowAlpha']
standard_materials = [
 'adboard', 'adboarddigital', 'adboarddigitalglow', 'adboarddigitalwide', 'adboardgeneric', 'adboardscrolling', 'adboardsingledigital', 'adboardsingledigitalglow', 'banneraway',
 'bannergroup', 'bannerhome', 'concrete', 'concreteshadow', 'crest', 'diffusealpha', 'diffuseopaque', 'diffusesimple', 'diffusewet', 'envmetal', 'genericad', 'glass',
 'homeprimary', 'homesecondary', 'initialshadinggroup', 'jumbotron', 'metalbare', 'metalpainted', 'pitch', 'pitchnoline', 'rubbershadow', 'sclockhalves', 'sclockminutesones',
 'sclockminutestens', 'sclockscoreawayones', 'sclockscoreawaytens', 'sclockscorehomeones', 'sclockscorehometens', 'sclocksecondsones', 'sclocksecondstens', 'sclocktimeanalog',
 'simpleglow', 'sky', 'snowpile', 'tournament']
for i in range(100):
	standard_materials.append('adboarddigitalwide' + str(i))

for i in range(100):
	standard_materials.append('adboardsingledigitalglow' + str(i))

for i in range(100):
	standard_materials.append('bannergroup' + str(i))

class align_crowd_faces(bpy.types.Operator):
	bl_idname = 'mesh.align_crowd_seats'
	bl_label = 'Set'
	bl_description = 'Click to align crowd seats'

	def invoke(self, context, event):
		scn = bpy.context.scene
		vec_dict = {0: Vector((scn.cursor_location.x, scn.cursor_location.y)),  1: Vector((1, 0)), 
		 2: Vector((0, 1)), 
		 3: Vector((-1, 0)), 
		 4: Vector((0, -1))}
		align_vector = vec_dict[int(scn.crowd_align_enum)]
		fifa_main.crowd_seat_align(align_vector)
		return {
		 'FINISHED'}


class crowd_create_seats(bpy.types.Operator):
	bl_idname = 'mesh.crowd_create_seats'
	bl_label = 'Create Seats'
	bl_description = 'Click to create Crowd Seats'
	bl_options = {'REGISTER', 'UNDO'}
	crowd_vertical_distance = bpy.props.FloatProperty(name='Vertical Distance', min=2, max=10)
	crowd_horizontal_distance = bpy.props.FloatProperty(name='Horizontal Distance', min=2, max=10)
	crowd_gap_distance = bpy.props.FloatProperty(name='Gap Distance', min=2, max=10)
	crowd_horizontal_seats = bpy.props.IntProperty(name='Seat Number Horizontally', min=2, max=1000)
	crowd_vertical_seats = bpy.props.IntProperty(name='Seat Number Vertically', min=1, max=50)

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		fifa_main.crowd_seat_create(self.crowd_vertical_seats, self.crowd_horizontal_seats, self.crowd_vertical_distance, self.crowd_horizontal_distance, self.crowd_gap_distance, context)
		return {
		 'FINISHED'}


class assign_crowd_type(bpy.types.Operator):
	bl_idname = 'mesh.assign_crowd_type'
	bl_label = ''
	bl_description = 'Click to assign selected vertices to the selected crowd type'

	def invoke(self, context, event):
		scn = bpy.context.scene
		fifa_main.crowd_groups(scn.crowd_type_enum + scn.crowd_fullness_enum)
		return {
		 'FINISHED'}


class colour_assign(bpy.types.Operator):
	bl_idname = 'mesh.color_assign'
	bl_label = 'Assign Color'

	def invoke(self, context, event):
		scn = context.scene
		try:
			scn.vx_color = gh.hex_to_rgb(scn.vx_color_hex)
		except:
			self.report({'ERROR'}, 'Malformed hex color')

		return {'FINISHED'}


class get_color(bpy.types.Operator):
	bl_idname = 'mesh.color_get_hex'
	bl_label = 'Get Color'

	def invoke(self, context, event):
		scn = context.scene
		scn.vx_color_hex = gh.rgb_to_hex((
		 scn.vx_color.r * 255, scn.vx_color.g * 255, scn.vx_color.b * 255))
		return {
		 'FINISHED'}


class assign_color_to_map(bpy.types.Operator):
	bl_idname = 'mesh.paint_faces'
	bl_label = 'Paint Faces'

	def invoke(self, context, event):
		scn = context.scene
		object = context.object
		try:
			active_color_layer = object.data.vertex_colors.active.name
		except:
			self.report({'ERROR'}, 'No active color layer')
			return {
			 'CANCELLED'}
		else:
			gh.paint_faces(object, scn.vx_color, active_color_layer)
		return {'FINISHED'}


class auto_paint(bpy.types.Operator):
	bl_idname = 'mesh.auto_paint_mesh'
	bl_label = 'Auto Mesh Paint'

	def invoke(self, context, event):
		object = context.object
		if context.mode == 'EDIT_MESH':
			self.report({'ERROR'}, 'Should be in Object Mode')
			return {
			 'CANCELLED'}
		gh.auto_paint_mesh(object)
		return {
		 'FINISHED'}


class se7en_import(bpy.types.Operator):
	bl_idname = 'system.se7en_import'
	bl_label = ''
	bl_description = 'For importing mesh with new method by DeathGOD7'

	def invoke(self, context, event):
		scn = context.scene
		meshimportcount = 0
		gT = fifa3D_se7en.GameType
		mainrx3 = [gT.FIFA12, gT.FIFA13,gT.FIFA14,gT.FIFA15,gT.FIFA16]
		meshlist = []
		texlist = []
		meshLoc = [scn.model_import_path, scn.hair_import_path]
		texLoc = [scn.main_texture_import_path, scn.face_texture_import_path, scn.hair_texture_import_path, scn.eyes_texture_import_path]

		for x in meshLoc:
			if x != "":
				meshlist.append(x)

		for x in texLoc:
			if x != "":
				texlist.append(x)

		if scn.model_import_path != "":
			choosenGame = f"{scn.game_enum[0:4]} {scn.game_enum[4:6]}" 
			log = fifa_tools.globalLogFile
			if (scn.geometry_flag) and (len(meshlist) > 0):
				if choosenGame == gT.FIFA11:
					log.writeLog(f"Mode : {scn.se7en_mode}", LogType.INFO)
					for x in meshlist:
						mainImport = fifa3D_se7en.RX3_File_Hybrid(x, choosenGame)
						log.writeLog(f"File Import : {mainImport.fileName}{mainImport.fileExt}", LogType.INFO)
						
						for i in range(mainImport.meshCount):
							logstr = f"[{choosenGame}] RX3 Type : RX3 Hybrid || File Type : {mainImport.fileType} || File ID : {mainImport.fileId} || Endian Type : {mainImport.endianStr} || Mesh Count : {i+1}/{mainImport.meshCount} || Primitive Type : {mainImport.primitiveType} || Total Vertices : {mainImport.totalVertCount[i]} || Total Indices : {mainImport.indicesCount[i]} || Total Faces : {mainImport.faceCount[i]}"
							
							if (len(mainImport.uvCount) > i):
								logstr += f" || Total UVS : {mainImport.uvCount[i]}"
							if (len(mainImport.collisionCount) > i):
								logstr += f" || Total Collision : {mainImport.collisionCount[i]}"
							if (len(mainImport.vertexColorCount) > i):
								logstr += f" || Total Vertex Color : {mainImport.vertexColorCount[i]}"
							if (len(mainImport.bonesIndiceCount) > i):
								logstr += f" || Total Bone Indice : {mainImport.bonesIndiceCount[i]}"
							if (len(mainImport.bonesWeightCount) > i):
								logstr += f" || Total Bone Weight : {mainImport.bonesWeightCount[i]}" 

							log.writeLog(logstr, LogType.INFO)

							name = mainImport.fileType + '_' + str(mainImport.fileId) + '_' + str(i)
							if mainImport.fileType == 'head':
								if i == 0:
									name += '_' + "head"
								elif i == 1:
									name += '_' + "eyes"
							obname = fifa_main.se7en_importmesh(mainImport.vertexPosition[i] , mainImport.faces[i] , mainImport.uvs[i] , name , meshimportcount , 0 , mainImport.cols[i], False, [], scn.fifa_import_loc)
							meshimportcount += 1
							skeletoninfo = fifa3D_helper.LoadSkeletonInfo(mainImport.skeletonType.value)
							
							if (scn.bone_groups_flag) and (len(mainImport.bonesIndice) > i) and (len(mainImport.bonesWeight) > 1):
								if skeletoninfo != None:
									fifa3D_helper.AddVgroupToObjects(mainImport.bonesIndice[i], mainImport.bonesWeight[i], skeletoninfo, obname)

					if (scn.create_materials_flag) and (len(texlist) > 0):
						for x in texlist:
							secImport = fifa3D_se7en.RX3_File(x , choosenGame)
							fifa_main.se7en_creatematerials(secImport.texNames)
			

				elif choosenGame in mainrx3:
					log.writeLog(f"Mode : {scn.se7en_mode}", LogType.INFO)
					for x in meshlist:
						mainImport = fifa3D_se7en.RX3_File(x , choosenGame)
						log.writeLog(f"File Import : {mainImport.fileName}{mainImport.fileExt}", LogType.INFO)
						
						for i in range(mainImport.meshCount):
							logstr = f"[{choosenGame}] RX3 Type : RX3 || File Type : {mainImport.fileType} || File ID : {mainImport.fileId} || Endian Type : {mainImport.endianStr} || Mesh Count : {i+1}/{mainImport.meshCount} || Primitive Type : {mainImport.primitiveType} || Total Vertices : {mainImport.totalVertCount[i]} || Total Indices : {mainImport.indicesCount[i]} || Total Faces : {mainImport.faceCount[i]}"
							
							if (len(mainImport.uvCount) > i):
								logstr += f" || Total UVS : {mainImport.uvCount[i]}"
							if (len(mainImport.collisionCount) > i):
								logstr += f" || Total Collision : {mainImport.collisionCount[i]}"
							if (len(mainImport.vertexColorCount) > i):
								logstr += f" || Total Vertex Color : {mainImport.vertexColorCount[i]}"
							if (len(mainImport.bonesIndiceCount) > i):
								logstr += f" || Total Bone Indice : {mainImport.bonesIndiceCount[i]}"
							if (len(mainImport.bonesWeightCount) > i):
								logstr += f" || Total Bone Weight : {mainImport.bonesWeightCount[i]}" 

							log.writeLog(logstr, LogType.INFO)
							
							name = mainImport.fileType + '_' + str(mainImport.fileId) + '_' + str(i)
							if mainImport.fileType == 'head':
								if i == 0:
									name += '_' + "head"
								elif i == 1:
									name += '_' + "eyes"
							obname = fifa_main.se7en_importmesh(mainImport.vertexPosition[i] , mainImport.faces[i] , mainImport.uvs[i] , name , meshimportcount , 0 , mainImport.cols[i], False, [], scn.fifa_import_loc)
							meshimportcount += 1
							skeletoninfo = fifa3D_helper.LoadSkeletonInfo(mainImport.skeletonType.value)
							
							if (scn.bone_groups_flag) and (len(mainImport.bonesIndice) > i) and (len(mainImport.bonesWeight) > 1):
								if skeletoninfo != None:
									fifa3D_helper.AddVgroupToObjects(mainImport.bonesIndice[i], mainImport.bonesWeight[i], skeletoninfo, obname)
							
							if (scn.bones_flag) and (len(mainImport.bones) > 0):
								if skeletoninfo != None:
									fifa3D_helper.AddVertexSkeleton(mainImport.bones, mainImport.fileId, skeletoninfo)
						
					if (scn.create_materials_flag) and (len(texlist) > 0):
						for x in texlist:
							secImport = fifa3D_se7en.RX3_File(x , choosenGame)
							fifa_main.se7en_creatematerials(secImport.texNames)
			
				else:
					print(f"Unsupported Game or Type : {scn.game_enum}")
		else:
			print("Empty file path.")
		return {
		 'FINISHED'}

class se7en_export(bpy.types.Operator):
	bl_idname = 'system.se7en_export'
	bl_label = ''
	bl_description = 'For exporting mesh with new method by DeathGOD7'

	def invoke(self, context, event):
		scn = context.scene
		selectedObj = []
		for obj in bpy.context.selected_objects:
			selectedObj.append(obj)
		if len(selectedObj) > 0:
			fifa3D_helper.ConvertMeshToData(selectedObj[0])
		return {
		 'FINISHED'}

class visit_thread_url(bpy.types.Operator):
	bl_idname = 'system.visit_thread_url'
	bl_label = ''
	bl_description = 'Visit the official thread of this addon on soccergaming'

	def invoke(self, context, event):
		webbrowser.open(url='http://soccergaming.com/index.php?threads/se7en-fifa-3d-importer-exporter-updated-version-blender-2-8x.6470022/')
		return {
		 'FINISHED'}


class visit_github_url(bpy.types.Operator):
	bl_idname = 'system.visit_github_url'
	bl_label = ''
	bl_description = 'Checkout the GitHub wiki to find tutorials about this addon'

	def invoke(self, context, event):
		webbrowser.open(url='https://github.com/DeathGOD7/FIFA-3D-Importer-Exporter/wiki')
		return {
		 'FINISHED'}

class report_bug(bpy.types.Operator):
	bl_idname = 'system.report_bug'
	bl_label = ''
	bl_description = 'If you have found any bug or want any feature in this addon, click here'

	def invoke(self, context, event):
 		#https://github.com/DeathGOD7/FIFA-3D-Importer-Exporter/issues/new/choose
		webbrowser.open(url='https://github.com/DeathGOD7/FIFA-3D-Importer-Exporter/issues/new/choose')
		return {
		 'FINISHED'}

class assign_materials(bpy.types.Operator):
	bl_idname = 'mesh.assign_materials'
	bl_label = 'Assign Created Materials'
	bl_description = 'In Blender 2.80 and above, materials are auto assigned to mesh'
	bl_options = {'UNDO'}

	def invoke(self, context, event):
		dict = {'head': 'face',  'eyes': 'eyes'}
		for obj in bpy.context.scene.objects:
			if obj.type in ('LAMP', 'CAMERA', 'EMPTY'):
				continue
			ident = obj.name.split(sep='.')[0].split(sep='_')[(-1)]
			if ident in dict:
				try:
					for j in obj.data.materials:
						obj.data.materials.pop(0, update_data=True)

					print(ident)
					obj.data.materials.append(bpy.data.materials[(dict[ident] + '_' + obj.name.split(sep='_')[1])])
				except KeyError:
					self.report({
					 'ERROR'}, 'Missing ' + ident.title() + ' Material')

			else:
				try:
					for j in obj.data.materials:
						obj.data.materials.pop(0, update_data=True)

					obj.data.materials.append(bpy.data.materials[(obj.name.split(sep='_')[0] + '_' + obj.name.split(sep='_')[1])])
				except KeyError:
					self.report({
					 'ERROR'}, 'Missing ' + obj.name.split(sep='_')[0].title() + ' Material')

		self.report({'INFO'}, 'Materials Assigned Successfully')
		return {
		 'FINISHED'}


class lights_export(bpy.types.Operator):
	bl_idname = 'mesh.lights_export'
	bl_label = 'EXPORT LIGHTS'

	def invoke(self, context, event):
		print('Light Export Started: ' + strftime('%Y-%m-%d %H:%M:%S', gmtime()))
		object = context.object
		scn = context.scene
		textures_list = []
		offset_list = []
		xmlstring = ''
		indent = 0
		rot_x_mat = Matrix.Rotation(radians(-90), 4, 'X')
		scale_mat = Matrix.Scale(100, 4)
		xmlstring += '<particleSystem>\n'
		indent += 1
		xmlstring += '    '
		xmlstring += '<particleEffect name=' + chr(34) + 'glares_' + str(scn.file_id) + '_' + scn.stadium_version + chr(34) + '>\n'
		indent += 1
		xmlstring += indent * '\t'
		xmlstring += fifa_main.write_xml_param('iCullBehavior', 0, 0)
		for ob in scn.objects:
			if ob.name[0:7] == 'LIGHTS_':
				textures_list.append([
				 ob.actionrender_props.sTexture.split(sep='.dds')[0], os.path.join('fifa_tools', 'light_textures') + os.path.sep + ob.actionrender_props.sTexture.split(sep='.')[0] + '.dds', False, 0, 0, 0, 0, '', 128])
				xmlstring += indent * '\t'
				xmlstring += '<particleGroup name=' + chr(34) + ob.name[7:] + chr(34) + '>\n'
				indent += 1
				xmlstring += indent * '\t'
				xmlstring += fifa_main.write_xml_param('iNumParticlesMax', 0, len(ob.children))
				xmlstring += indent * '\t'
				xmlstring += '<particleAction name=' + chr(34) + 'ParticleActionEmitBox' + chr(34) + ' className=' + chr(34) + 'ParticleActionEmitBox' + chr(34) + '>\n'
				indent += 1
				for i in range(len(ob.children)):
					child = ob.children[i]
					if child.type == 'LAMP':
						co = child.location
						co = scale_mat * rot_x_mat * co
						xmlstring += indent * '\t'
						xmlstring += fifa_main.write_xml_param('vCenter', i, (round(co[0], 5), round(co[1], 5), round(co[2], 5)))
						continue

				for attr in class_dir(ob.emitbox_props):
					if attr in light_props:
						xmlstring += indent * '\t'
						xmlstring += fifa_main.write_xml_param(attr, 0, getattr(ob.emitbox_props, attr))
						continue

				indent -= 1
				xmlstring += indent * '\t'
				xmlstring += '</particleAction>\n'
				xmlstring += indent * '\t'
				xmlstring += '<particleAction name=' + chr(34) + 'ParticleActionRender' + chr(34) + ' className=' + chr(34) + 'ParticleActionRender' + chr(34) + '>\n'
				indent += 1
				for entry in light_props:
					cl_name = entry.__class__.__name__
					if cl_name == 'str':
						try:
							param = fifa_main.write_xml_param(entry, 0, getattr(ob.actionrender_props, entry))
							xmlstring += indent * '\t'
							xmlstring += param
						except:
							print('Not an ActionRender Property, skipping...')

					elif cl_name == 'list':
						if entry[0] == 'sShader':
							xmlstring += indent * '\t'
							xmlstring += fifa_main.write_xml_param(entry[0], 0, getattr(ob.actionrender_props, entry[0]))
							val = getattr(ob.actionrender_props, entry[0])
							if val == 'lynxVbeam.fx':
								sect = 2
							else:
								sect = 1
							for subprop in entry[sect]:
								xmlstring += indent * '\t'
								xmlstring += fifa_main.write_xml_param(subprop, 0, getattr(ob.actionrender_props, subprop))

						else:
							try:
								tempval = getattr(ob.actionrender_props, entry[0])
								xmlstring += indent * '\t'
								xmlstring += fifa_main.write_xml_param(entry[0], 0, tempval)
								if tempval:
									indent += 1
									for subprop in entry[1]:
										xmlstring += indent * '\t'
										xmlstring += fifa_main.write_xml_param(subprop, 0, getattr(ob.actionrender_props, subprop))

									indent -= 1
							except:
								print('Not an ActionRender Property, skipping...')

							continue

				indent -= 1
				xmlstring += indent * '\t'
				xmlstring += '</particleAction>\n'
				indent -= 1
				xmlstring += indent * '\t'
				xmlstring += '</particleGroup>\n'
				continue

		indent -= 1
		xmlstring += '    '
		xmlstring += '</particleEffect>\n'
		indent -= 1
		xmlstring += indent * '\t'
		xmlstring += '</particleSystem>\n'
		print('WRITING LNX FILE')
		filename = scn.export_path + 'glares_' + str(scn.file_id) + '_' + scn.stadium_version + '_' + scn.stadium_time
		f = open(filename + '.lnx', 'w')
		f.write(xmlstring)
		f.close()
		print('WRITING RX3 FILE')
		f = fifa_main.fifa_rx3(filename + '.rx3', True)
		f.offset_list, f.texture_list = fifa_main.read_converted_textures(offset_list, textures_list, 'fifa_tools\\light_textures\\')
		f.write_offsets_to_file()
		f.write_offset_data_to_file('fifa_tools\\light_textures\\')
		f.data.seek(offset_list[(-1)][1])
		f.data.seek(offset_list[(-1)][2], 1)
		s = bytes(sig, 'utf-8')
		f.data.write(s)
		f.data.close()
		print(offset_list)
		self.report({'INFO'}, 'Lights Exported Successfully.')
		return {
		 'FINISHED'}


class file_import(bpy.types.Operator):
	bl_idname = 'mesh.fifa_import'
	bl_label = 'IMPORT'
	bl_description='Import the rx3 files to blender.'

	def invoke(self, context, event):
		global dir
		global f
		global files
		global objectcount
		scn = context.scene
		
		paths = []
		paths.append(scn.model_import_path)
		paths.append(scn.hair_import_path)
		tex_paths = []
		tex_paths.append(scn.stadium_texture_import_path)
		tex_paths.append(scn.face_texture_import_path)
		tex_paths.append(scn.hair_texture_import_path)
		tex_paths.append(scn.eyes_texture_import_path)

		for path in paths:
			if not scn.obj_path == '':
				break
			if path == '':
				continue
			f = fifa_main.fifa_rx3(path, 0)
			if f.code == 'io_error':
				self.report({'ERROR'}, 'File Error')
				return {
				 'CANCELLED'}
			if f.code == 'file_copy':
				self.report({'ERROR'}, 'Illegal File')
				return {
				 'CANCELLED'}
			if f.code == 'corrupt_file':
				self.report({'ERROR'}, 'Corrupt File')
				return {
				 'CANCELLED'}
			if f.type == 'textures':
				return {
				 'CANCELLED'}
			files.append([f, f.type])
			f.file_ident()
			f.read_file_offsets(fifa_tools.texdir)
			print(f.group_names)
			if scn.geometry_flag is True:
				print('PASSING MESHES TO SCENE')
				for i in range(f.mesh_count):
					sub_name = f.type + '_' + str(f.id) + '_' + str(i)
					if f.type == 'head':
						sub_name += '_' + f.sub_names[i]
					obname = fifa_main.createmesh(f.vxtable[i], f.itable[i], f.uvs[i], f.type, objectcount, f.id, sub_name, f.cols[i], False, [], scn.fifa_import_loc)
					objectcount += 1
					if scn.bone_groups_flag:
						groups = {}
						for j in range(len(f.v_bones_i[i])):
							for k in f.v_bones_i[i][j]:
								if k not in groups:
									groups[k] = []
								elif j in groups[k]:
									continue
								else:
									groups[k].append(j)

						for j in groups:
							if str(j) not in bpy.data.objects[obname].vertex_groups:
								bpy.data.objects[obname].vertex_groups.new(name=str(j))
							# print(groups[j])
							bpy.data.objects[obname].vertex_groups[str(j)].add(groups[j], 1, 'ADD')

						continue

				for i in f.mat_assign_table:
					bpy.data.objects[(str(f.type) + '_' + str(f.id) + '_' + str(i[0]))].parent = bpy.data.objects[('group_' + str(i[2]))]

				for ob in scn.objects:
					if ob.name.split(sep='_')[0] == 'group':
						id = int(ob.name.split(sep='_')[1])
						try:
							ob.name = f.group_names[id]
						except IndexError:
							print('Missing Group Name')

						continue

			if scn.materials_flag is True:
				for index in range(len(f.materials)):
					new_mat = bpy.data.materials.new(f.materials[index][0])
					# new_mat.use_shadeless = True
					new_mat.shadow_method = 'NONE'
					new_mat.specular_intensity = 0
					#new_mat.use_transparency = True
					new_mat.show_transparent_back = True
					# new_mat.alpha = 0
					new_mat.alpha_threshold = 0
					#new_mat.specular_alpha = 0
					for i in f.materials[index][1]:
						new_mat.use_nodes = True
						bsdf = new_mat.node_tree.nodes["Principled BSDF"]
						
						new_tex = new_mat.node_tree.nodes.new('ShaderNodeTexImage')
						new_tex.image = bpy.data.images.load(fifa_tools.texdir + '\\' + i[1])
						new_mat.node_tree.links.new(bsdf.inputs['Base Color'], new_tex.outputs['Color'])
						
						# if bpy.data.materials:
						# 	bpy.data.materials[0] = new_mat
						# else:
						# 	bpy.data.materials.append(new_mat)
						
						# slot = new_mat.texture_slots.add()
						# print(i[0], i[1])
						# if i[0] not in bpy.data.textures:
						# 	new_tex = bpy.data.textures.new(i[0], type='IMAGE')
						# 	try:
						# 		new_tex.image = bpy.data.images.load(os.path.realpath(i[1]))
						# 	except RuntimeError:
						# 		print('!!!Texture Not Found!!!', i[1])
						# 		continue
						# 	except:
						# 		print('allh malakia')
						# 		continue

						# 	slot.texture = new_tex
						# else:
						# 	slot.texture = bpy.data.textures[i[0]]
						# slot.texture_coords = 'UV'
						# slot.use_map_color_diffuse = True
						# slot.use_map_alpha = True
						# slot.alpha_factor = 1
						# if i[0].split(sep='_')[0] == 'ambientTexture':
						# 	slot.uv_layer = 'map1'
						# 	slot.blend_type = 'MULTIPLY'
						# else:
						# 	slot.uv_layer = 'map0'
						# 	slot.blend_type = 'MIX'

				for i in f.mat_assign_table:
					try:
						bpy.data.objects[('stadium_' + str(f.id) + '_' + str(i[0]))].data.materials.append(bpy.data.materials[f.materials[i[1]][0]])
					except IndexError:
						print('Index Not In Range')

			if f.type == 'stadium':
				for i in range(f.mesh_count):
					bpy.data.objects[(f.type + '_' + str(f.id) + '_' + str(i))].name = str(i) + '_' + f.sub_names[i]

			if scn.bones_flag is True and len(f.bones) > 0:
				print(f.bones[0][0])
				print(f.bones[0][1])
				print(f.bones[0][2])
				print(f.bones[0][3])
				print(f.bones[0][4])
				print(f.bones[0][5])
				print(f.bones[0][6])
				for arm_id in range(len(f.bones)):
					amt = bpy.data.armatures.new('armature_' + str(f.id) + '_' + str(arm_id))
					ob = bpy.data.objects.new('armature_object_' + str(arm_id), amt)
					
					# -bpy.context.scene.objects.link(newCurve)
					# +bpy.context.collection.objects.link(newCurve)
					context.collection.objects.link(ob)
					# scn.objects.link(ob)
					# bpy.context.scene.objects.active = ob
					bpy.context.view_layer.objects.active = ob
					bpy.ops.object.mode_set(mode='EDIT')
					for i in range(len(f.bones[arm_id])):
						bone = amt.edit_bones.new('mynewnewbone_' + str(i))
						# bone.head, bone.tail, bone.roll = f.bones[arm_id][i]
						bone.head, bone.tail, bone.roll = f.bones[arm_id][i]

					bpy.ops.object.mode_set(mode='OBJECT')
					ob.scale = Vector((0.01, 0.01, 0.01))
					ob.rotation_euler[1] = 1.5707972049713135

			if scn.props_flag is True:
				print('FOUND PROPS: ', len(f.props))
				print('POSITIONS FOUND: ', len(f.prop_positions))
				for i in range(len(f.props)):
					object_name = gh.create_prop(f.props[i], f.prop_positions[i], f.prop_rotations[i])
					if 'PROPS' not in bpy.data.objects:
						bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0,
																			  0))
						bpy.data.objects['Empty'].name = 'PROPS'
						bpy.data.objects[object_name].parent = bpy.data.objects['PROPS']
					else:
						bpy.data.objects[object_name].parent = bpy.data.objects['PROPS']

			f.data.close()
			objectcount = 0
			if scn.collision_flag is True:
				collisioncount = 0
				for collision in f.collisions:
					obname = fifa_main.createmesh(collision[1], collision[2], [], collision[0], collisioncount, f.id, '', [], False, [], scn.fifa_import_loc)
					collisioncount += 1

				continue

		for path in tex_paths:
			if path == '':
				continue
			elif not path.split(sep='_')[(-1)].split(sep='.')[0] == 'textures':
				self.report({
				 'ERROR'}, 'No valid file selected as a texture file')
				return {
				 'CANCELLED'}
			else:
				f = fifa_main.fifa_rx3(path, 0)
				if f.code == 'io_error':
					self.report({'ERROR'}, 'File Error')
					return {
					 'CANCELLED'}
				if f.code == 'file_copy':
					self.report({'ERROR'}, 'Illegal File')
					return {
					 'CANCELLED'}
				if f.code == 'corrupt_file':
					self.report({'ERROR'}, 'Corrupt File')
					return {
					 'CANCELLED'}
				print(f)
				f.type = path.split(sep='\\')[(-1)].split(sep='_')[0] + '_' + 'texture'
				texObjName = f.type.split(sep='_')[0]
				f.file_ident()
				f.read_file_offsets(fifa_tools.texdir)

			if f.type == 'stadium_texture':
				continue
			if scn.create_materials_flag is True:
				if f.type.split(sep='_')[0] + '_' + str(f.id) not in bpy.data.materials:
					new_mat = bpy.data.materials.new(f.type.split(sep='_')[0] + '_' + str(f.id))
					new_mat.specular_intensity = 0
					# new_mat.use_shadeless = True
					new_mat.shadow_method = 'NONE'
					#new_mat.use_transparency = True
					new_mat.show_transparent_back = True
					# new_mat.alpha = 0
					new_mat.alpha_threshold = 0
					#new_mat.specular_alpha = 0
				else:
					# new_mat = bpy.data.materials[(f.type.split(sep='_')[0] + '_' + str(f.id))]
					new_mat = bpy.data.materials.new(f.type.split(sep='_')[0] + '_' + str(f.id))
					new_mat.specular_intensity = 0
					# new_mat.use_shadeless = True
					new_mat.shadow_method = 'NONE'
					#new_mat.use_transparency = True
					new_mat.show_transparent_back = True
					# new_mat.alpha = 0
					new_mat.alpha_threshold = 0
					#new_mat.specular_alpha = 0
					# for i in range(5):
					# 	new_mat.texture_slots.clear(i)

				for id in range(f.texture_count):
					name = f.tex_names[id]
					if len(name) == 0:
						print('Skipping Texture, Probably Unsupported')
						continue
					
					new_mat.use_nodes = True
					bsdf = new_mat.node_tree.nodes["Principled BSDF"]
					
					# slot = new_mat.texture_slots.add()
					# name_fixed = name.split(sep='.')[0:len(name.split(sep='.')) - 1]
					# name_fixed = '.'.join(name_fixed)
					# if name_fixed in bpy.data.textures:
					# 	new_tex = bpy.data.textures[name_fixed]
					# else:
					# 	new_tex = bpy.data.textures.new(name_fixed, type='IMAGE')
					
					new_tex = new_mat.node_tree.nodes.new('ShaderNodeTexImage')
					new_tex.image = bpy.data.images.load(fifa_tools.texdir + '\\' + name)
					new_mat.node_tree.links.new(bsdf.inputs['Base Color'], new_tex.outputs['Color'])
					
					_mainObjT = False
					for obj in bpy.data.objects:
						objName = obj.name.split(sep='_')[0]
						mainTextureToUse = ['shoe','ball']

						if any(x in objName for x in mainTextureToUse):
							_mainObjT = True

						if objName == texObjName:
							try:
								obj.data.materials[0] = new_mat
								# obj.material_slot_remove()
								# print ("removed material from " + obj.name)
							except:
								obj.data.materials.append(new_mat)
								# print (obj.name + " does not have materials.")

					if _mainObjT:
						break

					# slot.texture = new_tex
					# slot.texture_coords = 'UV'
					# slot.uv_layer = 'map0'
					# slot.blend_type = 'MIX'
					# slot.use_map_color_diffuse = True
					# slot.use_map_alpha = True
					# slot.alpha_factor = 1

				continue

		if not scn.obj_path == '':
			past_ob_list = set(bpy.data.objects)
			bpy.ops.import_scene.obj(filepath=scn.obj_path, axis_forward='-Z', axis_up='Y', use_image_search=True, split_mode='OFF', global_clamp_size=1, use_groups_as_vgroups=True)
			present_ob_list = set(bpy.data.objects)
			ob = list(present_ob_list - past_ob_list)[0]
		if not scn.crwd_import_path == '':
			f = fifa_main.fifa_rx3(scn.crwd_import_path, 0)
			if f.__class__.__name__ == 'str':
				self.report({'ERROR'}, 'File Error')
				return {
				 'CANCELLED'}
			f.type = 'crowd'
			print('FILE TYPE DETECTED: ', f.type)
			fifa_main.read_crowd_15(f)
			f.data.close()
			crowd_verts = []
			crowd_faces = []
			crowd_col = []
			crowd_types = []
			hardcoreHome = crowdGroup('hardcoreHome')
			metalcoreHome = crowdGroup('metalcoreHome')
			heavyHome = crowdGroup('heavyHome')
			popHome = crowdGroup('popHome')
			folkHome = crowdGroup('folkHome')
			chickenAway = crowdGroup('chickenAway')
			deadAway = crowdGroup('deadAway')
			crowdGroupList = []
			crowdGroupList.extend([hardcoreHome, metalcoreHome, heavyHome, popHome, folkHome, chickenAway, deadAway])
			count = 0
			clog = open('clog.txt', 'w')
			for i in range(len(f.crowd)):
				clog.write(str(f.crowd[i][2]))
				clog.write('\n')
				if f.crowd[i][1] == 180:
					print(i, f.crowd[i][1])
				rot_mat = Matrix.Rotation(math.radians(f.crowd[i][1]) + math.radians(90.0), 4, Vector((0,
																									   1,
																									   0)))
				rot_mat = rot_mat.to_3x3()
				v = Vector((
				 f.crowd[i][0][0], f.crowd[i][0][1], f.crowd[i][0][2]))
				v1 = Vector((10, 10, -10))
				v2 = Vector((-10, 10, -10))
				v3 = Vector((-10, -10, 10))
				v4 = Vector((10, -10, 10))
				v1 = rot_mat * v1
				v2 = rot_mat * v2
				v3 = rot_mat * v3
				v4 = rot_mat * v4
				v1 = v1 + v
				v2 = v2 + v
				v3 = v3 + v
				v4 = v4 + v
				crowd_verts.append((v1[0], v1[1], v1[2]))
				crowd_verts.append((v2[0], v2[1], v2[2]))
				crowd_verts.append((v3[0], v3[1], v3[2]))
				crowd_verts.append((v4[0], v4[1], v4[2]))
				crowd_faces.append((count, count + 1, count + 2, count + 3))
				crowd_col.append(f.crowd[i][3])
				crowd_types.append((
				 f.crowd[i][2], f.crowd[i][3], (count, count + 1, count + 2, count + 3)))
				count += 4

			clog.close()
			crowd_name = fifa_main.createmesh(crowd_verts, crowd_faces, [], f.type, 0, f.id, 'crowd', [], False, [], scn.fifa_import_loc)
			gh.crowd_col(crowd_name, crowd_col, 'seat_colors')
			if scn.game_enum == 'FIFA15':
				for i in crowd_types:
					if i[0][0] == 0:
						if i[0][1] == 0:
							hardcoreHome.addToGroup(i[0][3], i[2])
						elif i[0][1] == 128:
							metalcoreHome.addToGroup(i[0][3], i[2])
						else:
							print('New Core 2nd Byte: ', i[0][1])
					elif 1 <= i[0][0] <= 128:
						if i[0][1] == 0:
							heavyHome.addToGroup(i[0][3], i[2])
						elif i[0][1] == 128:
							popHome.addToGroup(i[0][3], i[2])
						elif i[0][1] == 255:
							folkHome.addToGroup(i[0][3], i[2])
						else:
							print('New MediCore 2nd Byte: ', i[0][1])
					elif 129 <= i[0][0] <= 255:
						if i[0][1] == 128:
							chickenAway.addToGroup(i[0][3], i[2])
						elif i[0][1] == 255:
							deadAway.addToGroup(i[0][3], i[2])
						else:
							print('New Away 2nd Byte: ', i[0][1])
					else:
						print('New crowd group type first byte', i[0][0])

			for group in crowdGroupList:
				group.passGroupsToObject(bpy.data.objects[crowd_name])

			bpy.data.objects[crowd_name].scale = Vector((0.001, 0.001, 0.001))
			bpy.data.objects[crowd_name].rotation_euler[0] = radians(90)
		if not scn.lnx_import_path == '':
			f = fifa_main.fifa_rx3(scn.lnx_import_path, 0)
			if f.__class__.__name__ == 'str':
				self.report({'ERROR'}, 'File Error')
				return {
				 'CANCELLED'}
			f.type = 'lights'
			print('FILE TYPE DETECTED: ', f.type)
			xmldata = minidom.parse(f.data)
			f.data.close()
			system = xmldata.childNodes[0]
			effect = system.childNodes[1]
			for i in range(3, len(effect.childNodes), 2):
				name = effect.childNodes[i].attributes['name'].value
				particlegroup = effect.childNodes[i]
				for j in range(1, len(particlegroup.childNodes), 2):
					if particlegroup.childNodes[j].tagName == 'particleAction':
						param = particlegroup.childNodes[j]
						for k in range(1, len(param.childNodes), 2):
							try:
								object = param.childNodes[k]
								if object.attributes['name'].value == 'vCenter':
									index = object.attributes['index'].value
									loc = tuple(float(i) / 1000 for i in object.attributes['value'].value[1:-1].split(sep=','))
									bpy.ops.object.lamp_add(type='POINT', location=loc)
									bpy.data.objects['Point'].name = name + '_' + index
							except:
								print('Skipping')

						continue

			bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
			bpy.data.objects['Empty'].name = 'LIGHTS'
			for object in bpy.data.objects:
				if object.type == 'LAMP':
					object.parent = bpy.data.objects['LIGHTS']
					continue

			bpy.data.objects['LIGHTS'].rotation_euler = Euler((1.570796251296997, -0.0,
															   0.0), 'XYZ')
		return {
		 'FINISHED'}


class texture_export(bpy.types.Operator):
	bl_idname = 'mesh.texture_export'
	bl_label = 'EXPORT TEXTURES'

	def invoke(self, context, event):
		scn = bpy.context.scene
		textures_list = []
		ambient_textures_list = []
		texture_dict = {}
		status = ''
		mat_exceptions = ['jumbotron']
		if scn.stadium_export_flag or scn.trophy_export_flag:
			print('EXPORTING TEXTURES IN NORMAL MODE')
			for item in bpy.data.objects:
				if scn.stadium_export_flag and item.type == 'EMPTY' and item.name[0:5] == 'stad_' or scn.trophy_export_flag and item.type == 'EMPTY' and item.name in ('BALL',
																																									   'TROPHY'):
					for child_item in item.children:
						mat = bpy.data.materials[child_item.material_slots[0].material.name]
						item_texture_dict, item_textures_list, ambient, status = tex_gh.get_textures_list(child_item)
						if ambient and ambient not in ambient_textures_list and mat.name not in mat_exceptions:
							ambient_textures_list.append(ambient)
						if mat.name in mat_exceptions:
							item_textures_list.append(ambient)
						texture_dict.update(item_texture_dict)
						for t in item_textures_list:
							if t not in textures_list:
								textures_list.append(t)
								continue

						if status == 'material_missing':
							self.report({'ERROR'}, 'Missing Material')
							return {
							 'CANCELLED'}

					continue

			textures_list.extend(ambient_textures_list)
			if scn.trophy_export_flag:
				type = 'trophy-ball_'
			if scn.stadium_export_flag:
				type = 'stadium'
			status = fifa_main.write_textures_to_file(textures_list, type, scn.file_id)
			if status == 'missing_texture_file':
				self.report({'ERROR'}, 'Missing ' + status.split(sep=',')[1] + ' Texture File')
				return {
				 'CANCELLED'}
			if status == 'success':
				self.report({'INFO'}, 'Textures exported Successfully')
			elif status == 'error':
				self.report({'ERROR'}, 'File Error')
			else:
				if scn.gen_overwriter_flag:
					print('EXPORTING TEXTURES IN OVERWRITING MODE')
				name = scn.model_import_path.split(sep='\\')[(-1)].split(sep='.')[0]
				id = name.split(sep='_')[1]
				type = name.split(sep='_')[0]
				try:
					object = bpy.data.objects[(type + '_' + str(id) + '_0')]
				except KeyError:
					self.report({
					 'ERROR'}, 'Missing Appropriate Object. Check the naming.')
				else:
					texture_dict, textures_list, ambient, status = fifa_main.get_textures_list(object)
					if ambient:
						textures_list.append(ambient)
					if status == 'material_missing':
						self.report({'ERROR'}, 'Missing Material')
						return {
						 'CANCELLED'}
					status = fifa_main.write_textures_to_file(textures_list, type, id)
					if status == 'missing_texture_file':
						self.report({
						 'ERROR'}, 'Missing ' + status.split(sep=',')[1] + ' Texture File')
						return {
						 'CANCELLED'}
					if status == 'success':
						self.report({'INFO'}, 'Textures exported Successfully')
					if scn.face_edit_flag:
						print('EXPORTING TEXTURES IN FACE EDITING MODE')
						parts = []
						if scn.face_edit_head_flag:
							pass
				try:
					name = scn.model_import_path.split(sep='\\')[(-1)].split(sep='.')[0]
					id = name.split(sep='_')[1]
					type = name.split(sep='_')[0]
					head_found = False
					eyes_found = False
				except:
					self.report({
					 'ERROR'}, 'Please select the original head file in the Main Model Path')
					return {
					 'CANCELLED'}
				else:
					try:
						object = bpy.data.objects[(type + '_' + str(id) + '_0_' + 'head')]
						head_found = True
					except KeyError:
						try:
							object = bpy.data.objects[(type + '_' + str(id) + '_1_' + 'head')]
							head_found = True
						except KeyError:
							self.report({'ERROR'}, 'Head Part not found')

					if head_found:
						texture_dict, textures_list, ambient, status = tex_gh.get_textures_list(object)
						if ambient:
							textures_list.append(ambient)
						if status == 'material_missing':
							self.report({'ERROR'}, 'Missing Face Material')
							return {
							 'CANCELLED'}
						type = 'face'
						status = fifa_main.write_textures_to_file(textures_list, type, id)
						if status == 'missing_texture_file':
							self.report({
							 'ERROR'}, 'Missing ' + status.split(sep=',')[1] + ' Texture File')
							return {
							 'CANCELLED'}
						if status == 'success':
							self.report({'INFO'}, 'Textures exported Successfully')
				type = name.split(sep='_')[0]

		try:
			object = bpy.data.objects[(type + '_' + str(id) + '_0_' + 'eyes')]
			eyes_found = True
		except KeyError:
			try:
				object = bpy.data.objects[(type + '_' + str(id) + '_1_' + 'eyes')]
				eyes_found = True
			except KeyError:
				self.report({'ERROR'}, 'Eyes Part not found')

		else:
			if eyes_found:
				texture_dict, textures_list, ambient, status = tex_gh.get_textures_list(object)
				if ambient:
					textures_list.append(ambient)
				if status == 'material_missing':
					self.report({'ERROR'}, 'Missing Eyes Material')
					return {
					 'CANCELLED'}
				type = 'eyes'
				status = fifa_main.write_textures_to_file(textures_list, type, id)
				if status == 'missing_texture_file':
					self.report({
					 'ERROR'}, 'Missing ' + status.split(sep=',')[1] + ' Texture File')
					return {
					 'CANCELLED'}
				if status == 'success':
					self.report({'INFO'}, 'Textures exported Successfully')
			if scn.face_edit_hair_flag:
				try:
					name = scn.hair_import_path.split(sep='\\')[(-1)].split(sep='.')[0]
					id = name.split(sep='_')[1]
					type = name.split(sep='_')[0]
				except:
					self.report({
					 'ERROR'}, 'Please select the original hair file in the Main Model Path')
					return {
					 'CANCELLED'}

				try:
					object = bpy.data.objects[(type + '_' + str(id) + '_0')]
				except KeyError:
					self.report({'ERROR'}, 'Hair Part not found')
					return {
					 'CANCELLED'}
				else:
					texture_dict, textures_list, ambient, status = tex_gh.get_textures_list(object)
					if ambient:
						textures_list.append(ambient)
					if status == 'material_missing':
						self.report({'ERROR'}, 'Missing Material')
						return {
						 'CANCELLED'}
					status = fifa_main.write_textures_to_file(textures_list, type, id)
					if status == 'missing_texture_file':
						self.report({
						 'ERROR'}, 'Missing ' + status.split(sep=',')[1] + ' Texture File')
						return {
						 'CANCELLED'}
				if status == 'success':
					self.report({'INFO'}, 'Textures exported Successfully')
		return {
		 'FINISHED'}


class fifa_3d_model:

	def __init__(self):
		self.diffuseId = 0
		self.name = ''
		self.colorList = []
		self.boundBox = ()
		self.meshDescr = ''
		self.meshDescrShort = ''
		self.chunkLength = 0
		self.vertsCount = 0
		self.verts = []
		self.uvLayerCount = 0
		self.uvs = []
		self.indicesCount = 0
		self.indices = []
		self.colors = []
		self.normals = []
		self.material = 0


class file_export(bpy.types.Operator):
	bl_idname = 'mesh.fifa_export'
	bl_label = 'EXPORT'

	def invoke(self, context, event):
		scn = bpy.context.scene
		print('FIFA Exporter')
		if scn.stadium_export_flag:
			f = fifa_main.fifa_rx3(scn.export_path + 'stadium_' + str(scn.file_id) + '.rx3', 1)
		elif scn.trophy_export_flag:
			f = fifa_main.fifa_rx3(scn.export_path + 'trophy-ball_' + str(scn.file_id) + '.rx3', 1)
		#else:
		for item in bpy.data.objects:
			print(f'Object Name : {item.name}')
			print(f'Object Type : {item.type}')
			print(f'Object Child : {item.children}')

			if scn.stadium_export_flag and item.type == 'EMPTY' and item.name == 'PROPS':
				item_matrix_wrld = item.matrix_world
				rot_x_mat = Matrix.Rotation(radians(-90), 4, 'X')
				scale_mat = Matrix.Scale(100, 4)
				for child_item in item.children:
					co = scale_mat * rot_x_mat * item_matrix_wrld * child_item.location
					rot = (child_item.rotation_euler[0],
						child_item.rotation_euler[2], child_item.rotation_euler[1])
					rot = (
						round(rot[0] + radians(90)), round(rot[1] - radians(180)), round(rot[2]))
					f.prop_list.append((
						child_item.name, (co[0], co[1], co[2]), rot))

			if scn.stadium_export_flag and item.type == 'MESH' and item.name[0:14] == 'stad_Collision':
				entry = []
				collision_tris_length, collision_verts_table, collision_part_name = fifa_main.convert_mesh_collisions(item)
				entry.append(collision_tris_length)
				entry.append(collision_verts_table)
				entry.append(collision_part_name)
				f.collision_list.append(entry)
				continue

			if item.type == 'EMPTY' and item.name[0:5] == 'stad_':
				print(item.name)
				if len(item.children) == 0:
					continue
				if scn.stadium_export_flag:
					if len(f.group_list) == 0:
						group_object_offset = 0
					else:
						group_object_offset = f.group_list[(-1)][4] + f.group_list[(-1)][3]
					f.group_list.append([
						item.name, [0, 0, 0], [0, 0, 0], len(item.children), group_object_offset])
					f.group_list[(-1)][1], f.group_list[(-1)][2] = gh.group_bbox(item)
				print('Group Found: ' + str(item.name))
				for child_item in item.children:
					entry = fifa_3d_model()
					entry.diffuseId = 0
					entry.name = child_item.name
					entry.colorList, entry.boundBox, entry.meshDescr, entry.meshDescrShort, entry.chunkLength = fifa_main.convert_mesh_init(child_item, 0)
					entry.vertsCount, entry.verts, entry.uvLayerCount, entry.uvs, entry.indicesCount, entry.indices, entry.colors, entry.normals = fifa_main.convert_mesh_init(child_item, 1)
					if scn.stadium_export_flag:
						try:
							mat_name = child_item.material_slots[0].name
							if mat_name not in f.material_dict:
								materialType = mat_name.split(sep='_')[0]
								if materialType in standard_materials:
									local_mat_name = materialType
								elif bpy.data.materials[mat_name].use_transparency:
									local_mat_name = 'diffusealpha'
								else:
									local_mat_name = 'diffuseopaque'
								local_texture_list = []
								local_texture_name_list = []
								textureCount = 0
								for i in range(10):
									try:
										local_texture_list.append(bpy.data.materials[mat_name].texture_slots[i].name)
										local_texture_name_list.append(texture_slotType_dict[i])
										textureCount += 1
									except:
										print('Empty Texture Slot')

								print(local_texture_name_list)
								size = 16 + len(local_mat_name) + 1
								for i in range(len(local_texture_name_list)):
									size += len(local_texture_name_list[i])
									size += 5

								size = gh.size_round(size)
								f.material_dict[mat_name] = (
									mat_name, local_mat_name, local_texture_list, local_texture_name_list, size)
								f.material_list.append(mat_name)
								for i in range(textureCount):
									if local_texture_list[i] not in f.texture_list:
										f.texture_list.append(local_texture_list[i])
										continue

								try:
									entry_diffuse = f.texture_list.index(local_texture_list[0])
									entry_material = f.material_list.index(mat_name)
								except:
									self.report({
										'ERROR'}, 'Missing Texture in ' + str(child_item.name))
									return {
										'CANCELLED'}

							try:
								entry_diffuse = f.texture_list.index(f.material_dict[mat_name][2][0])
								entry_material = f.material_list.index(mat_name)
							except:
								self.report({
									'ERROR'}, 'Missing Texture in ' + str(child_item.name))
								return {
									'CANCELLED'}

						except IndexError:
							print('No material in object' + str(child_item.name))

					entry.diffuseId = entry_diffuse
					try:
						entry.material = entry_material
					except:
						pass
					else:
						f.object_list.append(entry)

			if item.type == 'MESH' and ('trophy' in item.name or 'ball' in item.name):
				#print(item.name)
				if len(item.children) != 0:
					continue
				
				entry = fifa_3d_model()
				entry.diffuseId = 0
				entry_diffuse = 0
				entry.name = item.name
				entry.colorList, entry.boundBox, entry.meshDescr, entry.meshDescrShort, entry.chunkLength = fifa_main.convert_mesh_init(item, 0)
				entry.vertsCount, entry.verts, entry.uvLayerCount, entry.uvs, entry.indicesCount, entry.indices, entry.colors, entry.normals = fifa_main.convert_mesh_init(item, 1)
				
				if scn.trophy_export_flag:
					try:
						mat_name = item.material_slots[0].name
						if mat_name not in f.material_dict:
							materialType = mat_name.split(sep='_')[0]
							if materialType in standard_materials:
								local_mat_name = materialType
							elif bpy.data.materials[mat_name].use_transparency:
								local_mat_name = 'diffusealpha'
							else:
								local_mat_name = 'diffuseopaque'
							local_texture_list = []
							local_texture_name_list = []
							textureCount = 0
							for i in range(10):
								try:
									local_texture_list.append(bpy.data.materials[mat_name].texture_slots[i].name)
									local_texture_name_list.append(texture_slotType_dict[i])
									textureCount += 1
								except:
									print('Empty Texture Slot')

							print(local_texture_name_list)
							size = 16 + len(local_mat_name) + 1
							for i in range(len(local_texture_name_list)):
								size += len(local_texture_name_list[i])
								size += 5

							size = gh.size_round(size)
							f.material_dict[mat_name] = (
								mat_name, local_mat_name, local_texture_list, local_texture_name_list, size)
							f.material_list.append(mat_name)
							for i in range(textureCount):
								if local_texture_list[i] not in f.texture_list:
									f.texture_list.append(local_texture_list[i])
									continue

							try:
								entry_diffuse = f.texture_list.index(local_texture_list[0])
								entry_material = f.material_list.index(mat_name)
							except:
								self.report({
									'ERROR'}, 'Missing Texture in ' + str(item.name))
								return {
									'CANCELLED'}

						try:
							entry_diffuse = f.texture_list.index(f.material_dict[mat_name][2][0])
							entry_material = f.material_list.index(mat_name)
						except:
							self.report({
								'ERROR'}, 'Missing Texture in ' + str(item.name))
							return {
								'CANCELLED'}
					except IndexError:
						print('No material in object' + str(item.name))

				entry.diffuseId = entry_diffuse
				try:
					entry.material = entry_material
				except:
					pass
				
				f.object_list.append(entry)


			f.write_offsets(0)
			f.write_offsets(1)
			print('Overall Objects Detected:', len(f.object_list))
			print('Materials Detected:', len(f.material_list))
			print(f.texture_list)
			f.write_offsets_to_file()
			f.write_offset_data_to_file('fifa_tools\\')
			f.data.seek(f.offset_list[(-1)][1])
			f.data.seek(f.offset_list[(-1)][2], 1)
			s = bytes(sig, 'utf-8')
			f.data.write(s)
			f.data.close()
			self.report({'INFO'}, 'Model Exported Successfully')

		return {'FINISHED'}


class crowd_export(bpy.types.Operator):
	bl_idname = 'mesh.crowd_export'
	bl_label = 'EXPORT CROWD'

	def invoke(self, context, event):
		scn = bpy.context.scene
		crowd_found = False
		for i in bpy.data.objects:
			if i.name == 'crowd':
				ob = i
				crowd_found = True
				break

		if not crowd_found:
			self.report({'ERROR'}, 'No crowd object found, Nothing exported')
			return {
			 'CANCELLED'}
		f = open(scn.export_path + 'crowd_' + str(scn.file_id) + '_' + scn.stadium_version + '.dat', 'wb')
		fifa_main.write_crowd_file(f, ob)
		f.close()
		self.report({'INFO'}, 'Crowd Exported')
		return {
		 'FINISHED'}


class ob_group_separator(bpy.types.Operator):
	bl_idname = 'mesh.ob_vertex_groups_separate'
	bl_label = 'SPLIT MODEL'

	def invoke(self, context, event):
		scn = bpy.context.scene
		object = context.object
		if context.mode == 'EDIT_MESH':
			fifa_func.object_separate(object)
		else:
			self.report({'ERROR'}, 'Must be in Object Mode')
		return {
		 'FINISHED'}


class file_overwrite(bpy.types.Operator):
	bl_idname = 'mesh.fifa_overwrite'
	bl_label = 'OVERWRITE'

	def invoke(self, context, event):
		global e
		scn = context.scene
		dict = {'head': 'face',  'eyes': 'eyes'}
		parts_dict = {}
		if scn.gen_overwriter_flag:
			print('GENERAL OVERWRITING MODE PROCEDURE \n')
			name = scn.model_import_path.split(sep='\\')[(-1)]
			try:
				copyfile(scn.model_import_path, scn.export_path + '\\' + name)
			except FileNotFoundError:
				self.report({'ERROR'}, 'File Not Found')
				return {
				 'CANCELLED'}
			else:
				e = fifa_main.fifa_rx3(scn.export_path + '\\' + name, 0)
				if e == 'io_error':
					self.report({'ERROR'}, 'File Error')
					return {
					 'CANCELLED'}
				if e == 'corrupt_file':
					self.report({'ERROR'}, 'Corrupt File')
					return {
					 'CANCELLED'}
				if e == 'file_clopy':
					self.report({'ERROR'}, 'Illegal File')
					return {
					 'CANCELLED'}
				e.overwrite_geometry_data()
		if scn.face_edit_flag:
			print('FACE EDITING MODE PROCEDURES \n')
			parts = []
			status = 0
			if scn.face_edit_head_flag and scn.model_import_path:
				parts.append(scn.model_import_path)
				status = 1
			if scn.face_edit_hair_flag and scn.hair_import_path:
				parts.append(scn.hair_import_path)
				status = 1
			if not status:
				self.report({
				 'ERROR'}, 'Please select the original head file in the Main Model Path')
				return {
				 'CANCELLED'}
			if scn.face_edit_hair_flag and scn.hair_import_path:
				parts.append(scn.hair_import_path)
			progress = 0
			for path in parts:
				name = path.split(sep=os.sep)[(-1)]
				try:
					t = fifa_main.fifa_rx3(path, 0)
					copyfile(t.data.raw.name, scn.export_path + os.sep + name)
				except FileNotFoundError:
					self.report({'ERROR'}, 'File Not Found')
					return {
					 'CANCELLED'}
				else:
					e = fifa_main.fifa_rx3(scn.export_path + os.sep + name, 0)
					if e == 'io_error':
						self.report({'ERROR'}, 'File Error')
						return {
						 'CANCELLED'}
					if e == 'corrupt_file':
						self.report({'ERROR'}, 'Corrupt File')
						return {
						 'CANCELLED'}
					if e == 'file_clopy':
						self.report({'ERROR'}, 'Illegal File')
						return {
						 'CANCELLED'}
					e.overwrite_geometry_data()
				progress += 1

			print('Total Files Modified ', progress)
		return {'FINISHED'}


class batch_importer(bpy.types.Operator):
	bl_idname = 'mesh.batch_import'
	bl_label = 'Batch Import Models'

	def invoke(self, context, event):
		scn = bpy.context.scene
		path = scn.batch_import_path
		count = 0
		for fpath in os.listdir(path):
			if len(fpath.split(sep='.rx3')) > 1 and 'textures' not in fpath:
				count += 1
				continue

		step = float(360 / count)
		print('step: ', step)
		count = 0
		for fpath in os.listdir(path):
			vec = Vector((0, scn.batch_radius, 0))
			if len(fpath.split(sep='.rx3')) > 1 and 'textures' not in fpath:
				eul = Euler()
				eul.rotate_axis('Z', radians(count * step))
				vec.rotate(eul)
				scn.fifa_import_loc = vec
				scn.fifa_import_loc[1] *= -1
				print('importing model')
				scn.model_import_path = path + fpath
				scn.geometry_flag = True
				bpy.ops.mesh.fifa_import('INVOKE_DEFAULT')
				count += 1
				continue

		return {
		 'FINISHED'}


class rx3Unlocker(bpy.types.Operator):
	bl_idname = 'system.rx3_unlock'
	bl_label = '.rx3 File Unlocker'

	def invoke(self, context, event):
		scn = bpy.context.scene
		if not scn.model_import_path:
			self.report({'ERROR'}, 'No file selected in the model import path')
			return {
			 'CANCELLED'}
		f = open(scn.model_import_path, 'rb')
		path, filename = os.path.split(scn.model_import_path)
		t = open(os.path.join(path, 'temp.rx3'), 'wb')
		t.write(f.read(8))
		size = struct.unpack('<I', f.read(4))[0]
		t.write(struct.pack('<I', size))
		t.write(f.read(size - 12))
		f.close()
		os.remove(scn.model_import_path)
		os.rename(os.path.join(path, 'temp.rx3'), scn.model_import_path)
		return {
		 'FINISHED'}


class group_add(bpy.types.Operator):
	bl_idname = 'system.add_stad_groups'
	bl_label = 'Add Groups'

	def invoke(self, context, event):
		for name in group_names_15:
			if 'stad_' + name not in bpy.data.objects:
				bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
				ob = bpy.data.objects['Empty']
				ob.name = 'stad_' + name
				continue

		return {
		 'FINISHED'}


class fix_relative_paths(bpy.types.Operator):
	bl_idname = 'system.fix_relative_paths'
	bl_label = 'Fix Settings'
	bl_description = 'In Blender 2.80 and above relative path default is set to TRUE'

	def invoke(self, context, event):
		bpy.context.user_preferences.filepaths.use_relative_paths = False
		bpy.context.scene.game_settings.material_mode = 'GLSL'
		return {
		 'FINISHED'}


class clear_temp_directory(bpy.types.Operator):
	bl_idname = 'system.clean_temp_dir'
	bl_label = 'Clean Up'
	bl_description = 'Delete all textures from temp texture folder'

	def invoke(self, context, event):
		files = os.listdir(fifa_tools.texdir)
		count = 0
		for f in files:
			if f.endswith('.dds') or f.endswith('.decompressed'):
				count += 1
				os.remove(fifa_tools.texdir + os.sep + f)
				print('Deleting ' + f)
				continue

		self.report({'INFO'}, str(count) + ' Textures Removed')
		return {
		 'FINISHED'}


class add_prop(bpy.types.Operator):
	bl_idname = 'system.add_prop'
	bl_label = 'Add Prop'
	bl_description = 'Adds Selected Prop to Curosr Location in the scene'

	def invoke(self, context, event):
		scn = context.scene
		gh.create_prop(scn.prop_enum, scn.cursor_location, (0, 0, 0))
		return {
		 'FINISHED'}


class remove_meshes(bpy.types.Operator):
	bl_idname = 'mesh.remove_meshes'
	bl_label = 'Remove Unused Meshes'
	bl_description = 'Remove Unused Meshes'

	def invoke(self, context, event):
		
		#CURVE
		curves = 0
		for o in bpy.context.scene.objects:
			if o.type == 'CURVE':
				bpy.data.objects.remove(o, do_unlink=True)
				curves += 1

		#LIGHT
		lights = 0
		for o in bpy.context.scene.objects:
			if o.type == 'LIGHT':
				bpy.data.objects.remove(o, do_unlink=True)
				lights += 1

		# ARMATURE
		armatures = 0
		for o in bpy.context.scene.objects:
			if o.type == 'ARMATURE':
				bpy.data.objects.remove(o, do_unlink=True)
				armatures += 1

		# CAMERA		
		cameras = 0
		for o in bpy.context.scene.objects:
			if o.type == 'CAMERA':
				bpy.data.objects.remove(o, do_unlink=True)
				cameras += 1


		self.report({'INFO'}, str(curves) + ' Unused Curves Removed, ' + str(lights) + ' Unused Lights Removed, ' + str(armatures) + ' Unused Armatures Removed, ' + str(cameras) + ' Unused Cameras Removed')
		return {
		 'FINISHED'}


class clean_paths(bpy.types.Operator):
	bl_idname = 'mesh.clean_paths'
	bl_label = 'Clean Paths'
	bl_description = 'Clear all Script Paths'

	def invoke(self, context, event):
		scn = bpy.context.scene
		scn.model_import_path = ''
		scn.hair_import_path = ''
		scn.stadium_texture_import_path = ''
		scn.face_texture_import_path = ''
		scn.hair_texture_import_path = ''
		scn.eyes_texture_import_path = ''
		scn.lnx_import_path = ''
		scn.crwd_import_path = ''
		scn.export_path = ''
		self.report({'INFO'}, 'Paths Cleared')
		return {
		 'FINISHED'}


class hide_props(bpy.types.Operator):
	bl_idname = 'mesh.hide_props'
	bl_label = 'Hide/Show Props'
	bl_description = 'Toggles Prop visibility'

	def invoke(self, context, event):
		for object in bpy.data.objects:
			if 'PROPS' in object.name :
				object.hide_set(object.visible_get())

			self.report({'INFO'}, 'Props View Toggled')

		return {'FINISHED'}



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
	align_crowd_faces,
	crowd_create_seats,
	assign_crowd_type,
	colour_assign,
	get_color,
	assign_color_to_map,
	auto_paint,
	se7en_import,
	se7en_export,
	visit_thread_url,
	visit_github_url,
	report_bug,
	assign_materials,
	lights_export,
	file_import,
	texture_export,
	file_export,
	crowd_export,
	ob_group_separator,
	file_overwrite,
	batch_importer,
	rx3Unlocker,
	group_add,
	fix_relative_paths,
	clear_temp_directory,
	add_prop,
	remove_meshes,
	clean_paths,
	hide_props
	]

def register():
	for cls in classes:
		make_annotations(cls) # what is this? Read the section on annotations above!
		bpy.utils.register_class(cls)



def unregister():  # note how unregistering is done in reverse
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)


if __name__ == '__main__':
	register()
# global tex_names ## Warning: Unused global