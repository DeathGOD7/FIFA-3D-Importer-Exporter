import os
import sys
import clr

sys.path.append(f'{fifa_tools.addonLoc}\fifa_tools\libs')

clr.AddReference('SE7EN')
ref1 = clr.AddReference('FIFALibrary_v21_11_13_0_x64')

from SE7EN007 import *
from FIFALibrary20 import *
import enum

class FifaGames(enum.Enum):
   FIFA13 = 1
   FIFA14 = 2
   FIFA15 = 3
   FIFA16 = 4

class RX3_File():
	@staticmethod
	def testdll():
		