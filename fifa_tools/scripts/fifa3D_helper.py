# Filename : fifa3D_helper.py
# Usage : Useful methods for my addon
# Author : Death GOD 7

import os
import sys
import bpy, imp, struct, bmesh, zlib
from bpy.types import Bone
import fifa_tools
from math import radians, degrees
from enum import Enum
from mathutils import Vector, Euler, Matrix
from fifa_tools.scripts.fifa3D_logger import *

def ListToTuple(lst):
	return tuple(ListToTuple(i) if isinstance(i, list) else i for i in lst)

def AddVgroupToObjects(vg_indices, vg_weights, skI, obj):
	assert(len(vg_indices) == len(vg_weights))
	ob = bpy.data.objects[obj] 
	groups = {}
	vgindice = ListToTuple(vg_indices)
	vgweight = ListToTuple(vg_weights)
	groupsV = {}
	for x in range(len(vgindice)):
		for y in vgindice[x]:
			t = vgindice[x].index(y)
			if y not in groups:
				groups[y] = []
				groupsV[y] = []
			elif x in groups[y]:
				continue
			groups[y].append(x)
			groupsV[y].append(vgweight[x][t])

	for y in groups:
		vg = ob.vertex_groups.get(skI[str(y)])
		if vg is None:
			vg = ob.vertex_groups.new(name=skI[str(y)])
		for x in groups[y]:
			n = groups[y].index(x)
			vg.add((x,), groupsV[y][n], 'ADD')

def LoadSkeletonInfo(skeletonType):
	log = fifa_tools.globalLogFile
	dictSkeleton = {}
	skeletonInfoDir = f"{fifa_tools.addonLoc}\\fifa_tools\\skeletons"
	skeletonInfoFile = f"{skeletonType}.txt"
	files = [f for f in os.listdir(skeletonInfoDir) if os.path.isfile(os.path.join(skeletonInfoDir, f)) if f.endswith(f".txt")]

	if skeletonInfoFile in files:
		f = open(f"{skeletonInfoDir}\\{skeletonInfoFile}", 'r')
		lines = f.readlines()
		for line in lines:
			temp = line.split(sep=",")
			key = temp[0]
			value = temp[1]
			dictSkeleton[key] = value
		return dictSkeleton
	else:
		log.writeLog(f"No skeleton named \"{skeletonType}\" found of given game. It is probably not supported.", LogType.ERROR)
		return None

def GetSkeletonBoneValues(bones):
	pos1 = bones[1]
	mat = Matrix()
	mat = mat.to_3x3()
	for x in range(3):
		for y in range(3):
			mat[x][y] = bones[0].Get(x,y)
	axis, roll = Bone.AxisRollFromMatrix(mat, axis=mat.col[1])
	pos2 = Vector(pos1) + axis
	return pos1, pos2, roll

def AddVertexSkeleton(bones, fileID, skI):
	for bone_id in range(len(bones)):
		amt = bpy.data.armatures.new('armature_' + str(fileID) + '_' + str(bone_id))
		ob = bpy.data.objects.new('armature_object_' + str(bone_id), amt)

		bpy.context.collection.objects.link(ob)
		bpy.context.view_layer.objects.active = ob
		bpy.ops.object.mode_set(mode='EDIT')

		for i in range(len(bones[bone_id])):
			bone = amt.edit_bones.new(skI[str(i)])
			pos1, pos2, roll = GetSkeletonBoneValues(bones[bone_id][i])
			bone.head = pos1
			bone.tail = pos2
			bone.roll = roll

		bpy.ops.object.mode_set(mode='OBJECT')
		ob.scale = Vector((0.01, 0.01, 0.01))
		ob.rotation_euler[1] = 1.5707972049713135

def ConvertMeshToData(object, normal, binormal, tangent):
	verts = []
	uvs = []
	indices = []
	cols_normals = []
	cols_binormals = []
	cols_tangents = []
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
	col_0 = [] #normal
	col_1 = [] #binormal
	col_2 = [] #tangent
	uvcount = len(bm.loops.layers.uv)
	# colcount = len(bm.loops.layers.color)
	rot_x_mat = Matrix.Rotation(radians(90), 4, 'X')
	scale_mat = Matrix.Scale(100, 4)
	
	if hasattr(bm.verts, "ensure_lookup_table"): 
		bm.verts.ensure_lookup_table()
		# only if you need to:
		# bm.edges.ensure_lookup_table()   
		# bm.faces.ensure_lookup_table()
	
	for vert in bm.verts:
		co = scale_mat @ rot_x_mat @ object.matrix_world @ vert.co
		
		verts.append((co[0], -co[1], -co[2]))

	bm.verts.ensure_lookup_table()
	for i in range(len(bm.verts)):
		for j in range(uvcount):
			uvlayer = bm.loops.layers.uv[j]
			eval('uvs_' + str(j) + '.append((round(bm.verts[i].link_loops[0][uvlayer].uv.x,8),round(1-bm.verts[i].link_loops[0][uvlayer].uv.y,8)))')
	
	# for i in range(len(bm.verts)):
	# 	for j in range(colcount):
	# 		# collayer = bm.loops.layers.color[j]
	# 		collayer = bm.loops.layers.color["Col"]
	# 		vert_data = bm.verts[i].link_loops[0][collayer]
	# 		eval('col_' + str(j) + '.append((vert_data[0]*1023,vert_data[1]*1023,vert_data[2]*1023))')

	for i in range(len(bm.verts)):
		# normal
		if normal:
			collayer0 = bm.loops.layers.color[('col_normal')]
			vert_data0 = bm.verts[i].link_loops[0][collayer0]
			col_0.append((vert_data0[0],vert_data0[1],vert_data0[2]))
		
		# binormal
		if binormal:
			collayer1 = bm.loops.layers.color[('col_binormal')]
			vert_data1 = bm.verts[i].link_loops[0][collayer1]
			col_1.append((vert_data1[0],vert_data1[1],vert_data1[2]))
		
		# normal
		if tangent:
			collayer2 = bm.loops.layers.color[('col_tangent')]
			vert_data2 = bm.verts[i].link_loops[0][collayer2]
			col_2.append((vert_data2[0],vert_data2[1],vert_data2[2]))

	bm.faces.ensure_lookup_table()
	for f in bm.faces:
		bm.faces.ensure_lookup_table()
		indices.append((
			f.verts[0].index, f.verts[1].index, f.verts[2].index))

	for j in range(uvcount):
		eval('uvs.append(uvs_' + str(j) + ')')

	# for j in range(colcount):
	# 	eval('cols.append(col_' + str(j) + ')')
	cols_normals.append(col_0)
	cols_binormals.append(col_1)
	cols_tangents.append(col_2)

	bm.free()	

	return (verts, indices, uvs, cols_normals, cols_binormals, cols_tangents)



