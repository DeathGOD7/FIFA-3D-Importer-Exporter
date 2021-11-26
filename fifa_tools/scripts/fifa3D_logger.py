# Filename : fifa3D_logger.py
# Usage : Logger
# Author : Death GOD 7

import os
import sys
import bpy
import datetime
import fifa_tools
from enum import Enum

class LogType(str, Enum):
	INFO = "INFO"
	WARNING = "WARNING"
	ERROR = "ERROR"

class logger():
	def __init__(self, file = None, ext="log"):
		self.logdir = fifa_tools.logdir
		self.todayDate = datetime.datetime.now().strftime("%Y-%m-%d")
		if file == None:
			self.logfilename = self.todayDate
		else:
			self.logfilename = file
		self.logext = ext
		self.logfile = fifa_tools.logdir + f"\\{self.logfilename}.{self.logext}"

		if not os.path.exists(self.logfile):
			self.createLog()
			print(f"Log File Created : {self.logfile}") 

	def createLog(self):
		f = open(self.logfile,'a+')
		f.writelines(f'Blender Version : {bpy.app.version_string}\n')
		f.writelines(f'Python Version : {fifa_tools.pythonVer} ({fifa_tools.pythonArc})\n')
		f.writelines(f'Addon : FIFA 3D Importer/Exporter {fifa_tools.version_text}\n')
		f.writelines(f'Author : Death GOD 7 , arti-10\n')
		f.writelines(f'Date : {self.todayDate}\n')
		f.writelines('-----------------------------------------------------------------\n')
		f.close()

	def writeLog(self, message, msgType : LogType):
		f = open(self.logfile,'a+')
		currentTime = datetime.datetime.now().time().strftime("%r")
		f.writelines(f"{currentTime} - [{msgType}] {message}\n")
		f.close()

