# Filename : fifa3D_helper.py
# Usage : Useful methods for my addon
# Author : Death GOD 7

import os
import sys
import bpy
import fifa_tools
import zlib, struct
from enum import Enum

def List_To_Tuple(lst):
	return tuple(List_To_Tuple(i) if isinstance(i, list) else i for i in lst)

def Add_Vgroup_To_Objects(vg_indices, vg_weights, vg_name, obj):
	assert(len(vg_indices) == len(vg_weights))
	ob = bpy.data.objects[obj] 
	groups = {}
	vgindice = List_To_Tuple(vg_indices)
	vgweight = List_To_Tuple(vg_weights)
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
		vg = ob.vertex_groups.get(str(y))
		if vg is None:
			vg = ob.vertex_groups.new(name=str(y))
		for x in groups[y]:
			n = groups[y].index(x)
			vg.add((x,), groupsV[y][n], 'ADD')

def LoadSkeletonInfo(skeletonType):
	dd = 0