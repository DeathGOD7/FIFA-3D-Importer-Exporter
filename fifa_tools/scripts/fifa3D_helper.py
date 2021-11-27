# Filename : fifa3D_helper.py
# Usage : Useful methods for my addon
# Author : Death GOD 7

import os
import sys
import bpy
import fifa_tools
import zlib, struct
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

def matCalc():
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
	# temp.append((pos, pos + axis, roll))

def AddVertexSkeleton(bones, fileID, skI):
	for bone_id in range(len(bones)):
		amt = bpy.data.armatures.new('armature_' + str(fileID) + '_' + str(bone_id))
		ob = bpy.data.objects.new('armature_object_' + str(bone_id), amt)
		
		bpy.context.collection.objects.link(ob)
		bpy.context.view_layer.objects.active = ob
		bpy.ops.object.mode_set(mode='EDIT')
		for i in range(len(bones[bone_id])):
			bone = amt.edit_bones.new(skI[str(i)])
			bone.head = bones[bone_id][i][3][0], bones[bone_id][i][3][1], bones[bone_id][i][3][2]
			bone.tail = bones[bone_id][i][3][0], bones[bone_id][i][3][1], bones[bone_id][i][3][2]
			bone.roll = bones[bone_id][i][3][2]

		bpy.ops.object.mode_set(mode='OBJECT')
		ob.scale = Vector((1, 1, 1))
		# ob.scale = Vector((0.01, 0.01, 0.01))
		ob.rotation_euler[1] = 1.5707972049713135




