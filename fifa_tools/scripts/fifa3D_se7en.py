import clr
import os
import sys
import bpy
import fifa_tools
import zlib, struct

sys.path.append(f'{fifa_tools.libsdir}')

clr.AddReference('SE7EN')
ref1 = clr.AddReference('FIFALibrary_v21_11_13_0_x64')

from SE7EN007 import *
from FIFALibrary20 import *
from enum import Enum

class GameType(str, Enum):
	FIFA11 = "FIFA 11"
	FIFA12 = "FIFA 12"
	FIFA13 = "FIFA 13"
	FIFA14 = "FIFA 14"
	FIFA15 = "FIFA 15"
	FIFA16 = "FIFA 16"

class FileType(str, Enum):
	RX2_OLD = "RX2_OLD" # FIFA 06/WC06
	RX2 = "RX2" # FIFA 07/08/euro08/09
	RX3_Hybrid = "RX3_Hybrid" # FIFA 10_console, FIFA 11 (pc+console), FO3_old : rx3 with RW4 sections
	RX3 = "RX3" # FIFA 12 - 16 or later
	FB = "FB" # FrostBite3 format (fbx)

class SkeletonType(str, Enum):
	OLD_SKELETON = "OLD_SKELETON"
	FIFA11PC_SKELETON = "FIFA11PC_SKELETON"
	IE_SKELETON = "IE_SKELETON" #impact engine
	FIFA14_SKELETON = "FIFA14_SKELETON" #ignite engine_v1
	FIFA15_SKELETON = "FIFA15_SKELETON" #ignite engine_v2
	FIFA16_SKELETON = "FIFA16_SKELETON" #ignite engine_v3
	FROSTBITE_OLD_SKELETON = "FROSTBITE_OLD_SKELETON" #Fifa_online_4_old
	FROSTBITE_NEW_SKELETON = "FROSTBITE_NEW_SKELETON" #Fifa_online_4_new + FIFA 17-21 pc

def GetRX3FileType(GType:GameType):
	rx3 = [GameType.FIFA12, GameType.FIFA13, GameType.FIFA14, GameType.FIFA15, GameType.FIFA16]
	rx3_hybrid = [GameType.FIFA11]

	if GType in rx3:
		return FileType.RX3
	elif GType in rx3_hybrid:
		return FileType.RX3_Hybrid
	else:
		return "Unsupported Game"

def GetSkeletonType(GType:GameType):
	if GType == GameType.FIFA11:
		return SkeletonType.FIFA11PC_SKELETON
	elif (GType == GameType.FIFA12) or (GType == GameType.FIFA13):
		return SkeletonType.IE_SKELETON
	elif GType == GameType.FIFA14:
		return SkeletonType.FIFA14_SKELETON
	elif GType == GameType.FIFA15:
		return SkeletonType.FIFA15_SKELETON
	elif GType == GameType.FIFA16:
		return SkeletonType.FIFA16_SKELETON
	else:
		return "Unsupported Game"

def GetFileType(file):
	filePath, fileName = os.path.split(file)
	fileName, filEext = os.path.splitext(fileName)
	try:
		fileId = fileName.split(sep='_')[1]
		fileType = fileName.split(sep='_')[0]
		return (fileName, filEext, fileType, fileId, filePath)
	except:
		return 'corrupt_filename'


