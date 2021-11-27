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
	for x in range(len(vgindice)):
		for y in vgindice[x]:
			if y not in groups:
				groups[y] = []
			elif x in groups[y]:
				continue
			groups[y].append(x)

	for y in groups:
		vg = ob.vertex_groups.get(str(y))
		if vg is None:
			vg = ob.vertex_groups.new(name=str(y))
		for i, w in zip(vg_indices, vg_weights):
			vg.add(groups[j], w, 'ADD')
