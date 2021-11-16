import os
import sys
import bpy
import clr
import fifa_tools

sys.path.append(f'{fifa_tools.addonLoc}\\fifa_tools\\libs')

clr.AddReference('SE7EN')
ref1 = clr.AddReference('FIFALibrary_v21_11_13_0_x64')

from SE7EN007 import *
from FIFALibrary20 import *
import enum



class FifaGames(enum.Enum):
	FIFA11 = 1
	FIFA12 = 2
	FIFA13 = 3
	FIFA14 = 4
	FIFA15 = 5
	FIFA16 = 6

class RX3_File():
	
	@staticmethod
	def testdll(rx3file):
		file = rx3file
		if file != "":
			model_test = Rx3File()
			model_test.Load(file)
			v = model_test.Rx3VertexBuffers[0]
			print(v.Vertexes)
		else:
			print("Please choose the model file.")

		