class RX3_File():
	def __init__(self, file, gtype): 
		# file info
		self.file = file
		self.fileName = ""
		self.fileExt = ""
		self.filePath = ""
		self.fileType = ""
		self.fileId = 0
		self.gtype = gtype
		# file info end
		self.cols = []  ## Normal / Binormals / Tangent Cols
		self.colCount = []
		self.collision = []
		self.collisionCount = []
		self.data = 0
		self.endian = ""
		self.endianStr = ""
		self.endianType = ""
		self.faces= []
		self.faceCount = []
		self.indicesCount = []
		self.indicesLength = []
		self.offsets = []
		self.meshCount = 0
		self.primitiveType = 0
		self.uvs = []
		self.uvCount = []
		self.vertexFormat = []
		self.vertexPosition = []
		self.totalVertCount = []
		self.vertexSize = []
		self.vertexColor = [] ## was used bone_c in it on original addon
		self.vertexColorCount = [] ## was used bone_c in it on original addon
		#bones section
		# -> 4 bones/vertex : FIFA 11 - 14
		# -> 8 bones/vertex : FIFA 15-16
		self.bonesIndice = [] ## was also used as bone_i in original addon
		self.bonesIndiceCount = [] ## was also used as bone_i in original addon
		self.bonesWeight = [] ## was also used as bone_w in original addon
		self.bonesWeightCount = []## was also used as bone_w in original addon
		#bones section end

		# Get file infos
		fI = GetFileType(self.file)
		if fI != "corrupt_filename":
			self.fileName = fI[0]
			self.fileExt = fI[1]
			self.fileType = fI[2]
			self.fileId = fI[3]
			self.filePath = fI[4]
			## Load Rx3
			if GetRX3FileType(self.gtype) == FileType.RX3:
				if self.fileExt == ".rx3":
					self.loadRx3()
				else:
					print(f"\n[ERROR] File {self.file} is not valid RX3 file.")
			else:
				print(f"\n[ERROR] Game {self.gtype} is not valid supported game or wrong file loaded here.")
		else:
			print(f"\n[ERROR] File {self.file} is not valid RX3 file or wrong file loaded here.")

	#region Importer

	def getDataRx3(self, file):
		data = open(file, 'rb')
		
		print(f"\nFile : {self.fileName+self.fileExt}")
		print(f"File ID : {self.fileId}")
		print(f"File Type : {self.fileType}")
		print(f"File Path : {self.filePath}\n")

		if str(data.read(8))[2:-1] == 'chunkzip':
			t = BytesIO()
			data.read(12)
			sec_num = struct.unpack('>I', data.read(4))[0]
			data.read(8)
			for i in range(sec_num):
				off = data.tell() % 4
				if off:
					data.read(4 - off)
				sec_found = False
				while 1:
					if not sec_found:
						sec_len = struct.unpack('>I', data.read(4))[0]
					if not sec_len == 0:
						sec_found = True
						continue

				data.read(4)
				data = data.read(sec_len)
				try:
					t.write(zlib.decompress(data, -15))
				except zlib.error:
					return 'corrupt_file'

			data = t

		return data

	def facereadlist(self, f, offset, mID, indicesLength, indicesCount, endian):
		f.seek(offset)
		faces = []
	
		self.faceCount.append(int(indicesCount / 3))

		print(f"Face Count, Mesh {mID}: {self.faceCount[mID]}")

		# this is read in addon to get indicescount and length
		# f.read(4) 
		# f.read(4) # indicescount
		# f.read(1) # indiceslength
		# f.read(3)
		# f.read(4)
		# all read are 16 bytes so...auto doing read of 16

		# > = big endian
		# < = little endian
		f.read(16)

		if indicesLength == 4:
			string = endian + 'III'
		elif indicesLength == 2:
			string = endian + 'HHH'

		for i in range(self.faceCount[mID]):
			temp = struct.unpack(string, f.read(indicesLength * 3))
			if not temp[0] == temp[1]:
				if not temp[2] == temp[1]:
					if temp[0] == temp[2]:
						continue
					faces.append((temp[0], temp[1], temp[2]))

		print(f"Values of Face 0, Mesh {mID}: {faces[0]}")
		return faces

	def facereadstrip(self, f, offset, mID, indicesLength, indicesCount, endian):
		f.seek(offset)
		faces = []
		self.faceCount.append(indicesCount - 2)

		print(f"Face Count, Mesh {mID}: {self.faceCount[mID]}")

		# f.read(4)
		# f.read(4) # indicescount
		# f.read(4) # indiceslength
		# f.read(4)
		# all read are 16 bytes so...auto doing read of 16

		# > = big endian
		# < = little endian
		f.read(16)

		if indicesLength == 4:
			string = endian + 'HHH'
		elif indicesLength == 2:
			string = endian + 'HHH'

		flag = False
		for i in range(self.faceCount[mID]):
			back = f.tell()
			temp = struct.unpack(string, f.read(indicesLength * 3))
			if temp[0] == temp[1] or temp[1] == temp[2] or temp[0] == temp[2]:
				flag = not flag
				f.seek(back + indicesLength)
				continue
			elif flag is False:
				faces.append((temp[0], temp[1], temp[2]))
			elif flag is True:
				faces.append((temp[2], temp[1], temp[0]))
			flag = not flag
			f.seek(back + indicesLength)

		print(f"Values of Face 0, Mesh {mID}: {faces[0]}")
		return faces

	def getOffsets(self, rx3file):
		obtainedOffsets = []
		sect_num  = rx3file.Rx3Header.NumSections
		print('Number of Sectors Detected : ', sect_num)

		# blender offset[0] -> rx3file.Rx3SectionHeaders(id).Signature (= section hashed name) 
		# blender offset[1] -> rx3file.Rx3SectionHeaders(id).Offset (= where the section starts in file)

		for x in range(0, sect_num):
			obtainedOffsets.append([rx3file.Rx3SectionHeaders[x].Signature, rx3file.Rx3SectionHeaders[x].Offset])

		print(f"Offsets : {obtainedOffsets}")
		
		return obtainedOffsets

	def getVertexFormats(self, rx3file):
		for x in range(rx3file.Rx3VertexFormats.Length):
			temp = []
			print(f"Total Vertex Elements , Mesh {x}: {rx3file.Rx3VertexFormats[x].VertexFormat.Length}")
			for y in range(rx3file.Rx3VertexFormats[x].VertexFormat.Length):
				temp.append(rx3file.Rx3VertexFormats[x].VertexFormat[y])
			self.vertexFormat.append(temp)

		print(f"Vertex Formats : {self.vertexFormat}")
		return self.vertexFormat

	def getVertexPosition(self, rx3file):
		for i in range(rx3file.Rx3VertexBuffers.Length):
			temp = []
			v = rx3file.Rx3VertexBuffers[i]

			self.totalVertCount.append(v.NumVertices)
			# self.totalVertCount.append(v.Vertexes.Length)
			print(f"Total Vertices Count, Mesh {i} : {self.totalVertCount[i]}")

			self.vertexSize.append(v.VertexSize)
			print(f"Total Vertex Size, Mesh {i} : {self.vertexSize[i]}")

			for x in range(v.Vertexes.Length):
				data = [v.Vertexes[x].Positions[0].X/100 , -v.Vertexes[x].Positions[0].Z/100, v.Vertexes[x].Positions[0].Y/100]
				# data = [v.Vertexes[x].Positions[0].X/100 , -v.Vertexes[x].Positions[0].Z/100, v.Vertexes[x].Positions[0].Y/100, v.Vertexes[x].Positions[0].W]
				temp.append(data)
			
			self.vertexPosition.append(temp)
			print(f"Position X,Z,Y,W of Vertex 0, Mesh {i} = {self.vertexPosition[i][0]}")

		return self.vertexPosition

	def getIndicesData(self, rx3file):
		# rx3model.Rx3IndexBuffer(meshid) ==> For faces
		# rx3model.Rx3IndexBuffer(meshid).Rx3IndexBufferHeader.IndexSize is the same as "indiceslength" in your code
		for i in range( rx3file.Rx3IndexBuffers.Length):
			indices = rx3file.Rx3IndexBuffers[i]

			self.indicesCount.append(indices.IndexStream.Length)
			print(f"Incides Count, Mesh {i} : {self.indicesCount[i]}")

			self.indicesLength.append(indices.Rx3IndexBufferHeader.IndexSize)
			print(f"Indices Length, Mesh {i} : {self.indicesLength[i]}")

		return [self.indicesCount, self.indicesLength]

	def getVertexColor(self, rx3file): #was also used as bone_c in original addon
		for i in range(rx3file.Rx3VertexBuffers.Length):
			temp = []
			v = rx3file.Rx3VertexBuffers[i]

			for x in range(v.Vertexes.Length):
				if (v.Vertexes[x].Colors != None) :
					data = [v.Vertexes[x].Colors[0].Value_R , v.Vertexes[x].Colors[0].Value_G, v.Vertexes[x].Colors[0].Value_B]
					# data = [v.Vertexes[x].Colors[0].Value_R , v.Vertexes[x].Colors[0].Value_G, v.Vertexes[x].Colors[0].Value_B, v.Vertexes[x].Colors[0].Value_A]
					temp.append(data)
				else:
					print(f"No Vertex Color Found in Mesh {i}!")
					break
			
			self.vertexColor.append(temp)
			self.vertexColorCount.append(len(self.vertexColor[i]))
			if len(self.vertexColor[i]) > 0:
				print(f"Color R,G,B,A of Vertex Color 0, Mesh {i} = {self.vertexColor[i][0]}")
				print(f"Vertex Color Count, Mesh {i} : {self.vertexColorCount[i]}")
		
		return self.vertexColor
	
	def getBoneIndice(self, rx3file): #was also used as bone_i in original addon
		for i in range(rx3file.Rx3VertexBuffers.Length):
			temp = []
			v = rx3file.Rx3VertexBuffers[i]

			if (v.Vertexes[0].BlendIndices != None) :
				print(f"Total Blend Indices Set : [{v.Vertexes[0].BlendIndices.Length}]")
			
			for x in range(v.Vertexes.Length):
				if (v.Vertexes[x].BlendIndices != None) :
					vertexdata = []
					for y in range(v.Vertexes[x].BlendIndices.Length):
						tempdata = [v.Vertexes[x].BlendIndices[y].Index_1 , v.Vertexes[x].BlendIndices[y].Index_2, v.Vertexes[x].BlendIndices[y].Index_3, v.Vertexes[x].BlendIndices[y].Index_4]
						vertexdata.append(tempdata)
					temp.append(vertexdata)
				else:
					print(f"No Bone Indices Found in Mesh {i}!")
					break
			
			self.bonesIndice.append(temp)
			self.bonesIndiceCount.append(len(self.bonesIndice[i]))
			if len(self.bonesIndice[i]) > 0:
				print(f"Bone Indice Index 1,2,3,4 of Vertex Bone 0, Mesh {i} = {self.bonesIndice[i][0]}")
				print(f"Bone Indice Count, Mesh {i} : {self.bonesIndiceCount[i]}")
		
		return self.bonesIndice
	
	def getBoneWeight(self, rx3file): #was also used as bone_w in original addon
		for i in range(rx3file.Rx3VertexBuffers.Length):
			temp = []
			v = rx3file.Rx3VertexBuffers[i]

			if (v.Vertexes[0].BlendWeights != None) :
				print(f"Total Blend Weights Set : [{v.Vertexes[0].BlendWeights.Length}]")
			

			for x in range(v.Vertexes.Length):
				if (v.Vertexes[x].BlendWeights != None) :
					vertexdata = []
					for y in range(v.Vertexes[x].BlendWeights.Length):
						tempdata = [v.Vertexes[x].BlendWeights[y].Weight_1 , v.Vertexes[x].BlendWeights[y].Weight_2, v.Vertexes[x].BlendWeights[y].Weight_3, v.Vertexes[x].BlendWeights[y].Weight_4]
						vertexdata.append(tempdata)
					temp.append(vertexdata)
				else:
					print(f"No Bone Weights Found in Mesh {i}!")
					break
			
			self.bonesWeight.append(temp)
			self.bonesWeightCount.append(len(self.bonesWeight[i]))
			if len(self.bonesWeight[i]) > 0:
				print(f"Bone Weights 1,2,3,4 of Vertex Bone 0, Mesh {i} = {self.bonesWeight[i][0]}")
				print(f"Bone Weights Count, Mesh {i} : {self.bonesWeightCount[i]}")
		
		return self.bonesWeight

	def getNormalCols(self, rx3file):
		for i in range(rx3file.Rx3VertexBuffers.Length):
			temp = []
			v = rx3file.Rx3VertexBuffers[i]

			for x in range(v.Vertexes.Length):
				#normals / n
				if v.Vertexes[x].Normals != None:
					data1 = [v.Vertexes[x].Normals[0].Normal_x , v.Vertexes[x].Normals[0].Normal_y, v.Vertexes[x].Normals[0].Normal_z]
					# data1 = [v.Vertexes[x].Normals[0].Normal_x , v.Vertexes[x].Normals[0].Normal_y, v.Vertexes[x].Normals[0].Normal_z, v.Vertexes[x].Normals[0].DEC3N]
					temp.append(data1)
				#binormals / b
				if v.Vertexes[x].Binormals != None:
					data2 = [v.Vertexes[x].Binormals[0].Binormal_x , v.Vertexes[x].Binormals[0].Binormal_y, v.Vertexes[x].Binormals[0].Binormal_z]
					# data2 = [v.Vertexes[x].Binormals[0].Binormal_x , v.Vertexes[x].Binormals[0].Binormal_y, v.Vertexes[x].Binormals[0].Binormal_z, v.Vertexes[x].Binormals[0].DEC3N]
					temp.append(data2)
				#tangent / g
				if v.Vertexes[x].Tangents != None:
					data3 = [v.Vertexes[x].Tangents[0].Tangent_x , v.Vertexes[x].Tangents[0].Tangent_y, v.Vertexes[x].Tangents[0].Tangent_z]
					# data3 = [v.Vertexes[x].Tangents[0].Tangent_x , v.Vertexes[x].Tangents[0].Tangent_y, v.Vertexes[x].Tangents[0].Tangent_z, v.Vertexes[x].Tangents[0].DEC3N]
					temp.append(data3)
			
			self.cols.append(temp)
			self.colCount.append(len(self.cols[i]))
			if len(self.cols[i]) > 0:
				print(f"Color X,Y,Z,DEC3N of Col 0, Mesh {i} = {self.cols[i][0]}")
				print(f"Color X,Y,Z,DEC3N of Col 1, Mesh {i} = {self.cols[i][1]}")
				print(f"Color X,Y,Z,DEC3N of Col 2, Mesh {i} = {self.cols[i][2]}")
				print(f"Color Count, Mesh {i} : {self.colCount[i]}")

		return self.cols

	def getUVS(self, rx3file):
		for i in range(rx3file.Rx3VertexBuffers.Length):
			temp = []
			v = rx3file.Rx3VertexBuffers[i]

			for x in range(v.Vertexes.Length):
				data = [v.Vertexes[x].TextureCoordinates[0].U , v.Vertexes[x].TextureCoordinates[0].V]
				# data = [v.Vertexes[x].TextureCoordinates[0].U , v.Vertexes[x].TextureCoordinates[0].V, v.Vertexes[x].TextureCoordinates[0].Xtra_Value]
				temp.append(data)
			
			self.uvs.append(temp)
			self.uvCount.append(len(self.uvs[i]))
			if len(self.uvs[i]) > 0:
				print(f"UVS U,V,Extra_Value of UV 0, Mesh {i} = {self.uvs[i][0]}")
				print(f"UV Count, Mesh {i} : {self.uvCount[i]}")

		return self.uvs

	def getCollisions(self, rx3file):
		# 160 = 1 > 3 > 9
		# 3
		# 3 X Y Z
		if (rx3file.Rx3CollisionTriMesh != None):
			for i in range(rx3file.Rx3CollisionTriMesh.Length):
				c = rx3file.Rx3CollisionTriMesh[i]
				temp = [] # per available mesh collision  ## eg 160 count
				for x in range(len(c.CollisionTriangles)):
					perCT = []	# per collision triangle  ## eg 3 for each of previous one
					for y in range(len(c.CollisionTriangles[x])):
						tempvar = c.CollisionTriangles[x][y]
						data = [tempvar.X, tempvar.Y, tempvar.Z] #per x y z data in one  # eg 3 for each of previous one
						perCT.append(data)
					temp.append(perCT)

				self.collision.append(temp)
				self.collisionCount.append(len(self.collision[i]))
				if len(self.cols[i]) > 0:
					print(f"Collision X,Y,Z of CollisionTriMesh 0, Mesh {i} = {self.collision[i][0]}")
					print(f"Collision X,Y,Z of CollisionTriMesh 1, Mesh {i} = {self.collision[i][1]}")
					print(f"Collision Count, Mesh {i} : {self.collisionCount[i]}")


		else:
			print(f"No collision data found in file!")

	def loadRx3(self):
		file = self.file
		if file != "":
			f = self.data = self.getDataRx3(file)
	
			mainFile = Rx3File()
			mainFile.Load(file)

			self.meshCount = mainFile.Rx3VertexBuffers.Length
			print(f"Total Mesh Count : {mainFile.Rx3IndexBuffers.Length}")
			#print(mainFile.Rx3IndexBuffers.Length)
			# rx3file.Rx3VertexBuffers.Length => can be used for mesh count
			# rx3file.Rx3IndexBuffers.Length => can also be used for mesh count

			self.endian = mainFile.Rx3Header.Endianness
			if self.endian == "b":
				self.endianType = '>'
				self.endianStr = "Big Endian"
				print(f"Endian Type : {self.endianStr}")
			elif self.endian == "l":
				self.endianType = '<'
				self.endianStr = "Little Endian"
				print(f"Endian Type : {self.endianStr}")

			self.offsets = self.getOffsets(mainFile)

			self.getVertexFormats(mainFile)

			self.getVertexPosition(mainFile)

			self.getNormalCols(mainFile)

			self.getUVS(mainFile)

			self.getIndicesData(mainFile)

			self.getVertexColor(mainFile)

			self.getBoneIndice(mainFile)
			
			self.getBoneWeight(mainFile)

			self.getCollisions(mainFile)

			fcOffset = []
			for x in self.offsets:
				if x[0] == 5798132:
					fcOffset.append(x[1])

			# f.seek(-16, 2)
			# self.primitiveType = int.from_bytes(f.read(1),"little")
			self.primitiveType = mainFile.GetPrimitiveType(0)

			if self.primitiveType == 4:
				print(f"Primitive Type : {self.primitiveType} (TriangleList)")
				for x in range(self.meshCount):
					print(f"Using Face Offset, Mesh {x} : {fcOffset[x]}")
					self.faces.append(self.facereadlist(self.data, fcOffset[x], x, self.indicesLength[x], self.indicesCount[x], self.endianType))
			elif self.primitiveType == 6:
				print(f"Primitive Type : {self.primitiveType} (TriangleFans)") #TriangleStrip
				for x in range(self.meshCount):
					print(f"Using Face Offset, Mesh {x} : {fcOffset[x]}")
					self.faces.append(self.facereadstrip(self.data, fcOffset[x], x, self.indicesLength[x], self.indicesCount[x], self.endianType))
			else:
				print("Unknown Primitive Type")


		else:
			print("Please choose the model file.")

	#endregion

	#region Exporter

	def saveRx3(self, rx3file):
		file = rx3file + ".rx3"
		
		if file != "":
			outFile = open(file, 'wb+')
		else:
			print(f"Please specify the export directory.")

	#endregion

