# Filename : utils/__init__.py
# Usage : Utils class made for FIFA 3D Importer/Exporter Addon for Blender
# Author : Death GOD 7

import os, sys, bpy, subprocess
import configparser
import datetime
import tarfile
from enum import Enum

import fifa_tools

def make_annotations(cls):
	"""Converts class fields to annotations if running with Blender 2.8 and higher"""
	if bpy.app.version < (2, 80):
		return cls
	bl_props = {k: v for k, v in cls.__dict__.items() if isinstance(v, tuple)}
	if bl_props:
		if '__annotations__' not in cls.__dict__:
			setattr(cls, '__annotations__', {})
		annotations = cls.__dict__['__annotations__']
		for k, v in bl_props.items():
			annotations[k] = v
			delattr(cls, k)
	return cls

class LogType(str, Enum):
	"""
	LogType Enum for different log types.

	Members:
	- INFO: General information messages.
	- WARNING: Warning messages indicating potential issues.
	- ERROR: Error messages indicating failures or critical issues.
	
	"""

	INFO = "INFO"
	WARNING = "WARNING"
	ERROR = "ERROR"

class Logger():
	"""
	Logger class for FIFA 3D Importer/Exporter Addon.

	Methods:
	- __init__(self, file = None, ext="log"): Initializes the logger with a specified file name and extension.
	- createLog(self): Creates a new log file with header information.
	- writeLog(self, message, msgType : LogType): Writes a log message with a specified type to the log file.
	"""
	
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
		f.writelines('-----------------------------------------------------------------\n')
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

class ArchiveManager():
	"""
	ArchiveManager class for managing archive files.

	Methods:
	- __init__(self): Initializes the ArchiveManager.
	- compress(self, path, archivename, ext=None): Compresses files in a specified directory into a tar.gz archive.
	- decompress(self, archivename, path=""): Decompresses a tar.gz archive into a specified directory.
	"""
	
	def __init__(self):
		pass

	def compress(self, path, archivename, ext=None):
		if ext != None:
			files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) if f.endswith(f".{ext}")]
		else:
			files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

		print(f"Compressing : {files}")

		with tarfile.open(f"{path}\\{archivename}.tar.gz","w:gz") as tar:
			for file in files:
				tar.add(os.path.basename(file))
		
		print(f"Files Compressed.")

	def decompress(self, archivename, path = ""):
		if tarfile.is_tarfile(archivename):
			if path == "":
				outdir = "."
			else:
				outdir = path

			if archivename.endswith("tar.gz"):
				tar = tarfile.open(archivename, "r:gz")
				tar.extractall(outdir)
				tar.close()
			elif archivename.endswith("tar"):
				tar = tarfile.open(archivename, "r:")
				tar.extractall(outdir)
				tar.close()
		else:
			print(f"Given file is not tar file.")		

class PackageManager():
	"""
	PackageManager class for managing Python packages.

	Methods:
	- __init__(self): Initializes the PackageManager.
	- checkFirstRun(self): Checks if it's the first run and upgrades pip if necessary.
	- install(self, pkgName): Installs a specified package.
	- uninstall(self, pkgName): Uninstalls a specified package.
	"""
	
	def __init__(self, configmanager):
		self.configManager = configmanager
		self.config = configmanager.config
		self.python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
		print(f"Using python from : {self.python_exe}")
		print(f"Python Version : {fifa_tools.pythonVer} ({fifa_tools.pythonArc})")
		self.checkFirstRun()

	def checkFirstRun(self):
		if (self.config['SETTINGS'].getboolean('First_Run')):
			subprocess.call([self.python_exe, "-m", "ensurepip"])
			subprocess.call([self.python_exe, "-m", "pip", "install", "--upgrade", "pip"])
		else:
			print("Skipping pip upgrade and deps install (Not first run)")

	def install(self, pkgName):
		subprocess.call([self.python_exe, "-m", "pip", "install", pkgName])
		filename = os.path.basename(pkgName)
		self.configManager.writeConfig("VERSIONS", "Python.NET", filename.split("-")[1])

	def uninstall(self, pkgName):
		subprocess.call([self.python_exe, "-m", "pip", "uninstall", pkgName])
		self.configManager.writeConfig("VERSIONS", "Python.NET", "0.0.0")

