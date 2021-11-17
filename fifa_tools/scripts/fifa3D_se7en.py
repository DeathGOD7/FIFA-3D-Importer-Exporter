import os
import sys
import bpy
import clr
import fifa_tools

sys.path.append(f'{fifa_tools.libsdir}')

clr.AddReference('SE7EN')
ref1 = clr.AddReference('FIFALibrary_v21_11_13_0_x64')

from SE7EN007 import *
from FIFALibrary20 import *
from enum import Enum

class GameType(str, Enum):
	FIFA11 = "FIFA11"
	FIFA12 = "FIFA12"
	FIFA13 = "FIFA13"
	FIFA14 = "FIFA14"
	FIFA15 = "FIFA15"
	FIFA16 = "FIFA16"

class FileType(str, Enum):
	RX2_OLD = "RX2_OLD"
	RX2 = "RX2"
	RX3_Hybrid = "RX3_Hybrid"
	RX3 = "RX3"
	FB = "FB"

class SkeletonType(str, Enum):
	OLD_SKELETON = "OLD_SKELETON"
	FIFA11PC_SKELETON = "FIFA11PC_SKELETON"
	IE_SKELETON = "IE_SKELETON"
	FIFA14_SKELETON = "FIFA14_SKELETON"
	FIFA15_SKELETON = "FIFA15_SKELETON"
	FIFA16_SKELETON = "FIFA16_SKELETON"
	FROSTBITE_OLD_SKELETON = "FROSTBITE_OLD_SKELETON"
	FROSTBITE_NEW_SKELETON = "FROSTBITE_NEW_SKELETON"

def GetFileType(GType):
	rx3 = [GameType.FIFA12, GameType.FIFA13, GameType.FIFA14, GameType.FIFA15, GameType.FIFA16]
	rx3_hybrid = [GameType.FIFA11]

	if GType in rx3:
		return FileType.RX3
	elif GType in rx3_hybrid:
		return FileType.RX3_Hybrid
	else:
		return "Unsupported Game"

def GetSkeletonType(GType):
	if GType == "FIFA11":
		return SkeletonType.FIFA11PC_SKELETON
	elif (GType == "FIFA12") or (GType == "FIFA13"):
		return SkeletonType.IE_SKELETON
	elif GType == "FIFA14":
		return SkeletonType.FIFA14_SKELETON
	elif GType == "FIFA15":
		return SkeletonType.FIFA15_SKELETON
	elif GType == "FIFA16":
		return SkeletonType.FIFA16_SKELETON
	else:
		return "Unsupported Game"

class RX3_File():
	def __init__(self, file, ftype): 
		self.file = file
		self.ftype = ftype

	@staticmethod
	def testdll(rx3file):
		file = rx3file
		if file != "":
			model_test = Rx3File()
			model_test.Load(file)
			
			print(f"Vertex Format Count : {model_test.Rx3VertexFormats.Length}")

			vF = list()

			for x in range(model_test.Rx3VertexFormats.Length):
				for y in range(model_test.Rx3VertexFormats[x].VertexFormat.Length):
					vF.append(model_test.Rx3VertexFormats[x].VertexFormat[y])

			print(f"Vertex Formats : {vF}")
			
			v = model_test.Rx3VertexBuffers[0]
			print(v.Vertexes.Length)
			print(f"Position X = {v.Vertexes[0].Positions[0].X}")
			print(f"Position Y = {v.Vertexes[0].Positions[0].Y}")
			print(f"Position Z = {v.Vertexes[0].Positions[0].Z}")
			print(f"Position W = {v.Vertexes[0].Positions[0].W}")
		else:
			print("Please choose the model file.")