class RX3_File_Hybrid():
	def __init__(self, file, gtype): 
		# file info
		self.file = file
		self.fileName = ""
		self.fileExt = ""
		self.filePath = ""
		self.fileType = ""
		self.fileId = 0
		self.gtype = gtype
		# file info end
		self.cols = []  ## Normal / Binormals / Tangent Cols
		self.colCount = []
		self.collision = []
		self.collisionCount = []
		self.data = 0
		self.endian = ""
		self.endianStr = ""
		self.endianType = ""
		self.faces= []
		self.faceCount = []
		self.indicesCount = []
		self.indicesLength = []
		self.offsets = []
		self.meshCount = 0
		self.primitiveType = 0
		self.uvs = []
		self.uvCount = []
		self.vertexFormat = []
		self.vertexPosition = []
		self.totalVertCount = []
		self.vertexSize = []
		self.vertexColor = [] ## was used bone_c in it on original addon
		self.vertexColorCount = [] ## was used bone_c in it on original addon
		#bones section
		# -> 4 bones/vertex : FIFA 11 - 14
		# -> 8 bones/vertex : FIFA 15-16
		self.bonesIndice = [] ## was also used as bone_i in original addon
		self.bonesIndicecount = [] ## was also used as bone_i in original addon
		self.bonesWeight = [] ## was also used as bone_w in original addon
		self.bonesWeightcount = []## was also used as bone_w in original addon
		#bones section end

		# Get file infos
		fI = GetFileType(self.file)
		if fI != "corrupt_filename":
			self.fileName = fI[0]
			self.fileExt = fI[1]
			self.fileType = fI[2]
			self.fileId = fI[3]
			self.filePath = fI[4]
			## Load Rx3
			if GetRX3FileType(self.gtype) == FileType.RX3_Hybrid:
				if self.fileExt == ".rx3":
					self.loadRx3()
				else:
					print(f"\n[ERROR] File {self.file} is not valid RX3 file.")
			else:
				print(f"\n[ERROR] Game {self.gtype} is not valid supported game or wrong file loaded here.")
		else:
			print(f"\n[ERROR] File {self.file} is not valid RX3 file or wrong file loaded here.")

	#region Importer

	def getDataRx3(self, file):
		data = open(file, 'rb')

		print(f"\nFile : {self.fileName+self.fileExt}")
		print(f"File ID : {self.fileId}")
		print(f"File Type : {self.fileType}")
		print(f"File Path : {self.filePath}\n")

		if str(data.read(8))[2:-1] == 'chunkzip':
			t = BytesIO()
			data.read(12)
			sec_num = struct.unpack('>I', data.read(4))[0]
			data.read(8)
			for i in range(sec_num):
				off = data.tell() % 4
				if off:
					data.read(4 - off)
				sec_found = False
				while 1:
					if not sec_found:
						sec_len = struct.unpack('>I', data.read(4))[0]
					if not sec_len == 0:
						sec_found = True
						continue

				data.read(4)
				data = data.read(sec_len)
				try:
					t.write(zlib.decompress(data, -15))
				except zlib.error:
					return 'corrupt_file'

			data = t

		return data

	def facereadlist(self, f, offset, mID, indicesLength, indicesCount, endian):
		f.seek(offset)
		faces = []
	
		self.faceCount.append(int(indicesCount / 3))

		print(f"Face Count, Mesh {mID}: {self.faceCount[mID]}")

		# this is read in addon to get indicescount and length
		# f.read(4) 
		# f.read(4) # indicescount
		# f.read(1) # indiceslength
		# f.read(3)
		# f.read(4)
		# all read are 16 bytes so...auto doing read of 16

		# > = big endian
		# < = little endian
		f.read(16)

		if indicesLength == 4:
			string = endian + 'III'
		elif indicesLength == 2:
			string = endian + 'HHH'

		for i in range(self.faceCount[mID]):
			temp = struct.unpack(string, f.read(indicesLength * 3))
			if not temp[0] == temp[1]:
				if not temp[2] == temp[1]:
					if temp[0] == temp[2]:
						continue
					faces.append((temp[0], temp[1], temp[2]))

		print(f"Values of Face 0, Mesh {mID}: {faces[0]}")
		return faces

	def facereadstrip(self, f, offset, mID, indicesLength, indicesCount, endian):
		f.seek(offset)
		faces = []
		self.faceCount.append(indicesCount - 2)

		print(f"Face Count, Mesh {mID}: {self.faceCount[mID]}")

		# f.read(4)
		# f.read(4) # indicescount
		# f.read(4) # indiceslength
		# f.read(4)
		# all read are 16 bytes so...auto doing read of 16

		# > = big endian
		# < = little endian
		f.read(16)

		if indicesLength == 4:
			string = endian + 'III'
		elif indicesLength == 2:
			string = endian + 'HHH'

		flag = False
		for i in range(self.faceCount[mID]):
			back = f.tell()
			temp = struct.unpack(string, f.read(indicesLength * 3))
			if temp[0] == temp[1] or temp[1] == temp[2] or temp[0] == temp[2]:
				flag = not flag
				f.seek(back + indicesLength)
				continue
			elif flag is False:
				faces.append((temp[0], temp[1], temp[2]))
			elif flag is True:
				faces.append((temp[2], temp[1], temp[0]))
			flag = not flag
			f.seek(back + indicesLength)

		print(f"Values of Face 0, Mesh {mID}: {faces[0]}")
		return faces

	def getOffsets(self, rx3file):
		obtainedOffsets = []
		sect_num  = rx3file.Rx3Header.NumSections
		print('Number of Sectors Detected : ', sect_num)

		# blender offset[0] -> rx3file.Rx2SectionHeaders(id).Signature (= section hashed name) 
		# blender offset[1] -> rx3file.Rx2SectionHeaders(id).Offset (= where the section starts in file)

		for x in range(0, sect_num):
			obtainedOffsets.append([rx3file.Rx3SectionHeaders[x].Signature, rx3file.Rx3SectionHeaders[x].Offset])

		print(f"Offsets : {obtainedOffsets}")
		
		return obtainedOffsets

	def getVertexFormats(self, rx3file):
		# RW4VertexDescriptors

		for x in range(rx3file.RW4Section.RW4VertexDescriptors.Length):
			print(f"Total Vertex Elements, Mesh {x} : {rx3file.RW4Section.RW4VertexDescriptors[x].NumElements}")
			for y in range(rx3file.RW4Section.RW4VertexDescriptors[x].Elements.Length):
				temp0 = rx3file.RW4Section.RW4VertexDescriptors[x].Elements[y]
				# usage, usageIndex, offset, unk0, dataType
				temp1 = f"{temp0.Usage, temp0.UsageIndex, temp0.Offset, 0, temp0.DataType}"
				self.vertexFormat.append(temp1)

		print(f"Vertex Formats : {self.vertexFormat}")
		return self.vertexFormat

	def getVertexPosition(self, rx3file):
		for i in range(rx3file.Rx3VertexBuffers.Length):
			temp = []
			v = rx3file.Rx3VertexBuffers[i]

			self.totalVertCount.append(v.NumVertices)
			# self.totalVertCount.append(v.Vertexes.Length)
			print(f"Total Vertices Count, Mesh {i} : {self.totalVertCount[i]}")

			self.vertexSize.append(v.VertexSize)
			print(f"Total Vertex Size, Mesh {i} : {self.vertexSize[i]}")

			for x in range(v.Vertexes.Length):
				data = [v.Vertexes[x].Positions[0].X/100 , -v.Vertexes[x].Positions[0].Z/100, v.Vertexes[x].Positions[0].Y/100]
				# data = [v.Vertexes[x].Positions[0].X/100 , -v.Vertexes[x].Positions[0].Z/100, v.Vertexes[x].Positions[0].Y/100, v.Vertexes[x].Positions[0].W]
				temp.append(data)
			
			self.vertexPosition.append(temp)
			print(f"Position X,Z,Y,W of Vertex 0, Mesh {i} = {self.vertexPosition[i][0]}")

		return self.vertexPosition

	def getIndicesData(self, rx3file):
		# rx3model.Rx3IndexBuffer(meshid) ==> For faces
		# rx3model.Rx3IndexBuffer(meshid).Rx3IndexBufferHeader.IndexSize is the same as "indiceslength" in your code
		for i in range( rx3file.Rx3IndexBuffers.Length):
			indices = rx3file.Rx3IndexBuffers[i]

			self.indicesCount.append(indices.IndexStream.Length)
			print(f"Incides Count, Mesh {i} : {self.indicesCount[i]}")

			self.indicesLength.append(indices.Rx3IndexBufferHeader.IndexSize)
			print(f"Indices Length, Mesh {i} : {self.indicesLength[i]}")

		return [self.indicesCount, self.indicesLength]

	def getVertexColor(self, rx3file): #was also used as bone_c in original addon
		for i in range(rx3file.Rx3VertexBuffers.Length):
			temp = []
			v = rx3file.Rx3VertexBuffers[i]

			for x in range(v.Vertexes.Length):
				if (v.Vertexes[x].Colors != None) :
					data = [v.Vertexes[x].Colors[0].Value_R , v.Vertexes[x].Colors[0].Value_G, v.Vertexes[x].Colors[0].Value_B]
					# data = [v.Vertexes[x].Colors[0].Value_R , v.Vertexes[x].Colors[0].Value_G, v.Vertexes[x].Colors[0].Value_B, v.Vertexes[x].Colors[0].Value_A]
					temp.append(data)
				else:
					print(f"No Vertex Color Found in Mesh {i}!")
					break
			
			self.vertexColor.append(temp)
			self.vertexColorCount.append(len(self.vertexColor[i]))
			if len(self.vertexColor[i]) > 0:
				print(f"Color R,G,B,A of Vertex Color 0, Mesh {i} = {self.vertexColor[i][0]}")
				print(f"Vertex Color Count, Mesh {i} : {self.vertexColorCount[i]}")
		
		return self.vertexColor
	
	def getBoneIndice(self, rx3file): #was also used as bone_i in original addon
		for i in range(rx3file.Rx3VertexBuffers.Length):
			temp = []
			v = rx3file.Rx3VertexBuffers[i]

			if (v.Vertexes[0].BlendIndices != None) :
				print(f"Total Blend Indices Set : [{v.Vertexes[0].BlendIndices.Length}]")
			
			for x in range(v.Vertexes.Length):
				if (v.Vertexes[x].BlendIndices != None) :
					vertexdata = []
					for y in range(v.Vertexes[x].BlendIndices.Length):
						tempdata = [v.Vertexes[x].BlendIndices[y].Index_1 , v.Vertexes[x].BlendIndices[y].Index_2, v.Vertexes[x].BlendIndices[y].Index_3, v.Vertexes[x].BlendIndices[y].Index_4]
						vertexdata.append(tempdata)
					temp.append(vertexdata)
				else:
					print(f"No Bone Indices Found in Mesh {i}!")
					break
			
			self.bonesIndice.append(temp)
			self.bonesIndiceCount.append(len(self.bonesIndice[i]))
			if len(self.bonesIndice[i]) > 0:
				print(f"Bone Indice Index 1,2,3,4 of Vertex Bone 0, Mesh {i} = {self.bonesIndice[i][0]}")
				print(f"Bone Indice Count, Mesh {i} : {self.bonesIndiceCount[i]}")
		
		return self.bonesIndice
	
	def getBoneWeight(self, rx3file): #was also used as bone_w in original addon
		for i in range(rx3file.Rx3VertexBuffers.Length):
			temp = []
			v = rx3file.Rx3VertexBuffers[i]

			if (v.Vertexes[0].BlendWeights != None) :
				print(f"Total Blend Weights Set : [{v.Vertexes[0].BlendWeights.Length}]")
			

			for x in range(v.Vertexes.Length):
				if (v.Vertexes[x].BlendWeights != None) :
					vertexdata = []
					for y in range(v.Vertexes[x].BlendWeights.Length):
						tempdata = [v.Vertexes[x].BlendWeights[y].Weight_1 , v.Vertexes[x].BlendWeights[y].Weight_2, v.Vertexes[x].BlendWeights[y].Weight_3, v.Vertexes[x].BlendWeights[y].Weight_4]
						vertexdata.append(tempdata)
					temp.append(vertexdata)
				else:
					print(f"No Bone Weights Found in Mesh {i}!")
					break
			
			self.bonesWeight.append(temp)
			self.bonesWeightCount.append(len(self.bonesWeight[i]))
			if len(self.bonesWeight[i]) > 0:
				print(f"Bone Weights 1,2,3,4 of Vertex Bone 0, Mesh {i} = {self.bonesWeight[i][0]}")
				print(f"Bone Weights Count, Mesh {i} : {self.bonesWeightCount[i]}")
		
		return self.bonesWeight

	def getNormalCols(self, rx3file):
		for i in range(rx3file.Rx3VertexBuffers.Length):
			temp = []
			v = rx3file.Rx3VertexBuffers[i]

			for x in range(v.Vertexes.Length):
				#normals / n
				if v.Vertexes[x].Normals != None:
					data1 = [v.Vertexes[x].Normals[0].Normal_x , v.Vertexes[x].Normals[0].Normal_y, v.Vertexes[x].Normals[0].Normal_z]
					# data1 = [v.Vertexes[x].Normals[0].Normal_x , v.Vertexes[x].Normals[0].Normal_y, v.Vertexes[x].Normals[0].Normal_z, v.Vertexes[x].Normals[0].DEC3N]
					temp.append(data1)
				#binormals / b
				if v.Vertexes[x].Binormals != None:
					data2 = [v.Vertexes[x].Binormals[0].Binormal_x , v.Vertexes[x].Binormals[0].Binormal_y, v.Vertexes[x].Binormals[0].Binormal_z]
					# data2 = [v.Vertexes[x].Binormals[0].Binormal_x , v.Vertexes[x].Binormals[0].Binormal_y, v.Vertexes[x].Binormals[0].Binormal_z, v.Vertexes[x].Binormals[0].DEC3N]
					temp.append(data2)
				#tangent / g
				if v.Vertexes[x].Tangents != None:
					data3 = [v.Vertexes[x].Tangents[0].Tangent_x , v.Vertexes[x].Tangents[0].Tangent_y, v.Vertexes[x].Tangents[0].Tangent_z]
					# data3 = [v.Vertexes[x].Tangents[0].Tangent_x , v.Vertexes[x].Tangents[0].Tangent_y, v.Vertexes[x].Tangents[0].Tangent_z, v.Vertexes[x].Tangents[0].DEC3N]
					temp.append(data3)
			
			self.cols.append(temp)
			self.colCount.append(len(self.cols[i]))
			if len(self.cols[i]) > 0:
				print(f"Color X,Y,Z,DEC3N of Col 0, Mesh {i} = {self.cols[i][0]}")
				print(f"Color X,Y,Z,DEC3N of Col 1, Mesh {i} = {self.cols[i][1]}")
				print(f"Color X,Y,Z,DEC3N of Col 2, Mesh {i} = {self.cols[i][2]}")
				print(f"Color Count, Mesh {i} : {self.colCount[i]}")

		return self.cols

	def getUVS(self, rx3file):
		for i in range(rx3file.Rx3VertexBuffers.Length):
			temp = []
			v = rx3file.Rx3VertexBuffers[i]

			for x in range(v.Vertexes.Length):
				data = [v.Vertexes[x].TextureCoordinates[0].U , v.Vertexes[x].TextureCoordinates[0].V]
				# data = [v.Vertexes[x].TextureCoordinates[0].U , v.Vertexes[x].TextureCoordinates[0].V, v.Vertexes[x].TextureCoordinates[0].Xtra_Value]
				temp.append(data)
			
			self.uvs.append(temp)
			self.uvCount.append(len(self.uvs[i]))
			if len(self.uvs[i]) > 0:
				print(f"UVS U,V,Extra_Value of UV 0, Mesh {i} = {self.uvs[i][0]}")
				print(f"UV Count, Mesh {i} : {self.uvCount[i]}")

		return self.uvs

	def getCollisions(self, rx3file):
		# 160 = 1 > 3 > 9
		# 3
		# 3 X Y Z
		if (rx3file.Rx3CollisionTriMesh != None):
			for i in range(rx3file.Rx3CollisionTriMesh.Length):
				c = rx3file.Rx3CollisionTriMesh[i]
				temp = [] # per available mesh collision  ## eg 160 count
				for x in range(len(c.CollisionTriangles)):
					perCT = []	# per collision triangle  ## eg 3 for each of previous one
					for y in range(len(c.CollisionTriangles[x])):
						tempvar = c.CollisionTriangles[x][y]
						data = [tempvar.X, tempvar.Y, tempvar.Z] #per x y z data in one  # eg 3 for each of previous one
						perCT.append(data)
					temp.append(perCT)

				self.collision.append(temp)
				self.collisionCount.append(len(self.collision[i]))
				if len(self.cols[i]) > 0:
					print(f"Collision X,Y,Z of CollisionTriMesh 0, Mesh {i} = {self.collision[i][0]}")
					print(f"Collision X,Y,Z of CollisionTriMesh 1, Mesh {i} = {self.collision[i][1]}")
					print(f"Collision Count, Mesh {i} : {self.collisionCount[i]}")


		else:
			print(f"No collision data found in file!")

	def loadRx3(self):
		file = self.file
		if file != "":
			f = self.data = self.getDataRx3(file)
	
			mainFile = Rx3File()
			mainFile.Load(file)

			self.meshCount = mainFile.Rx3VertexBuffers.Length
			print(f"Total Mesh Count : {mainFile.Rx3IndexBuffers.Length}")
			#print(mainFile.Rx3IndexBuffers.Length)
			# rx3file.Rx3VertexBuffers.Length => can be used for mesh count
			# rx3file.Rx3IndexBuffers.Length => can also be used for mesh count

			self.endian = mainFile.RW4Section.RW4Header.Endianness
			if self.endian == 1:
				self.endian = "b"
				self.endianType = '>'
				self.endianStr = "Big Endian"
				print(f"Endian Type : {self.endianStr}")
			elif self.endian == 0:
				self.endian = "l"
				self.endianType = '<'
				self.endianStr = "Little Endian"
				print(f"Endian Type : {self.endianStr}")

			self.offsets = self.getOffsets(mainFile)

			self.getVertexFormats(mainFile)

			self.getVertexPosition(mainFile)

			self.getNormalCols(mainFile)

			self.getUVS(mainFile)

			self.getIndicesData(mainFile)

			self.getVertexColor(mainFile)

			self.getBoneIndice(mainFile)
			
			self.getBoneWeight(mainFile)

			self.getCollisions(mainFile)

			fcOffset = []
			for x in self.offsets:
				if x[0] == 5798132:
					fcOffset.append(x[1])

			self.primitiveType = mainFile.GetPrimitiveType(0)
			# self.primitiveType = mainFile.RW4Section.RW4Shader_FxRenderableSimples[0].PrimitiveType

			if self.primitiveType == 4:
				print(f"Primitive Type : {self.primitiveType} (TriangleList)")
				for x in range(self.meshCount):
					print(f"Using Face Offset, Mesh {x} : {fcOffset[x]}")
					self.faces.append(self.facereadlist(self.data, fcOffset[x], x, self.indicesLength[x], self.indicesCount[x], self.endianType))
			elif self.primitiveType == 6:
				print(f"Primitive Type : {self.primitiveType} (TriangleFans)") #TriangleStrip
				for x in range(self.meshCount):
					print(f"Using Face Offset, Mesh {x} : {fcOffset[x]}")
					self.faces.append(self.facereadstrip(self.data, fcOffset[x], x, self.indicesLength[x], self.indicesCount[x], self.endianType))
			else:
				print("Unknown Primitive Type")

		else:
			print("Please choose the model file.")

	#endregion