# FIFA3DLibs_v0.1.1

class DependencyManager():
	"""
	DependencyManager class for managing libs dependencies.

	Methods:
	- __init__(self): Initializes the DependencyManager.
	- checkDependencies(self): Checks and lists all files in update directory.
	- installLibs(self, version): Installs the specified version of FIFA3DLibs.
	"""
	
	def __init__(self, configmanager):
		self.depsLoc = fifa_tools.libsdir
		self.depsUpdateLoc = fifa_tools.updatesdir
		self.availableVersions = []
		self.configManager = configmanager
		self.config = configmanager.config
		self.installedVersion = self.config['VERSIONS']['FIFA3DLibs']
		self.isInstalled = self.installedVersion != "0.0.0"
		self.checkDependencies()

	def checkDependencies(self):
		if not os.path.exists(self.depsLoc):
			os.makedirs(self.depsLoc)

		if not os.path.exists(self.depsUpdateLoc):
			os.makedirs(self.depsUpdateLoc)

		for files in os.listdir(self.depsUpdateLoc):
			if files.endswith(".tar.gz"):
				self.availableVersions.append(files.split("_v")[1].split(".tar.gz")[0])

		print(f"Available Libs Versions : {self.availableVersions}")

		if not self.isInstalled:
			print("FIFA3DLibs not installed. Please install the libs.")
			print("Please download the libs from the website and place them in the Updates folder.")

	def installLibs(self, version):
		if version not in self.availableVersions:
			print(f"Libs version {version} not found in available versions.")
			print("Please download the libs from the website and place them in the Updates folder.")
			return

		for file in os.listdir(self.depsLoc):
			file_path = os.path.join(self.depsLoc, file)
			os.remove(file_path)

		updatefile = os.path.join(self.depsUpdateLoc, f"FIFA3DLibs_v{version}.tar.gz")
		if os.path.exists(updatefile):
			print(f"Installing FIFA3DLibs v{version}...")
			archive_manager = ArchiveManager()
			archive_manager.decompress(updatefile, self.depsLoc)
			self.configManager.writeConfig("VERSIONS", "FIFA3DLibs", version)
			print(f"FIFA3DLibs v{version} installed.")

class ConfigManager():
	"""
	ConfigManager class for managing configuration files.

	Methods:
	- __init__(self, cfgname,  ext="ini"): Initializes the ConfigManager with a specified file name and section.
	- createConfig(self): Creates a new configuration file with default settings.
	- writeConfig(self, section, key, value): Writes a key-value pair to the configuration file.
	- loadConfig(self): Reads the configuration file and returns the config object.
	"""
	
	def __init__(self, cfgname, ext="ini"):
		self.cfgname = cfgname
		self.ext = ext
		self.config = None
		self.filedir = f"{fifa_tools.maindir}\{self.cfgname}.{self.ext}"
		self.loadConfig()

	def createConfig(self):
		print("Config file is missing. Creating new one....")
		self.config = configparser.ConfigParser()

		self.config["SETTINGS"] = {}
		self.config["VERSIONS"] = {}
	
		# Set default key-value pairs
		settingsDefaults = {
			"Config_Version": "1",
			"First_Run": "True",
			"Export_Location": "~"
		}
		
		versionsDefaults = {
			"Python.NET": "0.0.0",
			"FIFA3DLibs": "0.0.0"
		}

		for key, value in settingsDefaults.items():
			self.config["SETTINGS"][str(key)] = str(value)
		
		for key, value in versionsDefaults.items():
			self.config["VERSIONS"][str(key)] = str(value)
	
		print("Config file created. Writing data....")
		with open(self.filedir, 'w') as configfile:
			self.config.write(configfile)
	
		return self.config

	def writeConfig(self, section, key, value):
		if self.config is None:
			self.loadConfig()

		self.config[str(section)][str(key)] = str(value)

		with open(self.filedir,'w') as configfile:
			self.config.write(configfile)

		return self.config

	def checkConfigFile(self):
		if not os.path.exists(self.filedir):
			return False
		else:
			return True

	def loadConfig(self):
		if not self.checkConfigFile():
			self.config = self.createConfig()
		else:
			print("Reading config file....")
			# Read the config file
			self.config = configparser.ConfigParser()
			self.config.read(self.filedir)

		return self.config


