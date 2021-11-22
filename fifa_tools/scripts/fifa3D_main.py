# uncompyle6 version 3.5.0
# Python bytecode 3.4 (3310)
# Decompiled from: Python 2.7.5 (default, Nov 16 2020, 22:23:17) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: M:\Blender\blender-2.72-windows64\fifa_tools\scripts\fifa_main.py
# Compiled at: 2015-03-16 19:47:39
# Size of source mod 2**32: 76106 bytes

# Decompiled by Death GOD 7 from original fifa15_main.pyc

from fifa_tools import bl_info
import fifa_tools
vr = bl_info["version"]
version = (vr[0], vr[1], vr[2])
#version = (0, 67, 'alpha')

import bpy, imp, os, struct, bmesh, zlib, sys
from math import radians, degrees
from io import BytesIO
from shutil import copyfile
linux_path = '/media/2tb/Blender/blender-2.71-windows64'
if os.name == 'nt':
	prePath = ''
else:
	prePath = linux_path + os.sep
# fifa_func_path = 'fifa_tools' + os.sep + 'scripts' + os.sep + 'fifa3D_functions.py'
# fifa_func = imp.load_source(
#     'fifa_func', prePath + fifa_func_path)
#fifa_func = imp.load_compiled('fifa_func', 'fifa_tools' + os.sep + 'scripts' + os.sep + 'fifa3D_functions.pyc')
from mathutils import Vector, Euler, Matrix
from math import radians, sqrt
from subprocess import call

version_text = 'v' + str(version[0]) + '.' + \
	str(version[1]) + '.' + str(version[2])
credit1 = version_text + ", FIFA 3D Importer / Exporter "
credit2 = "Maintained & Updated by Death GOD 7 (Original Author : arti-10)"
sig = credit1 + '\n' + credit2

# from fifa_func import general_helper as gh
# from fifa_func import texture_helper as tex_gh
# from fifa_func import half

from fifa_tools.scripts.fifa3D_functions import general_helper as gh
from fifa_tools.scripts.fifa3D_functions import texture_helper as tex_gh
from fifa_tools.scripts.fifa3D_functions import half

comp = half.Float16Compressor()


class crowdGroup:
	fullNessDict = {'full': 255,  'almostFull': 75, 
	 'halfFull': 25, 
	 'almostEmpty': 10, 
	 'empty': 0}
	typeDict = {'hardcoreHome': (0, 0),  'metalcoreHome': (128, 0), 
	 'heavyHome': (0, 128), 
	 'popHome': (128, 128), 
	 'folkHome': (255, 128), 
	 'chickenAway': (128, 255), 
	 'deadAway': (255, 255)}

	def __init__(self, name):
		self.full = []
		self.almostFull = []
		self.halfFull = []
		self.almostEmpty = []
		self.empty = []
		self.name = name

	def passGroupsToObject(self, ob):
		if self.full:
			gname = self.name + '_full'
			ob.vertex_groups.new(gname)
			ob.vertex_groups[gname].add(self.full, 1, 'ADD')
		if self.almostFull:
			gname = self.name + '_almostFull'
			ob.vertex_groups.new(gname)
			ob.vertex_groups[gname].add(self.almostFull, 1, 'ADD')
		if self.halfFull:
			gname = self.name + '_halfFull'
			ob.vertex_groups.new(gname)
			ob.vertex_groups[gname].add(self.halfFull, 1, 'ADD')
		if self.almostEmpty:
			gname = self.name + '_almostEmpty'
			ob.vertex_groups.new(gname)
			ob.vertex_groups[gname].add(self.almostEmpty, 1, 'ADD')
		if self.empty:
			gname = self.name + '_empty'
			ob.vertex_groups.new(gname)
			ob.vertex_groups[gname].add(self.empty, 1, 'ADD')

	def addToGroup(self, value, items):
		if 76 <= value <= 255:
			self.full.extend(items)
		elif 26 <= value <= 75:
			self.almostFull.extend(items)
		elif 11 <= value <= 25:
			self.halfFull.extend(items)
		elif 1 <= value <= 10:
			self.almostEmpty.extend(items)
		else:
			self.empty.extend(items)


def createmesh(verts, faces, uvs, name, count, id, subname, colors, normal_flag, normals, loc):
	# scn = bpy.context.scene
	#print(f"Face:{faces}, UVs:{uvs}, Name:{name}, Count:{count}, ID:{id}, SubName:{subname}, Colors:{colors}, Normal Flag:{normal_flag}, Normals:{normals}, Loc:{loc}")
	#print(f"UVs:{uvs}, Count:{count}")
	print(f"Vertices 0 : {verts[0]}")
	print(f"Face 0 : {faces[0]}")
	# if len(colors[0]) > 0 :
	# 	print(f"Colors 0: {colors[0][0]}")
	# if len(uvs[0]) > 0 :
	# 	print(f"UVS 0: {uvs[0][0]}")
	scn = bpy.context.scene
	mesh = bpy.data.meshes.new('mesh' + str(count))
	mesh.from_pydata(verts, [], faces)
	## mesh.update()

	for i in range(len(uvs)):
		uvtex = mesh.uv_layers.new(name='map' + str(i))

	for i in range(len(colors)):
		coltex = mesh.vertex_colors.new(name='col' + str(i))

	bm = bmesh.new()
	bm.from_mesh(mesh)

	for i in range(len(uvs)):
		uvlayer = bm.loops.layers.uv[('map' + str(i))]
		for f in bm.faces:
			for l in f.loops:
				l[uvlayer].uv.x = uvs[i][l.vert.index][0]
				l[uvlayer].uv.y = 1 - uvs[i][l.vert.index][1]

	for i in range(len(colors)):
		collayer = bm.loops.layers.color[('col' + str(i))]
		for f in bm.faces:
			for l in f.loops:
				#l[collayer].r, l[collayer].g, l[collayer].b = colors[i][l.vert.index]
				l[collayer].x, l[collayer].y, l[collayer].z = colors[i][l.vert.index]

	if normal_flag == True:
		for i in range(len(normals)):
			bm.verts[i].normal = normals[i]

	bm.to_mesh(mesh)
	bm.free()
	if name.split(sep='_')[0] in ('stadium', 'head'):
		object = bpy.data.objects.new(subname, mesh)
	else:
		object = bpy.data.objects.new(name + '_' + str(id) + '_' + str(count), mesh)
	object.location = loc
	scn.collection.objects.link(object)
	#scn.objects.link(object)
	return object.name

def testmesh(verts, faces, uvs, name, count, id, subname, colors, normal_flag, normals, loc):
	# scn = bpy.context.scene
	#print(f"Face:{faces}, UVs:{uvs}, Name:{name}, Count:{count}, ID:{id}, SubName:{subname}, Colors:{colors}, Normal Flag:{normal_flag}, Normals:{normals}, Loc:{loc}")
	#print(f"UVs:{uvs}, Count:{count}")
	print(f"Vertices 0 : {verts[0]}")
	print(f"Face 0 : {faces[0]}")
	if len(colors) > 0 :
		print(f"Colors 0: {colors[0]}")
	if len(uvs) > 0 :
		print(f"UVS 0: {uvs[0]}")
	scn = bpy.context.scene
	mesh = bpy.data.meshes.new('mesh' + str(count))
	mesh.from_pydata(verts, [], faces)
	## mesh.update()

	if len(uvs) > 0 :
		# for i in range(len(uvs)):
		for i in range(1):
			uvtex = mesh.uv_layers.new(name='map' + str(i))

	if len(colors) > 0 :
		# for i in range(len(colors)):
		for i in range(1):
			coltex = mesh.vertex_colors.new(name='col' + str(i))

	bm = bmesh.new()
	bm.from_mesh(mesh)

	if len(uvs) > 0 :
		# for i in range(len(uvs)):
		for i in range(1):
			uvlayer = bm.loops.layers.uv[('map' + str(i))]
			for f in bm.faces:
				for l in f.loops:
					l[uvlayer].uv.x = uvs[l.vert.index][0]
					l[uvlayer].uv.y = 1 - uvs[l.vert.index][1]
					# l[uvlayer].uv.x = uvs[i][l.vert.index][0]
					# l[uvlayer].uv.y = 1 - uvs[i][l.vert.index][1]

	if len(colors) > 0 :
		for i in range(1):
			collayer = bm.loops.layers.color[('col' + str(i))]
			for f in bm.faces:
				for l in f.loops:
					#l[collayer].r, l[collayer].g, l[collayer].b = colors[i][l.vert.index]
					l[collayer].x, l[collayer].y, l[collayer].z = colors[l.vert.index]
					# l[collayer].x, l[collayer].y, l[collayer].z = colors[i][l.vert.index]

	if normal_flag == True:
		for i in range(len(normals)):
			bm.verts[i].normal = normals[i]

	bm.to_mesh(mesh)
	bm.free()
	if name.split(sep='_')[0] in ('stadium', 'head'):
		object = bpy.data.objects.new(subname, mesh)
	else:
		object = bpy.data.objects.new(name + '_' + str(id) + '_' + str(count), mesh)
	object.location = loc
	scn.collection.objects.link(object)
	#scn.objects.link(object)
	return object.name


