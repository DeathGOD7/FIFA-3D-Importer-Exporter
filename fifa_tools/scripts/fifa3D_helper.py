# Filename : fifa3D_helper.py
# Usage : Useful methods for my addon
# Author : Death GOD 7

import os
import sys
import bpy
import fifa_tools
import zlib, struct
from enum import Enum
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

def AddVertexSkeleton(bones, fileID, skI):
	for bone_id in range(len(bones)):
		amt = bpy.data.armatures.new('armature_' + str(fileID) + '_' + str(bone_id))
		ob = bpy.data.objects.new('armature_object_' + str(bone_id), amt)
		
		context.collection.objects.link(ob)
		bpy.context.view_layer.objects.active = obj
		bpy.ops.object.mode_set(mode='EDIT')
		for i in range(len(bones[bone_id])):
			bone = amt.edit_bones.new('mynewnewbone_' + str(i))
			bone.head, bone.tail, bone.roll = bones[bone_id][i]

		bpy.ops.object.mode_set(mode='OBJECT')
		ob.scale = Vector((1, 1, 1))
		# ob.scale = Vector((0.01, 0.01, 0.01))
		ob.rotation_euler[1] = 1.5707972049713135



