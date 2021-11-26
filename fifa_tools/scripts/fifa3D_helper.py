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
	if vg_indices:
		# We replace/override here...
		vg = obj.vertex_groups.get(vg_name)
		if vg is None:
			vg = obj.vertex_groups.new(name=vg_name)
		for i, w in zip(vg_indices, vg_weights):
			vg.add((i,), w, 'REPLACE') 