class fifa_rx3:

	def __init__(self, path, mode):
		self.path = path
		self.data = 0
		self.offsets = []
		self.mesh_offsets = []
		self.indices_offsets = []
		self.offset_list = []
		self.size = ''
		self.count = 0
		self.mesh_count = 0
		self.texture_list = []
		self.texture_count = 0
		self.mesh_descrs = []
		self.vxtable = []
		self.cols = []
		self.colcount = []
		self.v_bones_i = []
		self.v_bones_w = []
		self.itable = []
		self.ntable = []
		self.bboxtable = []
		self.uvs = []
		self.uvcount = []
		self.container_type = ''
		self.endianess = ''
		self.endian = ''
		self.bones = []
		self.props = []
		self.prop_list = []
		self.prop_positions = []
		self.prop_rotations = []
		self.prop_count = 0
		self.tex_names = []
		self.sub_names = []
		self.group_names = []
		self.group_list = []
		self.type = ''
		self.group_count = 0
		self.materials = []
		self.material_count = 0
		self.material_list = []
		self.material_dict = {}
		self.object_list = []
		self.mat_assign_table = []
		self.id = 0
		self.crowd = []
		self.collisions = []
		self.collision_list = []
		self.name = ''
		self.code = self.init_read(self.path, mode)
		self.logfile = fifa_tools.logfile

		print(f"RX3 Data File Object : {self.code}")

	def init_read(self, path, mode):
		# scn = bpy.context.scene
		scn = bpy.context.scene
		path, filename = os.path.split(path)
		filename, ext = os.path.splitext(filename)
		try:
			self.name = filename
			self.id = self.name.split('_')[1]
			self.type = self.name.split(sep='_')[0]
		except:
			return 'corrupt_filename'
		else:
			print('-------------------------------------------------------------------------------')
			print('FILE INITIALIZATION')
			print('FILE PATH: ', self.path)
			print('FILE TYPE: ', self.type)
			print('FILE ID:', self.id)
			print('FILE MODE:', mode)
			try:
				if mode:
					self.data = open(self.path, 'wb')
					return 'New RX3 Export'
				else:
					self.data = open(self.path, 'r+b')
					if str(self.data.read(8))[2:-1] == 'chunkzip':
						t = BytesIO()
						self.data.read(12)
						sec_num = struct.unpack('>I', self.data.read(4))[0]
						self.data.read(8)
						for i in range(sec_num):
							off = self.data.tell() % 4
							if off:
								self.data.read(4 - off)
							sec_found = False
							while 1:
								if not sec_found:
									sec_len = struct.unpack('>I', self.data.read(4))[0]
								if not sec_len == 0:
									sec_found = True
									continue

							self.data.read(4)
							data = self.data.read(sec_len)
							try:
								t.write(zlib.decompress(data, -15))
							except zlib.error:
								return 'corrupt_file'

						self.data = t
					self.data.seek(8)
					original_size = struct.unpack('<I', self.data.read(4))[0]
					f_size = len(self.data.read()) + 12
					if not original_size == f_size and ext == 'rx3' and self.type == 'stadium' and scn.game_enum in ('FIFA14','FIFA15'):
						e = open('fifa_tools\\scripts\\msg', 'r')
						print(e.read())
						print('                           I SEE WHAT YOU DID THERE')
						e.close()
						return 'file_copy'
					self.data.seek(0)
					return self
			except IOError as e:
				return 'io_error'

	def overwrite_geometry_data(self):
		# scn = bpy.context.scene
		scn = bpy.context.scene
		self.file_ident()
		self.read_file_offsets(dir)
		print('----------------------------')
		print('SEARCHING FOR ' + str(self.type).upper() + ' PARTS IN THE SCENE')
		progress = 0
		for i in range(len(self.mesh_offsets)):
			try:
				name = self.type + '_' + self.id + '_' + str(i)
				if self.type == 'head':
					name = name + '_' + self.sub_names[i]
				object = bpy.data.objects[name]
				progress += 1
				print('PROCESSING PART ', name)
			except KeyError:
				print('PART ', name, ' NOT FOUND')
				continue
			else:
				verts = []
				uvs = []
				cols = []
				indices = []
				opts = self.mesh_descr_convert(self.mesh_descrs[i])
				print(opts)
				verts, uvs, cols, indices = self.convert_original_mesh_to_data(object)
				self.data.seek(self.mesh_offsets[i][0] + 16)
				self.convert_mesh_to_bytes(opts, len(verts), verts, uvs, cols)
				if not scn.trophy_flag:
					self.data.seek(self.indices_offsets[i][0] + 16)
					self.write_indices(indices)
				print('----------------------------')
				print('OVERWRITTEN ', str(progress), '/', str(len(self.mesh_offsets)), ' PARTS \n')

		self.data.close()

	def convert_original_mesh_to_data(self, object):
		verts = []
		uvs = []
		indices = []
		cols = []
		data = object.data
		bm = bmesh.new()
		bm.from_mesh(data)
		uvs_0 = []
		uvs_1 = []
		uvs_2 = []
		uvs_3 = []
		uvs_4 = []
		uvs_5 = []
		uvs_6 = []
		uvs_7 = []
		col_0 = []
		col_1 = []
		col_2 = []
		uvcount = len(bm.loops.layers.uv)
		colcount = len(bm.loops.layers.color)
		rot_x_mat = Matrix.Rotation(radians(90), 4, 'X')
		scale_mat = Matrix.Scale(100, 4)
		
		if hasattr(bm.verts, "ensure_lookup_table"): 
			bm.verts.ensure_lookup_table()
			# only if you need to:
			# bm.edges.ensure_lookup_table()   
			# bm.faces.ensure_lookup_table()
		
		for vert in bm.verts:
			# For blender before 2.79
			# co = scale_mat * rot_x_mat * object.matrix_world * vert.co
			
			# For blender after 2.80
			co = scale_mat @ rot_x_mat @ object.matrix_world @ vert.co
			
			verts.append((co[0], -co[1], -co[2]))

		bm.verts.ensure_lookup_table()
		for i in range(len(bm.verts)):
			bm.verts.ensure_lookup_table()
			for j in range(uvcount):
				uvlayer = bm.loops.layers.uv[j]
				eval('uvs_' + str(j) + '.append((round(bm.verts[i].link_loops[0][uvlayer].uv.x,8),round(1-bm.verts[i].link_loops[0][uvlayer].uv.y,8)))')

		bm.verts.ensure_lookup_table()
		for i in range(len(bm.verts)):
			bm.verts.ensure_lookup_table()
			for j in range(colcount):
				collayer = bm.loops.layers.color[j]
				vert_data = bm.verts[i].link_loops[0][collayer]
				eval('col_' + str(j) + '.append((vert_data[0]*1023,vert_data[1]*1023,vert_data[2]*1023))')

		bm.faces.ensure_lookup_table()
		for f in bm.faces:
			bm.faces.ensure_lookup_table()
			indices.append((
			 f.verts[0].index, f.verts[1].index, f.verts[2].index))

		for j in range(uvcount):
			eval('uvs.append(uvs_' + str(j) + ')')

		for j in range(colcount):
			eval('cols.append(col_' + str(j) + ')')

		bm.free()
		return (
		 verts, uvs, cols, indices)

	def convert_mesh_to_bytes(self, opts, count, verts, uvs, cols):
		for i in range(count):
			for o in opts:
				if o[0] == 'p':
					if o[3:] == '4f16':
						gh.write_half_verts(self.data, verts[i])
					else:
						self.data.write(struct.pack('<3f', round(verts[i][0], 8), round(verts[i][1], 8), round(verts[i][2], 8)))
				elif o[0] == 'n':
					col = (int(cols[0][i][0]) << 20) + (int(cols[0][i][1]) << 10) + int(cols[0][i][2])
					self.data.write(struct.pack('<I', col))
				elif o[0] == 'g':
					col = (int(cols[1][i][0]) << 20) + (int(cols[1][i][1]) << 10) + int(cols[1][i][2])
					self.data.write(struct.pack('<I', col))
				elif o[0] == 'b':
					col = (int(cols[2][i][0]) << 20) + (int(cols[2][i][1]) << 10) + int(cols[2][i][2])
					self.data.write(struct.pack('<I', col))
				elif o[0] == 't':
					print(f'{o[1]}...{i}')
					huvx = eval('comp.compress(round(uvs[int(o[1])][i][0],8))')
					huvy = eval('comp.compress(round(uvs[int(o[1])][i][1],8))')
					self.data.write(struct.pack('<HH', huvx, huvy))
				elif o[0] == 'i':
					if o[3:] == '4u8':
						self.data.read(4)
					elif o[3:] == '4u16':
						self.data.read(8)
				elif o[0] == 'w':
					self.data.read(4)
					continue

	def read_file_offsets(self, dir):
		# scn = bpy.context.scene
		scn = bpy.context.scene
		print('READING FILE OFFSETS...')
		print(f"Offsets : {self.offsets}")
		log = open(self.logfile, 'a+')
		for offset in self.offsets:
			if offset[0] == 3263271920:
				self.read_mesh_descr(offset[1])
			elif offset[0] == 2047566042:
				self.read_texture(offset[1], dir)
				self.texture_count += 1
			elif offset[0] == 4034198449 and scn.collision_flag:
				self.read_collision(offset[1])
			elif offset[0] == 685399266:
				self.read_prop_positions(offset[1])
			elif offset[0] == 1285267122:
				self.read_props(offset[1], self.endian)
			elif offset[0] == 2116321516:
				log.write('Group Offset: ' + str(offset[1]))
				log.write('\n')
				self.read_group(offset[1])
				self.group_count += 1
			elif offset[0] == 230948820:
				self.read_group_names(offset[1])
			elif offset[0] == 123459928:
				self.create_material(offset[1], self.material_count)
				self.material_count += 1
			elif offset[0] == 5798132:
				if scn.trophy_flag:
					temp = gh.facereadstrip(self.data, offset[1], self.endian)
				else:
					temp = gh.facereadlist(self.data, offset[1], self.endian)
				self.itable.append(temp[0])
				#print(self.itable[0])
				print(f'Offset for Face/Indices : {offset[1]}')
				print(f'Indices Length : {temp[1]}')
				self.indices_offsets.append((offset[1], temp[1]))
				print(f"IndOff : {self.indices_offsets}")
			elif offset[0] == 3751472158:
				log.write('Bones Detected\n')
				self.data.seek(offset[1])
				size = struct.unpack(self.endian + 'I', self.data.read(4))[0]
				bc = struct.unpack(self.endian + 'I', self.data.read(4))[0]
				self.data.read(8)
				self.bones.append(self.read_bones(bc))
			elif offset[0] == 5798561 and scn.geometry_flag:
				self.data.seek(offset[1])
				self.data.read(4)
				vc = struct.unpack(self.endian + 'I', self.data.read(4))[0]
				chunk_length = struct.unpack(self.endian + 'I', self.data.read(4))[0]
				self.mesh_offsets.append([offset[1], chunk_length])
				count = len(self.mesh_offsets) - 1
				self.data.read(4)
				self.mesh_count += 1
				log.write('Mesh Count: %3d || Vert Count: %5d || Chunk Length: %2d || File Offset: %7d || Of Type: %s' % (
				 self.mesh_count, vc, chunk_length, offset[1], self.type))
				print(f'Mesh Description / Vertex Format : { self.mesh_descrs[count]}\nTotal Vertices Count:{vc}')
				temp = self.read_file_data(self.data, self.mesh_descrs[count], vc)
				#print(f"total uvs : {temp[2]}")
				self.vxtable.append(temp[0])
				self.cols.append(temp[1])
				self.colcount.append(len(temp[1]))
				self.uvs.append(temp[2])
				self.uvcount.append(len(temp[2]))
				self.v_bones_i.append(temp[3])
				self.v_bones_w.append(temp[4])
				log.write('\n')
				continue

		print('FILE OFFSETS READ SUCCESSFULLY')
		log.close()

	def file_ident(self):
		self.container_type, self.endianess, self.endian, self.size, self.offsets, self.count = self.file_ident_func()

	def file_ident_func(self):
		print('FILE IDENTIFICATION IN PROGRESS')
		offsets = []
		name = str(self.data.read(3))[2:-1]
		endian = str(self.data.read(1))[2:-1]
		#filesize = 0
		#mesh_count = 0
		if endian == 'b':
			endian = '>'
			endianstr = 'Big Endian'
		elif endian == 'l':
			endian = '<'
			endianstr = 'Little Endian'        
		# else:
		#     print('ENDIANNESS DETECTED: ', endianstr)
		#     self.data.read(4)
		#     filesize = struct.unpack(endian + 'I', self.data.read(4))[0]
		#     sect_num = struct.unpack(endian + 'I', self.data.read(4))[0]
		#     print('DESCRIPTIONS DETECTED: ', sect_num)
		#     for i in range(0, sect_num):
		#         offsets.append((
		#          struct.unpack(endian + 'I', self.data.read(4))[0], struct.unpack(endian + 'I', self.data.read(4))[0]))
		#         self.data.read(8)

		#     mesh_count = struct.unpack(endian + 'I', self.data.read(4))[0]
		#     print('MESH OBJECTS: ', mesh_count)
		print('ENDIANNESS DETECTED: ', endianstr)
		self.data.read(4)
		filesize = struct.unpack(endian + 'I', self.data.read(4))[0]
		sect_num = struct.unpack(endian + 'I', self.data.read(4))[0]
		print('DESCRIPTIONS DETECTED: ', sect_num)
		for i in range(0, sect_num):
			offsets.append((
				struct.unpack(endian + 'I', self.data.read(4))[0], struct.unpack(endian + 'I', self.data.read(4))[0]))
			self.data.read(8)

		mesh_count = struct.unpack(endian + 'I', self.data.read(4))[0]
		print('MESH OBJECTS: ', mesh_count)

		return (name, endianstr, endian, ('Total File Size:', round(filesize / 1024, 2), 'KBs'), offsets, mesh_count)

	def read_mesh_descr(self, offset):
		self.data.seek(offset)
		self.data.read(4)
		length = struct.unpack(self.endian + 'i', self.data.read(4))[0]
		self.data.read(8)
		descr_str = ''
		list = []
		temp = []
		part = ''
		vflag = 0
		uvcount = 0
		cols = 0
		bones_i = False
		bones_w = False
		for i in self.data.read(length):
			if i == 32 or i == 0:
				temp.append(part)
				list.append(temp)
				temp = []
				part = ''
			elif i == 58:
				temp.append(part)
				part = ''
			else:
				part = part + chr(i)

		self.mesh_descrs.append(list)

	def read_file_data(self, f, opts, count):
		uvcount = 0
		colcount = 0
		verts = []
		uvs = []
		cols = []
		cols_0 = []
		cols_1 = []
		cols_2 = []
		uvs_0, uvs_1, uvs_2, uvs_3, uvs_4, uvs_5, uvs_6, uvs_7 = ([], [], [], [], [], [], [], [])
		bones_i0 = []
		bones_i1 = []
		bones_w = []
		bones_c = []
		for i in range(count):
			uvcount = 0
			colcount = 0
			for j in opts:
				if j[0][0] == 'p':
					if j[4] == '3f32':
						verts.append(gh.read_vertices_1(f))
					elif j[4] == '4f16':
						verts.append(gh.read_vertices_0(f))
				elif j[0][0] == 't':
					if j[4] == '2f32':
						eval('uvs_' + str(j[0][1]) + '.append(gh.read_uvs_1(f))')
					elif j[4] == '2f16':
						eval('uvs_' + str(j[0][1]) + '.append(gh.read_uvs_0(f))')
					# else:
					# 	uvcount += 1
					uvcount += 1

				elif j[0][0] == 'n':
					colcount += 1
					cols_0.append(gh.read_cols(f))
				elif j[0][0] == 'b':
					colcount += 1
					cols_2.append(gh.read_cols(f))
				elif j[0][0] == 'g':
					colcount += 1
					cols_1.append(gh.read_cols(f))
				elif j[0][0] == 'i':
					if j[4] == '4u8':
						eval('bones_i' + str(j[0][1]) + ".append(struct.unpack('<4B',f.read(4)))")
					elif j[4] == '4u16':
						eval('bones_i' + str(j[0][1]) + ".append(struct.unpack('<4H',f.read(8)))")
				elif j[0][0] == 'w':
					bones_w.append(struct.unpack('<4B', f.read(4)))
				elif j[0][0] == 'c':
					bones_c.append(struct.unpack('<4B', f.read(4)))
					continue

		for j in range(uvcount):
			eval('uvs.append(uvs_' + str(j) + ')')

		for j in range(colcount):
			eval('cols.append(cols_' + str(j) + ')')

		return (
		 verts, cols, uvs, bones_i0, bones_w)

	def mesh_descr_convert(self, descr):
		opts = []
		for i in descr:
			opts.append(i[0] + ':' + i[4])

		return opts

	def read_props(self, offset, endian):
		self.data.seek(offset)
		self.data.read(4)
		count = struct.unpack(endian + 'i', self.data.read(4))[0]
		self.data.read(8)
		print('READING PROPS', 'COUNT: ', count)
		if self.type.endswith('_texture'):
			for i in range(count):
				self.tex_names.append('')

			for i in range(count):
				self.data.read(4)
				textlen = struct.unpack(endian + 'i', self.data.read(4))[0]
				text = ''
				for j in range(textlen):
					text = text + chr(struct.unpack(endian + 'B', self.data.read(1))[0])

				text = text[0:-1]
				try:
					path = os.path.join(fifa_tools.texdir , 'texture_' + str(i) + '.dds')
					destpath = os.path.join(fifa_tools.texdir , text + '.dds')
					
					if os.path.exists(destpath):
						print('[WARNING] Image File Exists')
						print('[WARNING] Deleting Previous Image File')
						os.remove(destpath)

					os.rename(path, destpath)
					print('Renaming texture_' + str(i) + '.dds to ' + text + '.dds')
					self.tex_names[i] = text + '.dds'
				except FileNotFoundError:
					print('Unsupported Image File')

		else:
			for i in range(count):
				off = struct.unpack(endian + 'I', self.data.read(4))[0]
				textlen = struct.unpack(endian + 'I', self.data.read(4))[0]
				text = ''
				for j in range(textlen):
					text = text + chr(struct.unpack(endian + 'B', self.data.read(1))[0])

				text = text[0:-1]
				if off == 685399266:
					self.props.append(text)
					self.prop_count += 1
				elif off == 0xD48D7880:
					self.sub_names.append(text.split(sep='.')[0].split(sep='_')[0])
				elif off == 2047566042:
					self.tex_names.append(text + '.dds')
					continue

	def read_prop_positions(self, offset):
		self.data.seek(offset)
		self.data.read(4)
		temp = struct.unpack('<3f', self.data.read(12))
		rot = struct.unpack('<3f', self.data.read(12))
		self.prop_positions.append((
		 0.01 * temp[0], -0.01 * temp[2], 0.01 * temp[1]))
		self.prop_rotations.append((rot[0], rot[1], rot[2]))

	def read_bones(self, count):
		temp = []
		for k in range(count):
			mat = Matrix()
			mat = mat.to_4x4()
			for i in range(4):
				for j in range(4):
					mat[j][i] = round(struct.unpack('<f', self.data.read(4))[0], 8)

			pos = Vector((mat[0][3], mat[1][3], mat[2][3]))
			if k in (2, 3, 4, 324, 333):
				print("Reading Bones...")
				print('Matrix ID : ', k)
				print(pos)
			rot = mat.to_euler()
			if not rot[0] == 0:
				sx = round(rot[0] / abs(rot[0]), 1)
			else:
				sx = 1.0
			if not rot[1] == 0:
				sy = round(rot[1] / abs(rot[1]), 1)
			else:
				sy = 1.0
			if not rot[2] == 0:
				sz = round(rot[2] / abs(rot[2]), 1)
			else:
				sz = 1.0
			axis, roll = gh.mat3_to_vec_roll(mat.to_3x3())
			if k in (2, 3, 4, 324, 333):
				print(sz)
				print(pos)
			temp.append((pos, pos + axis, roll))

		return temp

	def read_texture(self, offset, path):
		print('Seeking to texture offset: ', offset)
		self.data.seek(offset)
		overall_size = struct.unpack(self.endian + 'I', self.data.read(4))[0]
		self.data.read(1)
		identifier = struct.unpack(self.endian + 'B', self.data.read(1))[0]
		self.data.read(2)
		width = struct.unpack(self.endian + 'H', self.data.read(2))[0]
		height = struct.unpack(self.endian + 'H', self.data.read(2))[0]
		self.data.read(2)
		mipmaps = struct.unpack(self.endian + 'H', self.data.read(2))[0]
		print('Texture Information: ', width, height, mipmaps, identifier)
		self.data.read(8)
		size = struct.unpack(self.endian + 'I', self.data.read(4))[0]
		self.data.read(4)
		if identifier == 0:
			data = tex_gh.read_dds_header(0)
			string = 'DXT1'
		elif identifier == 1:
			data = tex_gh.read_dds_header(0)
			data[87] = 51
			string = 'DXT3'
		elif identifier == 2:
			data = tex_gh.read_dds_header(144)
			string = 'DXT5'
		elif identifier == 7:
			data = tex_gh.read_dds_header(288)
			string = 'NVTT'
		else:
			print('NOT RECOGNISABLE IMAGE FILE')
			return
		data[12] = height.to_bytes(2, 'little')[0]
		data[13] = height.to_bytes(2, 'little')[1]
		data[16] = width.to_bytes(2, 'little')[0]
		data[17] = width.to_bytes(2, 'little')[1]
		data[28] = mipmaps.to_bytes(1, 'little')[0]
		path = os.path.join(fifa_tools.texdir , 'texture_' + str(self.texture_count) + '.dds')
		tf = open(path, 'wb')
		[tf.write(b) for b in [struct.pack('<B', x) for x in data]]
		for i in range(mipmaps):
			print('Mipmap offset: ', self.data.tell(), 'Size: ', size)
			tf.write(self.data.read(size))
			self.data.read(8)
			size = struct.unpack(self.endian + 'I', self.data.read(4))[0]
			self.data.read(4)

		tf.close()

	def create_material(self, offset, count):
		self.data.seek(offset)
		self.data.read(4)
		tex_num = struct.unpack(self.endian + 'i', self.data.read(4))[0]
		self.data.read(8)
		entry = []
		mat_name = gh.read_string(self.data) + '_' + str(count)
		for i in range(tex_num):
			texture_type = gh.read_string(self.data)
			tex_id = struct.unpack('<i', self.data.read(4))[0]
			texture_name = texture_type + '_' + str(tex_id)
			try:
				entry.append((
				 texture_name, self.tex_names[tex_id]))
				#  texture_name, fifa_tools.texdir + '\\' + self.tex_names[tex_id]))
			except:
				entry.append((
				 texture_name, '\\texture_' + str(tex_id)))
				#  texture_name, fifa_tools.texdir + '\\texture_' + str(tex_id)))

		self.materials.append((mat_name, entry))
		return {
		 'FINISHED'}

	def read_group(self, offset):
		# scn = bpy.context.scene
		scn = bpy.context.scene
		name = 'group_' + str(self.group_count)
		self.data.seek(offset)
		self.data.read(4)
		group_status = struct.unpack(self.endian + 'I', self.data.read(4))[0]
		if not group_status:
			return
		self.data.read(72)
		vec1 = Vector((struct.unpack(self.endian + 'f', self.data.read(4))[0],
		 struct.unpack(self.endian + 'f', self.data.read(4))[0], struct.unpack(self.endian + 'f', self.data.read(4))[0]))
		self.data.read(4)
		vec2 = Vector((struct.unpack(self.endian + 'f', self.data.read(4))[0],
		 struct.unpack(self.endian + 'f', self.data.read(4))[0], struct.unpack(self.endian + 'f', self.data.read(4))[0]))
		self.data.read(4)
		group_items = struct.unpack(self.endian + 'i', self.data.read(4))[0]
		self.data.read(4)
		if scn.geometry_flag:
			gh.create_boundingbox(vec1, vec2, name)
		for i in range(group_items):
			ivec1 = Vector((struct.unpack(self.endian + 'f', self.data.read(4))[0],
			 struct.unpack(self.endian + 'f', self.data.read(4))[0], struct.unpack(self.endian + 'f', self.data.read(4))[0]))
			self.data.read(4)
			ivec2 = Vector((struct.unpack(self.endian + 'f', self.data.read(4))[0],
			 struct.unpack(self.endian + 'f', self.data.read(4))[0], struct.unpack(self.endian + 'f', self.data.read(4))[0]))
			self.data.read(4)
			self.bboxtable.append((ivec1, ivec2))
			part_id = struct.unpack(self.endian + 'i', self.data.read(4))[0]
			render_line = struct.unpack(self.endian + 'i', self.data.read(4))[0]
			self.mat_assign_table.append((
			 part_id, render_line, self.group_count))

	def read_group_names(self, offset):
		self.data.seek(offset)
		self.data.read(16)
		group_name = gh.read_string(self.data)
		self.group_names.append(group_name)

	def read_collision(self, offset):
		self.data.seek(offset)
		self.data.read(16)
		name = gh.read_string(self.data)
		self.data.read(4)
		triscount = struct.unpack('<I', self.data.read(4))[0]
		indices = []
		verts = []
		j = 0
		for i in range(triscount):
			for k in range(3):
				temp = struct.unpack('<3f', self.data.read(12))
				verts.append((temp[0] / 100, -temp[2] / 100, temp[1] / 100))

			indices.append((j, j + 1, j + 2))
			j += 3

		self.collisions.append((name, verts, indices))

	def write_offsets_to_file(self):
		size = 0
		for off in self.offset_list:
			size += off[2] + 16

		self.data.write(struct.pack('<4I', 1815304274, 4, size + 16, len(self.offset_list)))
		for i in self.offset_list:
			self.data.write(struct.pack('<4I', i[0], i[1], i[2], 0))

	def write_offset_data_to_file(self, path):
		object_count = len(self.object_list)
		texture_count = len(self.texture_list)
		for i in range(len(self.offset_list)):
			self.data.seek(self.offset_list[i][1])
			if self.offset_list[i][0] == 582139446:
				self.data.write(struct.pack('<4I', object_count, 0, 0, 0))
				for j in range(object_count):
					if self.object_list[j].vertsCount > 65535:
						ind_size = 4
					else:
						ind_size = 2
					self.data.write(struct.pack('<4I', gh.size_round(self.object_list[j].indicesCount * ind_size + 16), self.object_list[j].indicesCount, ind_size, 0))

			elif self.offset_list[i][0] == 3263271920:
				id = self.offset_list[i][3]
				self.data.write(struct.pack('<4I', self.offset_list[i][2], len(self.object_list[id].meshDescr) + 1, 0, 0))
				s = bytes(self.object_list[id].meshDescr, 'utf-8')
				self.data.write(s)
			elif self.offset_list[i][0] == 685399266:
				id = self.offset_list[i][3]
				self.data.write(struct.pack('<Ifff', self.offset_list[i][2], self.prop_list[id][1][0], self.prop_list[id][1][1], self.prop_list[id][1][2]))
				self.data.write(struct.pack('<fffI', self.prop_list[id][2][0], self.prop_list[id][2][1], self.prop_list[id][2][2], 0))
			elif self.offset_list[i][0] == 1285267122:
				self.data.write(struct.pack('<4I', self.offset_list[i][2], len(self.prop_list) + len(self.texture_list) + len(self.object_list), 0, 0))
				for j in range(len(self.prop_list)):
					self.data.write(struct.pack('<2I', 685399266, len(self.prop_list[j][0]) + 1))
					s = bytes(self.prop_list[j][0], 'utf-8')
					self.data.write(s)
					self.data.write(bytes('\x00' ,encoding = 'utf-8'))
					# self.data.write(hex(00))

				for j in range(len(self.object_list)):
					self.data.write(struct.pack('<2I', 3566041216, len(self.object_list[j].name) + 1))
					s = bytes(self.object_list[j].name, 'utf-8')
					self.data.write(s)
					self.data.write(bytes('\x00' ,encoding = 'utf-8'))
					# self.data.write(hex(00))

				for j in range(len(self.texture_list)):
					self.data.write(struct.pack('<I', 2047566042))
					print(self.texture_list[j])
					if type(self.texture_list[j]) == type(''):
						s = bytes(self.texture_list[j], 'utf-8')
						self.data.write(struct.pack('<I', len(self.texture_list[j]) + 1))
					elif type(self.texture_list[j][0]) == type(''):
						s = bytes(self.texture_list[j][0], 'utf-8')
						self.data.write(struct.pack('<I', len(self.texture_list[j][0]) + 1))
					else:
						self.data.write(s)
						self.data.write(bytes('\x00' ,encoding = 'utf-8')) 
						# self.data.write(hex(00)) 

			elif self.offset_list[i][0] == 5798132:
				id = self.offset_list[i][3]
				if self.object_list[id].vertsCount > 65535:
					ind_size = 4
				else:
					ind_size = 2
				self.data.write(struct.pack('<4I', gh.size_round(self.object_list[id].indicesCount * ind_size + 16), self.object_list[id].indicesCount, ind_size, 0))
				self.write_indices(self.object_list[id].indices)
			elif self.offset_list[i][0] == 5798561:
				id = self.offset_list[i][3]
				self.data.write(struct.pack('<4I', self.offset_list[i][2], self.object_list[id].vertsCount, self.object_list[id].chunkLength, 1))
				self.convert_mesh_to_bytes(self.object_list[id].meshDescrShort, self.object_list[id].vertsCount, self.object_list[id].verts, self.object_list[id].uvs, self.object_list[id].colors)
			elif self.offset_list[i][0] == 3566041216:
				self.data.write(struct.pack('<4I', 4, 0, 0, 0))
			elif self.offset_list[i][0] == 230948820:
				id = self.offset_list[i][3]
				data = self.data.write(struct.pack('<4I', self.offset_list[i][2], 1, 0, 0))
				if id >= len(self.group_list):
					s = bytes('CollisionGeometry', 'utf-8')
					data += self.data.write(s)
					data += self.data.write(bytes('\x00' ,encoding = 'utf-8'))
					# data += self.data.write(hex(00))
					data += self.data.write(struct.pack('B', id))
				else:
					s = bytes(self.group_list[id][0][5:], 'utf-8')
					self.data.write(s)
					self.data.write(bytes('\x00' ,encoding = 'utf-8'))
					# self.data.write(hex(00))
					self.data.write(struct.pack('B', id))
			elif self.offset_list[i][0] == 123459928:
				id = self.offset_list[i][3]
				self.data.write(struct.pack('<4I', self.offset_list[i][2], len(self.material_dict[self.material_list[id]][3]), 0, 0))
				s = bytes(self.material_dict[self.material_list[id]][1], 'utf-8')
				self.data.write(s)
				self.data.write(bytes('\x00' ,encoding = 'utf-8'))
				# self.data.write(hex(00))
				for j in range(len(self.material_dict[self.material_list[id]][2])):
					s = bytes(self.material_dict[self.material_list[id]][3][j], 'utf-8')
					self.data.write(s)
					self.data.write(bytes('\x00' ,encoding = 'utf-8'))
					# self.data.write(hex(00))
					self.data.write(struct.pack('I', self.texture_list.index(self.material_dict[self.material_list[id]][2][j])))

			elif self.offset_list[i][0] == 2116321516:
				id = self.offset_list[i][3]
				self.data.write(struct.pack('<4I', self.offset_list[i][2], 1, 4294967295, 0))
				self.data.write(struct.pack('<4f', 1, 0, 0, 0))
				self.data.write(struct.pack('<4f', 0, 1, 0, 0))
				self.data.write(struct.pack('<4f', 0, 0, 1, 0))
				self.data.write(struct.pack('<4f', 0, 0, 0, 1))
				self.data.write(struct.pack('<4f', self.group_list[id][1][0], self.group_list[id][1][1], self.group_list[id][1][2], 1))
				self.data.write(struct.pack('<4f', self.group_list[id][2][0], self.group_list[id][2][1], self.group_list[id][2][2], 1))
				self.data.write(struct.pack('<2I', self.group_list[id][3], 4294967295))
				object_offset = self.group_list[id][4]
				for j in range(self.group_list[id][3]):
					self.data.write(struct.pack('<4f', self.object_list[(object_offset + j)].boundBox[0][0], self.object_list[(object_offset + j)].boundBox[0][1], self.object_list[(object_offset + j)].boundBox[0][2], 1))
					self.data.write(struct.pack('<4f', self.object_list[(object_offset + j)].boundBox[1][0], self.object_list[(object_offset + j)].boundBox[1][1], self.object_list[(object_offset + j)].boundBox[1][2], 1))
					self.data.write(struct.pack('<2I', object_offset + j, self.object_list[(object_offset + j)].material))

			elif self.offset_list[i][0] == 4034198449:
				id = self.offset_list[i][3]
				self.data.write(struct.pack('4I', self.offset_list[i][2], 1, 0, 0))
				s = bytes(self.collision_list[id][2], 'utf-8')
				self.data.write(s)
				self.data.write(bytes('\x00' ,encoding = 'utf-8'))
				# self.data.write(hex(00))
				self.data.write(struct.pack('I', 1))
				self.data.write(struct.pack('I', self.collision_list[id][0]))
				for i in range(len(self.collision_list[id][1])):
					self.data.write(struct.pack('<3f', self.collision_list[id][1][i][0], self.collision_list[id][1][i][1], self.collision_list[id][1][i][2]))

			elif self.offset_list[i][0] == 1808827868:
				self.data.write(struct.pack('<4I', texture_count, 0, 0, 0))
				id = 0
				for tex in self.texture_list:
					if tex[7] == 'DXT5':
						id = 2
					self.data.write(struct.pack('<IBBHHHHH', tex[6], 1, id, 1, tex[3], tex[4], 1, tex[5]))

			elif self.offset_list[i][0] == 2047566042:
				id = self.offset_list[i][3]
				ext_len = len(self.texture_list[id][1].split(sep=os.sep)[(-1)].split(sep='.')[(-1)])
				t = open(self.texture_list[id][1], 'rb')
				divider = 1
				comp_id = 0
				w = self.texture_list[id][3]
				h = self.texture_list[id][4]
				phys_size = w * h
				mipmaps = self.texture_list[id][5]
				if self.texture_list[id][7] == 'DXT1':
					divider = 2
				if self.texture_list[id][7] == 'DXT5':
					comp_id = 2
				t.seek(128)
				print('Writing Texture: ', self.texture_list[id][1], w, h, mipmaps)
				self.data.write(struct.pack('<IBBHHHHH', self.texture_list[id][6], 1, comp_id, 1, self.texture_list[id][3], self.texture_list[id][4], 1, self.texture_list[id][5]))
				for j in range(mipmaps):
					tw = w * h // divider
					pitch = w * 4 // divider
					self.data.write(struct.pack('<4I', pitch, tw // pitch, tw, 0))
					self.data.write(t.read(tw))
					w = max(w // 2, 4)
					h = max(h // 2, 4)

				t.close()
				continue

	def write_offsets(self, data_pass):
		object_count = len(self.object_list)
		material_count = len(self.material_list)
		group_count = len(self.group_list)
		prop_count = len(self.prop_list)
		collision_count = len(self.collision_list)
		#scn = bpy.context.scene
		scn = bpy.context.scene
		if data_pass == 0:
			self.offset_list.append([582139446, 0, 0])
			for i in range(object_count):
				self.offset_list.append([3263271920, 0, 0, i])

			self.offset_list.append([1285267122, 0, 0])
			for i in range(object_count):
				self.offset_list.append([5798132, 0, 0, i])

			if scn.face_edit_head_flag:
				for i in range(object_count):
					self.offset_list.append([255353250, 0, 0, i])

			for i in range(object_count):
				self.offset_list.append([5798561, 0, 0, i])

			if scn.face_edit_head_flag:
				for i in range(object_count):
					self.offset_list.append([3751472158, 0, 0, i])

			for i in range(object_count):
				self.offset_list.append([3566041216, 0, 0, i])

			if scn.stadium_export_flag:
				for i in range(prop_count):
					self.offset_list.append([685399266, 0, 0, i])

				for i in range(collision_count):
					self.offset_list.append([4034198449, 0, 0, i])

				for i in range(material_count):
					self.offset_list.append([123459928, 0, 0, i])

				for i in range(group_count):
					self.offset_list.append([2116321516, 0, 0, i])

				for i in range(group_count + 1):
					self.offset_list.append([230948820, 0, 0, i])

		elif data_pass == 1:
			table_size = len(self.offset_list)
			for i in range(table_size):
				if i == 0:
					self.offset_list[i][1] = table_size * 16 + 16
				else:
					self.offset_list[i][1] = self.offset_list[(i - 1)][1] + self.offset_list[(i - 1)][2]
				if self.offset_list[i][0] == 582139446:
					self.offset_list[i][2] = 16 + len(self.object_list) * 16
				elif self.offset_list[i][0] == 1285267122:
					size = 16
					for j in range(len(self.prop_list)):
						size += len(self.prop_list[j][0]) + 1 + 8

					for j in range(len(self.object_list)):
						size += len(self.object_list[j].name) + 1 + 8

					for j in range(len(self.texture_list)):
						size += len(self.texture_list[j]) + 1 + 8

					self.offset_list[i][2] = gh.size_round(size)
				elif self.offset_list[i][0] == 3263271920:
					id = self.offset_list[i][3]
					self.offset_list[i][2] = gh.size_round(len(self.object_list[id].meshDescr) + 1 + 16)
				elif self.offset_list[i][0] == 5798132:
					id = self.offset_list[i][3]
					if self.object_list[id].vertsCount > 65535:
						ind_size = 4
					else:
						ind_size = 2
					self.offset_list[i][2] = gh.size_round(self.object_list[id].indicesCount * ind_size + 16)
				elif self.offset_list[i][0] == 5798561:
					id = self.offset_list[i][3]
					self.offset_list[i][2] = gh.size_round(16 + self.object_list[id].vertsCount * self.object_list[id].chunkLength)
				elif self.offset_list[i][0] == 3566041216:
					self.offset_list[i][2] = 16
				elif self.offset_list[i][0] == 4034198449:
					id = self.offset_list[i][3]
					self.offset_list[i][2] = gh.size_round(16 + len(self.collision_list[id][2]) + 1 + 4 + self.collision_list[id][0] * 3 * 12)
				elif self.offset_list[i][0] == 685399266:
					self.offset_list[i][2] = 32
				elif self.offset_list[i][0] == 123459928:
					id = self.offset_list[i][3]
					self.offset_list[i][2] = self.material_dict[self.material_list[id]][4]
				elif self.offset_list[i][0] == 230948820:
					id = self.offset_list[i][3]
					try:
						self.offset_list[i][2] = gh.size_round(16 + len(self.group_list[id][0][5:]) + 5)
					except IndexError:
						self.offset_list[i][2] = 48

				elif self.offset_list[i][0] == 2116321516:
					id = self.offset_list[i][3]
					self.offset_list[i][2] = gh.size_round(120 + self.group_list[id][3] * 40)
					continue

	def write_indices(self, indices):
		if 3 * len(indices) > 65535:
			ind_size = 4
			format = '<III'
		else:
			ind_size = 2
			format = '<HHH'
		for entry in indices:
			self.data.write(struct.pack(format, entry[0], entry[1], entry[2]))


def write_textures_to_file(textures_list, type, id):
	#scn = bpy.context.scene
	scn = bpy.context.scene
	if type == 'face':
		f_name = 'face_' + str(id) + '_0_0_0_0_0_0_0_0_textures.rx3'
	elif type == 'eyes':
		f_name = 'eyes_' + str(id) + '_0_textures.rx3'
	elif type == 'hair':
		f_name = 'hair_' + str(id) + '_0_textures.rx3'
	elif type == 'stadium':
		f_name = 'stadium_' + str(id) + '_' + scn.stadium_version + '_textures.rx3'
	else:
		f_name = type + '_' + str(id) + '_textures.rx3'
	f = fifa_rx3(scn.export_path + f_name, 1)
	#scn = bpy.context.scene
	scn = bpy.context.scene
	status = texture_convert(textures_list)
	print('Total Number of textures: ', len(textures_list))
	if status.split(sep=',')[0] == 'texture_path_error':
		return 'missing_texture_file'
	f.offset_list, f.texture_list = read_converted_textures(f.offset_list, textures_list, fifa_tools.texdir + '\\')
	[print(i) for i in f.texture_list]
	try:
		f.write_offsets_to_file()
		f.write_offset_data_to_file(fifa_tools.texdir + '\\')
	except:
		print(sys.exc_info()[0])
		print('ERROR ON TEXTURE WRITING')
		f.data.close()
		return 'error'
	else:
		f.data.seek(f.offset_list[(-1)][1])
		f.data.seek(f.offset_list[(-1)][2], 1)
		s = bytes(sig, 'utf-8')
		f.data.write(s)
		f.data.close()
		print(f.offset_list)
	return 'success'


def read_converted_textures(offset_list, textures_list, path):
	offset_list.append((
	 1808827868, len(textures_list) * 16 + 48, len(textures_list) * 16 + 16))
	for k in range(len(textures_list)):
		print('Reading: ', textures_list[k][1])
		ext_len = len(textures_list[k][1].split(sep='\\')[(-1)].split(sep='.')[(-1)])
		t = open(textures_list[k][1], 'rb')
		width, height, mipmaps, textype = tex_gh.read_dds_info(t)
		textures_list[k][3], textures_list[k][4], textures_list[k][5], textures_list[k][7] = (
		 width, height, mipmaps, textype)
		t.close()
		print(width, height, mipmaps, textype)
		phys_size = width * height
		divider = 1
		if textype == 'DXT1':
			divider = 2
		size = 0
		for i in range(mipmaps):
			size = size + width * height // divider + 16
			width = max(width // 2, 4)
			height = max(height // 2, 4)

		textures_list[k][6] = gh.size_round(size + 16)
		offset_list.append((
		 2047566042, offset_list[(-1)][1] + offset_list[(-1)][2], textures_list[k][6], k))

	size = 16
	for i in range(len(textures_list)):
		size = size + len(textures_list[i][0]) + 9

	offset_list.append((
	 1285267122, offset_list[(-1)][1] + offset_list[(-1)][2], gh.size_round(size)))
	return (
	 offset_list, textures_list)


def crowd_seat_align(align_vector):
	# scn = bpy.context.scene
	scn = bpy.context.scene
	ob = bpy.context.object
	bm = bmesh.from_edit_mesh(ob.data)
	for f in bm.faces:
		if f.select:
			base = gh.face_center(f)
			if align_vector == Vector((0, 0, 0)):
				align_vector = ob.matrix_world.inverted() * (scn.cursor_location - ob.matrix_world * base)
				align_vector = Vector((align_vector[0], align_vector[1]))
			angle = Vector((f.normal[0], f.normal[1])).angle_signed(align_vector)
			rot_mat = Matrix.Rotation(round(-angle, 2), 4, 'Z')
			for v in f.verts:
				v.co = v.co - base
				v.co = rot_mat * v.co
				v.co = v.co + base

			continue

	bm.normal_update()
	bmesh.update_edit_mesh(ob.data, False)


def crowd_seat_create(v_num, h_num, v_dist, h_dist, gap, context):
	# scn = context.scene
	scn = bpy.context.scene
	found_crowd = False
	if context.mode == 'EDIT_MESH':
		ob = context.object
		bm = bmesh.from_edit_mesh(ob.data)
		found_object = ob
		print(found_object)
	else:
		bm = bmesh.new()
		# for ob in scn.objects:
		for ob in scn.collection.objects:
			if ob.name == 'crowd':
				found_object = ob
				bm.from_mesh(ob.data)
				found_crowd = True
				break

	cursor_loc = Vector((
	 scn.cursor_location[0], scn.cursor_location[1], scn.cursor_location[2]))
	val = 0.1
	for i in range(v_num):
		for j in range(h_num):
			bm.faces.new((bm.verts.new(Vector((cursor_loc[0] + val, cursor_loc[1] + val, cursor_loc[2] - val))),
			 bm.verts.new(Vector((cursor_loc[0] - val, cursor_loc[1] + val, cursor_loc[2] - val))),
			 bm.verts.new(Vector((cursor_loc[0] - val, cursor_loc[1] - val, cursor_loc[2] + val))),
			 bm.verts.new(Vector((cursor_loc[0] + val, cursor_loc[1] - val, cursor_loc[2] + val)))))
			cursor_loc[0] -= h_dist * val

		cursor_loc[0] = scn.cursor_location[0]
		cursor_loc[1] += gap * val
		cursor_loc[2] -= v_dist * val

	bm.normal_update()
	if not found_crowd and context.mode == 'OBJECT':
		me = bpy.data.meshes.new('crowd')
		bm.to_mesh(me)
		ob = bpy.data.objects.new('crowd', me)
		# context.scene.objects.link(ob)
		# scn.objects.link(ob)
		scn.collection.objects.link(ob)
	elif found_crowd:
		bm.to_mesh(found_object.data)
	elif context.mode == 'EDIT_MESH':
		bmesh.update_edit_mesh(found_object.data)
	bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)


def crowd_groups(name):
	# scn = bpy.context.scene
	scn = bpy.context.scene
	ob = bpy.context.object
	bm = bmesh.from_edit_mesh(ob.data)
	vxlist = []
	for v in bm.verts:
		if v.select == True:
			vxlist.append(v.index)
			continue

	bm.free()
	bpy.ops.object.editmode_toggle()
	flag = False
	while not flag:
		if name in ob.vertex_groups:
			name = name[:-1] + str(int(name[(-1)]) + 1)
		else:
			ob.vertex_groups.new(name)
			flag = True

	for g in ob.vertex_groups:
		if g.name == name:
			ob.vertex_groups[name].add(vxlist, 1, 'ADD')
		else:
			ob.vertex_groups[g.name].add(vxlist, 1, 'SUBTRACT')


def convert_mesh_init(object, mode):
	# scn = bpy.context.scene
	scn = bpy.context.scene
	verts = []
	norms = []
	uvs = []
	cols = []
	indices = []
	collist = []
	data = object.data
	print('Processing: ', object.name)
	bm = bmesh.new()
	bm.from_mesh(data)
	bm.normal_update()
	if mode == 0:
		mesh_descr = ''
		mesh_descr_short = []
		boundbox = gh.object_bbox(object)
		off = 0
		last = 0
		chunk_length = 0
		mesh_descr = 'p0:' + '{:02X}'.format(off) + ':00:0001:3f32' + ' '
		mesh_descr_short.append('p0:3f32')
		uvlen = len(bm.loops.layers.uv)
		for i in range(len(bm.loops.layers.color)):
			collist.append(bm.loops.layers.color[i].name)

		off += 12
		if len(collist) >= 1:
			mesh_descr += 'n0:' + '{:02X}'.format(off) + ':00:0001:3s10n' + ' '
			mesh_descr_short.append('n0:3s10n')
			off += 4
		if len(collist) >= 2:
			mesh_descr += 'g0:' + '{:02X}'.format(off) + ':00:0001:3s10n' + ' '
			mesh_descr_short.append('g0:3s10n')
			off += 4
		for i in range(uvlen):
			mesh_descr += 't' + str(i) + ':' + '{:02X}'.format(off) + ':00:0001:2f16' + ' '
			mesh_descr_short.append('t' + str(i) + ':2f16')
			off += 4

		if object.name.split(sep='_')[0] in ('head', 'hair'):
			mesh_descr += 'i0:' + '{:02X}'.format(off) + ':00:0001:4u8' + ' '
			mesh_descr_short.append('i0:4u8')
			off += 4
			mesh_descr += 'w0:' + '{:02X}'.format(off) + ':00:0001:4u8' + ' '
			mesh_descr_short.append('w0:4u8')
			off += 4
		if len(collist) >= 3:
			mesh_descr += 'b0:' + '{:02X}'.format(off) + ':00:0001:3s10n' + ' '
			mesh_descr_short.append('b0:3s10n')
			off += 4
		mesh_descr = mesh_descr[0:-1]
		print(mesh_descr_short)
		bm.free()
		return (
		 collist, boundbox, mesh_descr, mesh_descr_short, off - last)
	if mode == 1:
		uvs_0 = []
		uvs_1 = []
		uvs_2 = []
		col_0 = []
		col_1 = []
		col_2 = []
		id = 0
		object_matrix_wrld = object.matrix_world
		rot_x_mat = Matrix.Rotation(radians(-90), 4, 'X')
		scale_mat = Matrix.Scale(100, 4)
		# data.update(calc_tessface=True)
		data.update(calc_edges=True, calc_edges_loose=True)
		uvcount = len(data.uv_layers)
		colcount = len(data.vertex_colors)
		# for f in data.tessfaces:
		for f in data.loop_triangles:
			if len(f.vertices) == 4:
				indices.append((id, id + 1, id + 2))
				indices.append((id + 3, id, id + 2))
				id += 4
			else:
				indices.append((id, id + 1, id + 2))
				id += 3
			for vert in range(len(f.vertices)):
				co = scale_mat * rot_x_mat * object_matrix_wrld * data.vertices[f.vertices[vert]].co
				norm = scale_mat * rot_x_mat * object_matrix_wrld * data.vertices[f.vertices[vert]].normal
				verts.append((co[0], co[1], co[2]))
				norms.append((norm[0], norm[1], norm[2]))
				for k in range(uvcount):
					u = eval('data.tessface_uv_textures[' + str(k) + '].data[' + str(f.index) + '].uv' + str(vert + 1) + '[0]')
					v = 1 - eval('data.tessface_uv_textures[' + str(k) + '].data[' + str(f.index) + '].uv' + str(vert + 1) + '[1]')
					eval('uvs_' + str(k) + '.append((round(u,8),round(v,8)))')

				for k in range(colcount):
					r = eval('data.tessface_vertex_colors[' + str(k) + '].data[' + str(f.index) + '].color' + str(vert + 1) + '[0]*1023')
					g = eval('data.tessface_vertex_colors[' + str(k) + '].data[' + str(f.index) + '].color' + str(vert + 1) + '[1]*1023')
					b = eval('data.tessface_vertex_colors[' + str(k) + '].data[' + str(f.index) + '].color' + str(vert + 1) + '[2]*1023')
					eval('col_' + str(k) + '.append((r,g,b))')

		for j in range(uvcount):
			eval('uvs.append(uvs_' + str(j) + ')')

		for j in range(colcount):
			eval('cols.append(col_' + str(j) + ')')

		return (
		 len(verts), verts, len(uvs), uvs, len(indices) * 3, indices, cols, norms)


def read_crowd_14(file):
	print('READING CROWD FILE')
	header = file.data.read(4).decode('utf-8')
	if not header == 'CRWD':
		print('NOT A VALID CROWD FILE')
		return
	file.data.read(2)
	count = struct.unpack('<H', file.data.read(2))[0]
	print(count)
	for i in range(count):
		file.data.read(2)
		verts = struct.unpack('<3f', file.data.read(12))
		zrot = struct.unpack('<f', file.data.read(4))[0]
		rawr = struct.unpack('<B', file.data.read(1))[0]
		rawg = struct.unpack('<B', file.data.read(1))[0]
		rawb = struct.unpack('<B', file.data.read(1))[0]
		r = hex(rawr)[2:]
		g = hex(rawg)[2:]
		b = hex(rawb)[2:]
		color = '#' + str(r) + str(g) + str(b)
		r = float(rawr / 255)
		g = float(rawg / 255)
		b = float(rawb / 255)
		colorrgb = (r, g, b)
		c_status = struct.unpack('<B', file.data.read(1))[0]
		c_attendance = struct.unpack('<B', file.data.read(1))[0]
		file.crowd.append((
		 verts, zrot, c_status, c_attendance, colorrgb, color, set1, set2, set3, set4))


def read_crowd_15(file):
	# scn = bpy.context.scene
	scn = bpy.context.scene
	print('READING CROWD FILE')
	header = file.data.read(4).decode('utf-8')
	if not header == 'CRWD':
		print('NOT A VALID CROWD FILE')
		return
	file.data.read(2)
	count = struct.unpack('<H', file.data.read(2))[0]
	print('Seat Count: ', count)
	t = open('crowd_log.txt', 'w')
	if scn.game_enum == 'FIFA15':
		skip = 7
	else:
		skip = 19
	for i in range(count):
		file.data.read(2)
		verts = struct.unpack('<3f', file.data.read(12))
		zrot = struct.unpack('<f', file.data.read(4))[0]
		rawr = struct.unpack('<B', file.data.read(1))[0]
		rawg = struct.unpack('<B', file.data.read(1))[0]
		rawb = struct.unpack('<B', file.data.read(1))[0]
		r = hex(rawr)[2:]
		g = hex(rawg)[2:]
		b = hex(rawb)[2:]
		color = '#' + str(r) + str(g) + str(b)
		r = float(rawr / 255)
		g = float(rawg / 255)
		b = float(rawb / 255)
		colorrgb = (r, g, b)
		c_status = struct.unpack('<4B', file.data.read(4))
		t.write(str(c_status) + '       ' + str(file.data.read(skip)) + '\n')
		file.crowd.append((verts, zrot, c_status, colorrgb, color))

	t.close()


def texture_convert(textures_list):
	status = ''
	for tex in textures_list:
		if tex[2]:
			comp = '-dxt5'
		else:
			comp = '-dxt1a'
		if tex[8] >= 2048:
			nmips = 10
		elif tex[8] >= 512:
			nmips = 3
		else:
			nmips = 1
		path, filename = os.path.split(tex[1])
		filename, ext = os.path.splitext(filename)
		if ext == '.dds':
			pass
		elif os.path.isfile(os.path.join(fifa_tools.texdir , filename + '.dds')):
			tex[1] = os.path.join(fifa_tools.texdir , filename + '.dds')
		else:
			status = call(['./fifa_tools/nvidia_tools/nvdxt.exe', '-file', tex[1], comp, '-nmips',
			 str(nmips), '-outdir', fifa_tools.texdir , '-quality_production', '-output', filename + '.dds'])
			tex[1] = os.path.join(fifa_tools.texdir , filename + '.dds')
		if status == 4294967294:
			return 'texture_path_error,' + tex[1]

	return str(status)


def convert_mesh_collisions(object):
	data = object.data
	verts = []
	bm = bmesh.new()
	bm.from_mesh(data)
	triscount = 0
	rot_x_mat = Matrix.Rotation(radians(-90), 4, 'X')
	scale_mat = Matrix.Scale(100, 4)
	for f in bm.faces:
		if len(f.verts) == 4:
			v0 = scale_mat * rot_x_mat * object.matrix_world * f.verts[0].co
			v1 = scale_mat * rot_x_mat * object.matrix_world * f.verts[1].co
			v2 = scale_mat * rot_x_mat * object.matrix_world * f.verts[2].co
			v3 = scale_mat * rot_x_mat * object.matrix_world * f.verts[3].co
			v0 = (
			 v0[0], v0[1], v0[2])
			v1 = (v1[0], v1[1], v1[2])
			v2 = (v2[0], v2[1], v2[2])
			v3 = (v3[0], v3[1], v3[2])
			verts.append(v0)
			verts.append(v1)
			verts.append(v2)
			verts.append(v3)
			verts.append(v0)
			verts.append(v2)
			triscount += 2
		else:
			v0 = scale_mat * rot_x_mat * object.matrix_world * f.verts[0].co
			v1 = scale_mat * rot_x_mat * object.matrix_world * f.verts[1].co
			v2 = scale_mat * rot_x_mat * object.matrix_world * f.verts[2].co
			v0 = (
			 v0[0], v0[1], v0[2])
			v1 = (v1[0], v1[1], v1[2])
			v2 = (v2[0], v2[1], v2[2])
			verts.append(v0)
			verts.append(v1)
			verts.append(v2)
			triscount += 1

	return (triscount, verts, object.name.split(sep='_')[(-1)] + 'Shape')


def write_crowd_file(f, object):
	data = object.data
	bm = bmesh.new()
	bm.from_mesh(data)
	bm.normal_update()
	rot_x_mat = Matrix.Rotation(radians(-90), 4, 'X')
	scale_mat = Matrix.Scale(100, 4)
	f.write(struct.pack('<IHI', 1146573379, 261, len(bm.faces)))
	for face in bm.faces:
		loc = face.calc_center_median()
		loc = scale_mat * rot_x_mat * object.matrix_world * loc
		f.write(struct.pack('<3f', loc[0], loc[1], loc[2]))
		f_normal = object.matrix_world * face.normal
		angle = round(degrees(Vector((f_normal[0], f_normal[1])).angle_signed(Vector((1,
																					  0)))), 0)
		if angle == 0:
			if round(degrees(Vector((f_normal[0], f_normal[1], 0)).angle(Vector((0,
																				 1,
																				 0)))), 0) == 180:
				angle = -180
			if round(degrees(Vector((f_normal[0], f_normal[1], 0)).angle(Vector((0,
																				 1,
																				 0)))), 0) == 0:
				angle = 180
		elif angle == 90:
			if round(degrees(Vector((f_normal[0], f_normal[1], 0)).angle(Vector((0,
																				 1,
																				 0)))), 0) == 180:
				angle = -90
			if round(degrees(Vector((f_normal[0], f_normal[1], 0)).angle(Vector((0,
																				 1,
																				 0)))), 0) == 0:
				angle = 90
		else:
			angle = angle
		f.write(struct.pack('<f', angle))
		try:
			collayer = bm.loops.layers.color[0]
			color = (
			 face.loops[0][collayer][0] * 255, face.loops[0][collayer][1] * 255, face.loops[0][collayer][2] * 255)
			f.write(struct.pack('<3B', int(color[0]), int(color[1]), int(color[2])))
		except:
			print('exception')
			f.write(struct.pack('<3B', 255, 255, 255))
		else:
			testvert = face.verts[0].index
			g = object.data.vertices[testvert].groups[0]
			print(g.group)
			gnameParts = object.vertex_groups[g.group].name.split(sep='_')
			try:
				gType = gnameParts[0]
				gFullness = gnameParts[1]
				gTier = int(gnameParts[2])
			except:
				gType = 'deadAway'
				gFullness = 'empty'
				gTier = 1
			else:
				f.write(struct.pack('<4B', *(list(crowdGroup.typeDict[gType]) + [gTier, crowdGroup.fullNessDict[gFullness]])))
				f.write(struct.pack('<9B', 0, 0, 0, 0, 0, 0, 0, 0, 0))


def object_separate(ob):
	verts = {}
	for g in ob.vertex_groups:
		verts[g.index] = []

	print(verts)
	for vert in ob.data.vertices:
		try:
			verts[vert.groups[0].group].append(vert.index)
		except:
			print('malakia')

	bm = bmesh.from_edit_mesh(ob.data)
	bpy.context.tool_settings.mesh_select_mode = (True, False, True)
	for f in bm.faces:
		f.select = False

	for i in range(len(verts) - 1):
		for f in bm.faces:
			for v in f.verts:
				if v.index in verts[i]:
					v.select = True
					f.select = True
					continue

	bmesh.update_edit_mesh(ob.data, False)
	bm.free()
	print('separating')


def write_xml_param(name, index, prop):
	class_name = prop.__class__.__name__
	if class_name == 'Vector' or class_name == 'bpy_prop_array' or class_name == 'tuple':
		value_repr = '{ '
		for i in range(len(prop)):
			value_repr += str(round(prop[i], 3))
			if i < len(prop) - 1:
				value_repr += ', '
				continue

		value_repr += ' }'
	else:
		value_repr = str(prop)
		if value_repr == 'True':
			value_repr = '1'
		elif value_repr == 'False':
			value_repr = '0'
	return '<parameter index=' + chr(34) + str(index) + chr(34) + ' name=' + chr(34) + name + chr(34) + ' value=' + chr(34) + value_repr + chr(34) + ' />\n'


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
	crowdGroup,
	fifa_rx3
	]

def register():
	for cls in classes:
		make_annotations(cls) # what is this? Read the section on annotations above!
		bpy.utils.register_class(cls)


def unregister():  # note how unregistering is done in reverse
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
		
if __name__ == "__main__":
	register()