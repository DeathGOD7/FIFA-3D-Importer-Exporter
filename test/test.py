from io import BufferedIOBase
from typing import Collection
import clr
import os
import sys
import zlib, struct
import math

sys.path.append(r'.\lib')

clr.AddReference('SE7EN')
ref1 = clr.AddReference('FIFALibrary_v21.11.28.0_x64')
# ref1 = clr.AddReference('FIFALibrary_v21.12.08_beta')

from SE7EN007 import *
from FIFALibrary20 import *
from enum import Enum

class fifa_tools():
	texdir = r"C:\Users\dell\Documents\SE7EN\FIFA 3D\Textures"

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

class TextureFormat(int, Enum):
	DXT1 = 0,
	DXT3 = 1,
	DXT5 = 2,
	A8R8G8B8 = 3,
	GREY8 = 4,
	GREY8ALFA8 = 5,
	RGBA = 6,
	ATI2 = 7,
	ATI1 = 12,
	A4R4G4B4 = 109,
	R5G6B5 = 120,
	X1R5G5B5 = 126,
	BIT8 = 123,
	R8G8B8 = 127

class TextureType(int, Enum):
	TEXTURE_2D = 1,
	TEXTURE_CUBEMAP = 3,
	TEXTURE_VOLUME = 4

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
	temp = fileName.split(sep='_')
	isTex = ("textures" or "texture") in temp
	try:
		fileId = temp[1]
		fileType = temp[0]
		return (fileName, filEext, fileType, fileId, filePath, isTex)
	except:
		return 'corrupt_filename'

def GetTextureFormat(id):
	values = [item.value for item in TextureFormat]
	temp = ""
	if id in values:
		temp = TextureFormat(id).name
	else:
		temp = "Unknown Texture Format"

	return temp

def GetTextureType(id):
	values = [item.value for item in TextureType]
	temp = ""
	if id in values:
		temp = TextureType(id).name
	else:
		temp = "Unknown Texture Format"

	return temp


class RX3_File():
	def __init__(self, file, gtype): 
		# file info
		self.file = file
		self.fileName = ""
		self.fileExt = ""
		self.filePath = ""
		self.fileType = ""
		self.fileId = 0
		self.isTexture = False
		self.gtype = gtype
		# file info end
		
		## Normals
		self.cols_normals = []  
		self.colCount_normals = []
		## Binormals 
		self.cols_binormals = []  
		self.colCount_binormals = []
		## Tangents
		self.cols_tangents = []  
		self.colCount_tangents = []

		self.collision = []
		self.collisionCount = []
		self.data = 0
		self.dataRX3 = Rx3File()
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
		self.rx3Type = ""
		self.skeletonType = ""
		self.bones = []
		self.bonesCount = []
		#texture section
		self.textureCount = 0
		self.textureInfos = []
		self.textureRes = []
		#names
		self.meshNames = []
		self.texNames = []

		# Get file infos
		fI = GetFileType(self.file)
		if fI != "corrupt_filename":
			self.fileName = fI[0]
			self.fileExt = fI[1]
			self.fileType = fI[2]
			self.fileId = fI[3]
			self.filePath = fI[4]
			self.isTexture = fI[5]

			## Load Rx3
			self.rx3Type = GetRX3FileType(self.gtype)
			self.skeletonType = GetSkeletonType(self.gtype)
			if self.rx3Type == FileType.RX3:
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
		print(f"Texture File? : {self.isTexture}\n")

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
					for y in range(v.Vertexes[x].BlendIndices.Length):
						vertexdata = [v.Vertexes[x].BlendIndices[y].Index_1 , v.Vertexes[x].BlendIndices[y].Index_2, v.Vertexes[x].BlendIndices[y].Index_3, v.Vertexes[x].BlendIndices[y].Index_4]
					temp.append(vertexdata)
				else:
					print(f"No Bone Indices Found in Mesh {i}!")
					break
			
			self.bonesIndice.append(temp)
			self.bonesIndiceCount.append(len(self.bonesIndice[i]))
			if len(self.bonesIndice[i]) > 0:
				print(f"Bone Indice Index 1,2,3,4 of Vertex Bone 0, Mesh {i} = {self.bonesIndice[i][0]}")
				print(f"Bone Indice Index 1,2,3,4 of Vertex Bone 1, Mesh {i} = {self.bonesIndice[i][1]}")
				print(f"Bone Indice Index 1,2,3,4 of Vertex Bone 2, Mesh {i} = {self.bonesIndice[i][2]}")
				print(f"Bone Indice Index 1,2,3,4 of Vertex Bone 3, Mesh {i} = {self.bonesIndice[i][3]}")
				print(f"Bone Indice Index 1,2,3,4 of Vertex Bone 4, Mesh {i} = {self.bonesIndice[i][4]}")
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
					for y in range(v.Vertexes[x].BlendWeights.Length):
						vertexdata = [v.Vertexes[x].BlendWeights[y].Weight_1 , v.Vertexes[x].BlendWeights[y].Weight_2, v.Vertexes[x].BlendWeights[y].Weight_3, v.Vertexes[x].BlendWeights[y].Weight_4]
					temp.append(vertexdata)
				else:
					print(f"No Bone Weights Found in Mesh {i}!")
					break
			
			self.bonesWeight.append(temp)
			self.bonesWeightCount.append(len(self.bonesWeight[i]))
			if len(self.bonesWeight[i]) > 0:
				print(f"Bone Weights 1,2,3,4 of Vertex Bone 0, Mesh {i} = {self.bonesWeight[i][0]}")
				print(f"Bone Weights 1,2,3,4 of Vertex Bone 1, Mesh {i} = {self.bonesWeight[i][1]}")
				print(f"Bone Weights 1,2,3,4 of Vertex Bone 2, Mesh {i} = {self.bonesWeight[i][2]}")
				print(f"Bone Weights 1,2,3,4 of Vertex Bone 3, Mesh {i} = {self.bonesWeight[i][3]}")
				print(f"Bone Weights 1,2,3,4 of Vertex Bone 4, Mesh {i} = {self.bonesWeight[i][4]}")
				print(f"Bone Weights Count, Mesh {i} : {self.bonesWeightCount[i]}")
		
		return self.bonesWeight

	def getNormalCols(self, rx3file):
		for i in range(rx3file.Rx3VertexBuffers.Length):
			temp1 = [] #normals
			temp2 = [] #binromals
			temp3 = [] #tangents
			v = rx3file.Rx3VertexBuffers[i]

			for x in range(v.Vertexes.Length):
				#normals / n
				if v.Vertexes[x].Normals != None:
					data1 = [v.Vertexes[x].Normals[0].Normal_x , v.Vertexes[x].Normals[0].Normal_y, v.Vertexes[x].Normals[0].Normal_z]
					# data1 = [v.Vertexes[x].Normals[0].Normal_x , v.Vertexes[x].Normals[0].Normal_y, v.Vertexes[x].Normals[0].Normal_z, v.Vertexes[x].Normals[0].DEC3N]
					temp1.append(data1)
				#binormals / b
				if v.Vertexes[x].Binormals != None:
					data2 = [v.Vertexes[x].Binormals[0].Binormal_x , v.Vertexes[x].Binormals[0].Binormal_y, v.Vertexes[x].Binormals[0].Binormal_z]
					# data2 = [v.Vertexes[x].Binormals[0].Binormal_x , v.Vertexes[x].Binormals[0].Binormal_y, v.Vertexes[x].Binormals[0].Binormal_z, v.Vertexes[x].Binormals[0].DEC3N]
					temp2.append(data2)
				#tangent / g
				if v.Vertexes[x].Tangents != None:
					data3 = [v.Vertexes[x].Tangents[0].Tangent_x , v.Vertexes[x].Tangents[0].Tangent_y, v.Vertexes[x].Tangents[0].Tangent_z]
					# data3 = [v.Vertexes[x].Tangents[0].Tangent_x , v.Vertexes[x].Tangents[0].Tangent_y, v.Vertexes[x].Tangents[0].Tangent_z, v.Vertexes[x].Tangents[0].DEC3N]
					temp3.append(data3)
			
			self.cols_normals.append(temp1)
			self.cols_binormals.append(temp2)
			self.cols_tangents.append(temp3)

			self.colCount_normals.append(len(self.cols_normals[i]))
			self.colCount_binormals.append(len(self.cols_binormals[i]))
			self.colCount_tangents.append(len(self.cols_tangents[i]))


			if len(self.cols_normals[i]) > 0:
				print(f"Color X,Y,Z,DEC3N of Normal Col 0, Mesh {i} = {self.cols_normals[i][0]}")
				print(f"Color X,Y,Z,DEC3N of Normal Col 1, Mesh {i} = {self.cols_normals[i][1]}")
				print(f"Color X,Y,Z,DEC3N of Normal Col 2, Mesh {i} = {self.cols_normals[i][2]}")
				print(f"Normal Color Count, Mesh {i} : {self.colCount_normals[i]}")

			if len(self.cols_binormals[i]) > 0:
				print(f"Color X,Y,Z,DEC3N of Binormal Col 0, Mesh {i} = {self.cols_binormals[i][0]}")
				print(f"Color X,Y,Z,DEC3N of Binormal Col 1, Mesh {i} = {self.cols_binormals[i][1]}")
				print(f"Color X,Y,Z,DEC3N of Binormal Col 2, Mesh {i} = {self.cols_binormals[i][2]}")
				print(f"Binormal Color Count, Mesh {i} : {self.colCount_binormals[i]}")

			if len(self.cols_tangents[i]) > 0:
				print(f"Color X,Y,Z,DEC3N of Tangent Col 0, Mesh {i} = {self.cols_tangents[i][0]}")
				print(f"Color X,Y,Z,DEC3N of Tangent Col 1, Mesh {i} = {self.cols_tangents[i][1]}")
				print(f"Color X,Y,Z,DEC3N of Tangent Col 2, Mesh {i} = {self.cols_tangents[i][2]}")
				print(f"Tangent Color Count, Mesh {i} : {self.colCount_tangents[i]}")

		return self.cols_normals, self.cols_binormals, self.cols_tangents

	def getUVS(self, rx3file):
		for i in range(rx3file.Rx3VertexBuffers.Length):
			temp = []
			v = rx3file.Rx3VertexBuffers[i]

			for x in range(v.Vertexes.Length):
				if (v.Vertexes[x].TextureCoordinates != None) :
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
		# 1
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
				if len(self.collision[i]) > 0:
					print(f"Collision X,Y,Z of CollisionTriMesh 0, Mesh {i} = {self.collision[i][0]}")
					print(f"Collision X,Y,Z of CollisionTriMesh 1, Mesh {i} = {self.collision[i][1]}")
					print(f"Collision Count, Mesh {i} : {self.collisionCount[i]}")

			return self.collision

		else:
			print(f"No collision data found in file!")

	def getBones(self, rx3file):
		if (rx3file.Rx3AnimationSkins != None):
			for i in range(rx3file.Rx3AnimationSkins.Length):
				temp = []
				v = rx3file.Rx3AnimationSkins[i]

				self.bonesCount.append(v.NumBones)

				# perBM = []  
				for x in range(len(v.BoneMatrices)):
					if (v.BoneMatrices[x] != None) :
						aBP = v.BoneMatrices[x].absBindPose
						iPT = v.BoneMatrices[x].invPoseTranslation
						bonedata = [aBP, [iPT.X , iPT.Y, iPT.Z]]
						# perBM.append(bonedata)
						temp.append(bonedata)
					else:
						print(f"No Bone Matrices Found in Meshes!")
						break
				
				
				self.bones.append(temp)
				if len(self.bones[i]) > 0:
					print(f"Bone Matrices X,Y,Z of Bone 0, All Mesh = {self.bones[i][0]}")
					print(f"Bone Matrices X,Y,Z of Bone 1, All Mesh = {self.bones[i][1]}")
					print(f"Bone Matrices X,Y,Z of Bone 2, All Mesh = {self.bones[i][2]}")
					print(f"Bone Matrices X,Y,Z of Bone 3, All Mesh = {self.bones[i][3]}")
					print(f"Bone Matrices Count, All Mesh : {self.bonesCount[i]}")
				
				break 
			
			return self.bones

		else:
			print(f"No Animation data found in file!")

	def getTextures(self, rx3file):
		texdir = fifa_tools.texdir

		self.textureCount = rx3file.Rx3Textures.Length

		for x in range(self.textureCount):
			temp = rx3file.Rx3Textures[x]
			temp1 = [temp.Rx3TextureHeader.Width, temp.Rx3TextureHeader.Height]
			
			self.texNames.append(rx3file.Rx3NameTable.Names[x].Name.replace(".Raster", ""))
			
			tF = GetTextureFormat(temp.Rx3TextureHeader.TextureFormat)
			tT = GetTextureType(temp.Rx3TextureHeader.TextureType)
			tS = temp.Rx3TextureHeader.TotalSize / 1024
			if tS >= 1024:
				tS = f"{math.ceil(tS / 1024)} MB"
			else:
				tS = f"{math.ceil(tS)} KB"
			
			
			temp2 = [self.texNames[x], tF, tT, tS, f"{temp.Rx3TextureHeader.NumLevels} Mipmaps", f"{temp.Rx3TextureHeader.NumFaces} Tex Faces"]
			
			self.textureRes.append(temp1)
			self.textureInfos.append(temp2)

			print(f"Texture {x} Resolution : {self.textureRes[x]}")
			print(f"Texture {x} Info : {self.textureInfos[x]}")
		
			# texture file extractor
			ddsfile = temp.GetDds()
			ddsfile.Save(f"{texdir}/{self.texNames[x]}.dds")			

	def loadRx3(self):
		file = self.file
		if file != "":
			f = self.data = self.getDataRx3(file)
	
			self.dataRX3.Load(file)

			for x in range(self.dataRX3.Rx3IndexBuffers.Length):
				print(self.dataRX3.Rx3IndexBuffers[x].IndexStream.Length)
				f = open("allindices__dll_new.txt", "w+")
				for y in range(self.dataRX3.Rx3IndexBuffers[x].IndexStream.Length):
					f.writelines(str(self.dataRX3.Rx3IndexBuffers[x].IndexStream[y]) + ", ")


			self.endian = self.dataRX3.Rx3Header.Endianness
			if self.endian == "b":
				self.endianType = '>'
				self.endianStr = "Big Endian"
				print(f"Endian Type : {self.endianStr}")
			elif self.endian == "l":
				self.endianType = '<'
				self.endianStr = "Little Endian"
				print(f"Endian Type : {self.endianStr}")
			
			self.offsets = self.getOffsets(self.dataRX3)

			if not self.isTexture:
				self.meshCount = self.dataRX3.Rx3VertexBuffers.Length
				print(f"Total Mesh Count : {self.dataRX3.Rx3IndexBuffers.Length}")

				for x in range(self.meshCount):
					# temp = self.dataRX3.Rx3NameTable.Names[x].Name.split(sep="_")
					temp = self.dataRX3.Rx3NameTable.Names[x].Name
					self.meshNames.append(temp)

				self.getVertexFormats(self.dataRX3)

				self.getVertexPosition(self.dataRX3)

				self.getNormalCols(self.dataRX3)

				self.getUVS(self.dataRX3)

				self.getIndicesData(self.dataRX3)

				self.getVertexColor(self.dataRX3)

				self.getBoneIndice(self.dataRX3)
				
				self.getBoneWeight(self.dataRX3)

				self.getCollisions(self.dataRX3)

				self.getBones(self.dataRX3)

				fcOffset = []
				for x in self.offsets:
					if x[0] == 5798132:
						fcOffset.append(x[1])

				# f.seek(-16, 2)
				# self.primitiveType = int.from_bytes(f.read(1),"little")
				self.primitiveType = self.dataRX3.GetPrimitiveType(0)

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
				self.getTextures(self.dataRX3)



		else:
			print("Please choose the model file.")

	#endregion

	#region Exporter
	
	def GetVertex(self, vertex):
		temp = [] # mesh

		# obtained data from dll
		# from dll = x, y, z
		# for blender = x, z, y

		# obtained data from blender
		# from blender = x, y, z
		# for dll = x, z, y

		for x in range(len(vertex)):
			tmp1 = []
			for y in vertex[x]:
				tmp1.append(y)
			temp.append(tmp1)

		return temp
	
	def GetIndice(self, indice):
		temp = [] # mesh
		for x in range(len(indice)):
			for y in indice[x]:
				temp.append(y)

		return temp
	
	def GetCols(self, normalscol, binormalscol, tangentscol, meshid, rx3file):
		v = rx3file.Rx3VertexBuffers[meshid]

		hasnormal = False
		hasbinormals = False
		hastangents = False
		if v.Vertexes[meshid].Normals != None:
			hasnormal = True
			print("Normals : " + str(hasnormal))
		if v.Vertexes[meshid].Binormals != None:
			hasbinormals = True
			print("Binormals : " + str(hasbinormals))
		if v.Vertexes[meshid].Tangents != None:
			hastangents = True
			print("Tangents : " + str(hastangents))


		normals = [] # mesh per cols
		binormals = [] # mesh per cols
		tangents = [] # mesh per cols

		if hasnormal:
			print("Has normal cols")
			for x in range(0, len(normalscol), 1):
				for y in normalscol[x]:
					tmp1 = [y[0], y[1], y[2]]
					normals.append(tmp1)

			# for x in range(len(normals) - )

		if hasbinormals:
			print("Has binormals cols")
			for x in range(0, len(binormalscol), 1):
				for y in binormalscol[x]:
					tmp1 = [y[0], y[1], y[2]]
					binormals.append(tmp1)

		if hastangents:
			print("Has tangents cols")
			for x in range(0, len(tangentscol), 1):
				for y in tangentscol[x]:
					tmp1 = [y[0], y[1], y[2]]
					tangents.append(tmp1)


		return normals, binormals, tangents
		
	def GetUVs(self, uvs):
		temp = []
		for x in range(len(uvs)):
			for y in uvs[x]:
				tmp1 = [y[0], y[1]]
				temp.append(tmp1)

		return temp
	
	### WRITING FILE ###

	def WriteVertexData(self, meshid, vertex, uvs, normals, binormals, tangents, rx3file):
		v = rx3file.Rx3VertexBuffers[meshid]
		vlengthold = v.Vertexes.Length
		vlengthnew = len(vertex)
		newvertex = vlengthnew - vlengthold

		print(f"old vertex length : {vlengthold}")
		print(f"new vertex length : {vlengthnew}")
		print(f"new uvs length : {len(uvs)}")
		print(f"new normal cols length : {len(normals)}")
		print(f"new binormals cols length : {len(binormals)}")
		print(f"new tangents cols length : {len(tangents)}")
		# if (v.)



		# [v.Vertexes[x].BlendWeights[y].Weight_1
		# vertexdata = [v.Vertexes[x].BlendIndices[y].Index_1



			# 	if (rx3file.Rx3AnimationSkins != None):
			# for i in range(rx3file.Rx3AnimationSkins.Length):
			# 	temp = []
			# 	v = rx3file.Rx3AnimationSkins[i]

		
		hasnormal = False
		hasbinormals = False
		hastangents = False
		if v.Vertexes[meshid].Normals != None:
			hasnormal = True
		if v.Vertexes[meshid].Binormals != None:
			hasbinormals = True
		if v.Vertexes[meshid].Tangents != None:
			hastangents = True
		
		# v.Vertexes.Clear()   # 0 - x


		collection = []
		for x in range(len(vertex)):
			vrt = Vertex()

			## pos
			pos = Position()
			# pos.X = vertex[x][0]  # 0 - x
			# pos.Y = vertex[x][2]  # 2 - y
			# pos.Z = -vertex[x][1]  # 1 - z

			pos.X = vertex[x][0]  # 0 - x
			pos.Y = vertex[x][1]  # 1 - y
			pos.Z = vertex[x][2]  # 2 - z

			vrt.Positions = [pos]


			## uvs
			TextureCoord = TextureCoordinate()
			TextureCoord.U = uvs[x][0]
			TextureCoord.V = uvs[x][1]

			vrt.TextureCoordinates = [TextureCoord]


			## cols

			fc = FifaUtil()


			if hasnormal:
				#normals / n
				normal = Normal()
				normal.DEC3N = fc.FloatsToDEC3N(normals[x][0],normals[x][1],normals[x][2])


			if hasbinormals:
				#binormals / b
				binormal = Binormal()
				binormal.DEC3N = fc.FloatsToDEC3N(binormals[x][0],binormals[x][1],binormals[x][2])

			if hastangents:
				#tangent / g
				tangent = Tangent()
				tangent.DEC3N = fc.FloatsToDEC3N(tangents[x][0],tangents[x][1],tangents[x][2])



			if hasnormal:
				vrt.Normals = [normal]
			
			if hasbinormals:
				vrt.Binormals = [binormal]
			
			if hastangents:
				vrt.Tangents = [tangent]


			collection.append(vrt)

		
		v.Vertexes = collection


	def WriteIndice(self, meshid, indice, rx3file):
		i = rx3file.Rx3IndexBuffers[meshid]
		# i.IndexStream.Clear()
		print(f"indice length : {len(indice)}")
		i.IndexStream = indice


	def saveRx3(self, fileloc, game, mesh):
		outDirectory = fileloc
		test = True
		
		if outDirectory != "":
			file = outDirectory + f"\\{self.fileType}_0_0.rx3"

			if test:
				game = "FIFA 14"
				lfile = r"C:\Users\dell\Documents\SE7EN\FIFA 3D\Logs\testlogs.log"
				log = open(lfile, "a+")
				logmessage = open(r"E:\SE7EN\Github\FIFA 3D Importer Exporter\fifa_tools\scripts\msg","r")
			else:
				game = game
				log = fifa_tools.globalLogFile
				logmessage = open(fifa_tools.addonLoc + r"\fifa_tools\scripts\msg", "r")

			if (game == self.gtype):
				print(f"Exporting File : {file}")
				
				## for each mesh in obj get its data
				if (self.meshCount != len(mesh)):
					log.writeLog("Mesh count is different from what you loaded. Please do each file seperately.", "INFO")
					return
				
				temp = []
				for x in range(len(mesh)):
					v = self.dataRX3.Rx3VertexBuffers[x]
					hasnormal = False
					hasbinormals = False
					hastangents = False
					if v.Vertexes[x].Normals != None:
						hasnormal = True
					if v.Vertexes[os.X_OK].Binormals != None:
						hasbinormals = True
					if v.Vertexes[x].Tangents != None:
						hastangents = True
					temp.append(ConvertMeshToData(mesh[x], hasnormal, hasbinormals, hastangents))

				vertex = []
				indice = []
				uvs = []
				normals = [] #  per cols
				binormals = [] #  per cols
				tangents = [] #  per cols

				for x in range(len(temp)):
					# get vertex 0
					print(f"Getting Vertex for Mesh {x}")
					log.writeLog(f"Getting Vertex for Mesh {x}", "INFO")

					vertex.append(self.GetVertex(temp[x][0]))

					## get indice 1
					print(f"Getting Indice for Mesh {x}")
					log.writeLog(f"Getting Indice for Mesh {x}", "INFO")

					indice.append(self.GetIndice(temp[x][1]))

					### get uvs 2
					print(f"Getting UVs for Mesh {x}")
					log.writeLog(f"Getting UVs for Mesh {x}", "INFO")

					uvs.append(self.GetUVs(temp[x][2]))

					#### get cols 3
					print(f"Getting Cols for Mesh {x}")
					log.writeLog(f"Getting Cols for Mesh {x}", "INFO")

					t0 = temp[x][3]
					t1 = temp[x][4]
					t2 = temp[x][5]

					te = self.GetCols(t0, t1, t2, x, self.dataRX3)
					normals.append(te[0])
					binormals.append(te[1])
					tangents.append(te[2])

				for x in range(self.meshCount):
					# (meshid, vertex, uvs, normals, binormals, tangents, rx3file):
					self.WriteVertexData(x, vertex[x], uvs[x], normals[x], binormals[x], tangents[x], self.dataRX3)
					self.WriteIndice(x, indice[x], self.dataRX3)

					# TriangleFan = 6,
					# TriangleList = 4,

					self.dataRX3.Rx3SimpleMeshes[x].PrimitiveType = 4


				self.dataRX3.Save(file)

			else:
				lines = logmessage.readlines()
				for line in lines:
					log.writelines(line)
				
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
		self.isTexture = False
		self.gtype = gtype
		# file info end
		
		## Normals
		self.cols_normals = []  
		self.colCount_normals = []
		## Binormals 
		self.cols_binormals = []  
		self.colCount_binormals = []
		## Tangents
		self.cols_tangents = []  
		self.colCount_tangents = []
		
		self.collision = []
		self.collisionCount = []
		self.data = 0
		self.dataRX3 = Rx3File()
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
		self.rx3Type = ""
		self.skeletonType = ""
		self.bones = []
		self.bonesCount = []
		#texture section
		self.textureCount = 0
		self.textureInfos = []
		self.textureRes = []
		#names
		self.meshNames = []
		self.texNames = []

		# Get file infos
		fI = GetFileType(self.file)
		if fI != "corrupt_filename":
			self.fileName = fI[0]
			self.fileExt = fI[1]
			self.fileType = fI[2]
			self.fileId = fI[3]
			self.filePath = fI[4]
			self.isTexture = fI[5]

			## Load Rx3
			self.rx3Type =  GetRX3FileType(self.gtype)
			self.skeletonType = GetSkeletonType(self.gtype)
			if self.rx3Type == FileType.RX3_Hybrid:
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
		print(f"Texture File? : {self.isTexture}\n")

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
					for y in range(v.Vertexes[x].BlendIndices.Length):
						vertexdata = [v.Vertexes[x].BlendIndices[y].Index_1 , v.Vertexes[x].BlendIndices[y].Index_2, v.Vertexes[x].BlendIndices[y].Index_3, v.Vertexes[x].BlendIndices[y].Index_4]
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
					for y in range(v.Vertexes[x].BlendWeights.Length):
						vertexdata = [v.Vertexes[x].BlendWeights[y].Weight_1 , v.Vertexes[x].BlendWeights[y].Weight_2, v.Vertexes[x].BlendWeights[y].Weight_3, v.Vertexes[x].BlendWeights[y].Weight_4]
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
			temp1 = [] #normals
			temp2 = [] #binromals
			temp3 = [] #tangents
			v = rx3file.Rx3VertexBuffers[i]

			for x in range(v.Vertexes.Length):
				#normals / n
				if v.Vertexes[x].Normals != None:
					data1 = [v.Vertexes[x].Normals[0].Normal_x , v.Vertexes[x].Normals[0].Normal_y, v.Vertexes[x].Normals[0].Normal_z]
					# data1 = [v.Vertexes[x].Normals[0].Normal_x , v.Vertexes[x].Normals[0].Normal_y, v.Vertexes[x].Normals[0].Normal_z, v.Vertexes[x].Normals[0].DEC3N]
					temp1.append(data1)
				#binormals / b
				if v.Vertexes[x].Binormals != None:
					data2 = [v.Vertexes[x].Binormals[0].Binormal_x , v.Vertexes[x].Binormals[0].Binormal_y, v.Vertexes[x].Binormals[0].Binormal_z]
					# data2 = [v.Vertexes[x].Binormals[0].Binormal_x , v.Vertexes[x].Binormals[0].Binormal_y, v.Vertexes[x].Binormals[0].Binormal_z, v.Vertexes[x].Binormals[0].DEC3N]
					temp2.append(data2)
				#tangent / g
				if v.Vertexes[x].Tangents != None:
					data3 = [v.Vertexes[x].Tangents[0].Tangent_x , v.Vertexes[x].Tangents[0].Tangent_y, v.Vertexes[x].Tangents[0].Tangent_z]
					# data3 = [v.Vertexes[x].Tangents[0].Tangent_x , v.Vertexes[x].Tangents[0].Tangent_y, v.Vertexes[x].Tangents[0].Tangent_z, v.Vertexes[x].Tangents[0].DEC3N]
					temp3.append(data3)
			
			self.cols_normals.append(temp1)
			self.cols_binormals.append(temp2)
			self.cols_tangents.append(temp3)

			self.colCount_normals.append(len(self.cols_normals[i]))
			self.colCount_binormals.append(len(self.cols_binormals[i]))
			self.colCount_tangents.append(len(self.cols_tangents[i]))


			if len(self.cols_normals[i]) > 0:
				print(f"Color X,Y,Z,DEC3N of Normal Col 0, Mesh {i} = {self.cols_normals[i][0]}")
				print(f"Color X,Y,Z,DEC3N of Normal Col 1, Mesh {i} = {self.cols_normals[i][1]}")
				print(f"Color X,Y,Z,DEC3N of Normal Col 2, Mesh {i} = {self.cols_normals[i][2]}")
				print(f"Normal Color Count, Mesh {i} : {self.colCount_normals[i]}")

			if len(self.cols_binormals[i]) > 0:
				print(f"Color X,Y,Z,DEC3N of Binormal Col 0, Mesh {i} = {self.cols_binormals[i][0]}")
				print(f"Color X,Y,Z,DEC3N of Binormal Col 1, Mesh {i} = {self.cols_binormals[i][1]}")
				print(f"Color X,Y,Z,DEC3N of Binormal Col 2, Mesh {i} = {self.cols_binormals[i][2]}")
				print(f"Binormal Color Count, Mesh {i} : {self.colCount_binormals[i]}")

			if len(self.cols_tangents[i]) > 0:
				print(f"Color X,Y,Z,DEC3N of Tangent Col 0, Mesh {i} = {self.cols_tangents[i][0]}")
				print(f"Color X,Y,Z,DEC3N of Tangent Col 1, Mesh {i} = {self.cols_tangents[i][1]}")
				print(f"Color X,Y,Z,DEC3N of Tangent Col 2, Mesh {i} = {self.cols_tangents[i][2]}")
				print(f"Tangent Color Count, Mesh {i} : {self.colCount_tangents[i]}")

		return self.cols_normals, self.cols_binormals, self.cols_tangents

	def getUVS(self, rx3file):
		for i in range(rx3file.Rx3VertexBuffers.Length):
			temp = []
			v = rx3file.Rx3VertexBuffers[i]

			for x in range(v.Vertexes.Length):
				if (v.Vertexes[x].TextureCoordinates != None) :
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
		# 2 (maybe left and right)
		# 2 bbox 1 and 2 on each (maybe top and bottom corner)
		# 2 bbox each
		# 4 values (val 1 2 3 4)
		# x [0/1] [bbox1 or 2] [0/1 bbox] [values]

		if (rx3file.RW4Section.RW4ModelCollisions != None):
			for i in range(rx3file.RW4Section.RW4ModelCollisions.Length):
				c = rx3file.RW4Section.RW4ModelCollisions[i]
				temp = [] # per available mesh collision  ## eg 2 count
				
				# [0/1] = [[bbox1_1,bbox1_2][bbox2_1,bbox2_2]]
				# [0/1][0/1] = [bbox1_1,bbox1_2]
				# [0/1][0/1][0/1] = [1,2,3,4]

				perBBOX1 = []	# per bbox1  ## eg 2
				for x in range(len(c.BBox_1)):
					tempvar = c.BBox_1[x]  ## bbox1_0/1
					data = [tempvar.Value_1, tempvar.Value_2, tempvar.Value_3, tempvar.Value_4] #4 values
					perBBOX1.append(data)
				
				perBBOX2 = []	# per bbox  ## eg 2 for each of previous one
				for x in range(len(c.BBox_2)):
					tempvar = tempvar = c.BBox_2[x]  ## bbox2_0/1
					data = [tempvar.Value_1, tempvar.Value_2, tempvar.Value_3, tempvar.Value_4] #4 values
					perBBOX2.append(data)
					
				temp.append(perBBOX1)
				temp.append(perBBOX2)
					

				self.collision.append(temp)
				self.collisionCount.append(len(self.collision[i]))
				if len(self.collision[i]) > 0:
					print(f"Collision 1,2,3,4 of BBOX 1_1, Set {i} = {self.collision[i][0]}")
					print(f"Collision 1,2,3,4 of BBOX 1_2, Set {i} = {self.collision[i][1]}")
					print(f"Collision Count, Set {i} : {self.collisionCount[i]}")

			return self.collision

		else:
			print(f"No collision data found in file!")

	def getBones(self, rx3file):
		if (rx3file.RW4Section.RW4AnimationSkins != None):
			for i in range(rx3file.RW4Section.RW4AnimationSkins.Length):
				temp = []
				v = rx3file.RW4Section.RW4AnimationSkins[i]

				self.bonesCount.append(v.NumBones)
				
				# perBM = []  
				for x in range(len(v.BoneMatrices)):
					if (v.BoneMatrices[x] != None) :
						aBP = v.BoneMatrices[x].absBindPose
						iPT = v.BoneMatrices[x].invPoseTranslation
						bonedata = [aBP, [iPT.X , iPT.Y, iPT.Z]]
						# perBM.append(bonedata)
						temp.append(bonedata)
					else:
						print(f"No Bone Matrices Found in Meshes!")
						break
				
				self.bones.append(temp)
				if len(self.bones[i]) > 0:
					print(f"Bone Matrices X,Y,Z of Bone 0, All Mesh = {self.bones[i][0]}")
					print(f"Bone Matrices X,Y,Z of Bone 1, All Mesh = {self.bones[i][1]}")
					print(f"Bone Matrices X,Y,Z of Bone 2, All Mesh = {self.bones[i][2]}")
					print(f"Bone Matrices X,Y,Z of Bone 3, All Mesh = {self.bones[i][3]}")
					print(f"Bone Matrices Count, All Mesh : {self.bonesCount[i]}")
				
				break 
			
			return self.bones

		else:
			print(f"No Animation data found in file!")

	def getTextures(self, rx3file):
		texdir = fifa_tools.texdir

		self.textureCount = rx3file.Rx3Textures.Length

		for x in range(self.textureCount):
			temp = rx3file.Rx3Textures[x]
			temp1 = [temp.Rx3TextureHeader.Width, temp.Rx3TextureHeader.Height]
			
			self.texNames.append(rx3file.RW4Section.RW4NameSection.Names[x].Name.replace(".Raster",""))
			
			tF = GetTextureFormat(temp.Rx3TextureHeader.TextureFormat)
			tT = GetTextureType(temp.Rx3TextureHeader.TextureType)
			tS = temp.Rx3TextureHeader.TotalSize / 1024
			if tS >= 1024:
				tS = f"{math.ceil(tS / 1024)} MB"
			else:
				tS = f"{math.ceil(tS)} KB"
			
			
			temp2 = [self.texNames[x], tF, tT, tS, f"{temp.Rx3TextureHeader.NumLevels} Mipmaps", f"{temp.Rx3TextureHeader.NumFaces} Tex Faces"]
			
			self.textureRes.append(temp1)
			self.textureInfos.append(temp2)

			print(f"Texture {x} Resolution : {self.textureRes[x]}")
			print(f"Texture {x} Info : {self.textureInfos[x]}")
		
			# texture file extractor
			ddsfile = temp.GetDds()
			ddsfile.Save(f"{texdir}/{self.texNames[x]}.dds")			

	def loadRx3(self):
		file = self.file
		if file != "":
			f = self.data = self.getDataRx3(file)
	
			self.dataRX3.Load(file)

			self.endian = self.dataRX3.RW4Section.RW4Header.Endianness
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
			
			self.offsets = self.getOffsets(self.dataRX3)

			if not self.isTexture:
				self.meshCount = self.dataRX3.Rx3VertexBuffers.Length
				print(f"Total Mesh Count : {self.dataRX3.Rx3IndexBuffers.Length}")

				for x in range(self.meshCount):
					# temp = self.dataRX3.Rx3NameTable.Names[x].Name.split(sep="_")
					temp = self.dataRX3.RW4Section.RW4NameSection.Names[x].Name
					self.meshNames.append(temp)

				self.getVertexFormats(self.dataRX3)

				self.getVertexPosition(self.dataRX3)

				self.getNormalCols(self.dataRX3)

				self.getUVS(self.dataRX3)

				self.getIndicesData(self.dataRX3)

				self.getVertexColor(self.dataRX3)

				self.getBoneIndice(self.dataRX3)
				
				self.getBoneWeight(self.dataRX3)

				self.getCollisions(self.dataRX3)

				self.getBones(self.dataRX3)

				fcOffset = []
				for x in self.offsets:
					if x[0] == 5798132:
						fcOffset.append(x[1])

				self.primitiveType = self.dataRX3.GetPrimitiveType(0)
				# self.primitiveType = self.dataRX3.RW4Section.RW4Shader_FxRenderableSimples[0].PrimitiveType

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
				self.getTextures(self.dataRX3)


		else:
			print("Please choose the model file.")

	#endregion



# x2 = RX3_File(r".\f16\head_16.rx3", GameType.FIFA16)
# x2 = RX3_File(r".\f14\head_14.rx3", GameType.FIFA14)
# print(x2.gtype.name) 
# print(x2.saveRx3("test.s")) 
# print(x2.dataRX3.NumMeshes)
# print(x2.bones[0][0][0].Get(0,0))
# x2 = RX3_File(r".\f14\specificball_0_13_0_textures.rx3", GameType.FIFA14)
# x2 = RX3_File(r".\f14_practice_arena\stadium_665_1_textures.rx3", GameType.FIFA14)
# print(x1.rx3Type.value)
# print(x1.skeletonType.value)
# x2 = RX3_File(r".\f14\stadium_14.rx3", GameType.FIFA14)
# print(x2.texNames)
# # print(x2.meshNames)
# for x in x2.meshNames:
# 	print(x)


# x2 = RX3_File(r".\f14\specificball_0_13_0.rx3", GameType.FIFA14)
# x3 = RX3_File(r".\f14\New Folder\specificball_0_0.rx3", GameType.FIFA14)

x2 = RX3_File(r".\f14\ball_0.rx3", GameType.FIFA14)
x3 = RX3_File(r".\f14\New Folder\ball_0_0.rx3", GameType.FIFA14)


# x2 = RX3_File(r".\f14\specificball_0_13_0.rx3", GameType.FIFA14)
# # x3 = RX3_File(r".\f14\ball_14.rx3", GameType.FIFA14)

# x,y,z = 421.2353299856186/1023, 633.8588467240334/1023, 304.89412996172905/1023
# # x,y,z = 0.4134897, 0.6187683, 0.2981427

# fc = FifaUtil()
# print(fc.FloatsToDEC3N(x,y,z))

# for x in fc.DEC3NtoFloats(882102880):
# 	print(x)

# f = open("alluvs_dll.txt", "w+")
# for x in x2.uvs:
# 	for y in x:
# 		f.writelines(str(x))

# f = open("allvertexpos_dll.txt", "w+")
# for x in x2.vertexPosition :
# 	for y in x:
# 		f.writelines(str(x))

# f = open("allcolor_dll.txt", "w+")
# for x in x2.cols :
# 	for y in x:
# 		f.writelines(str(x))


# get all vertex index from rx3file and convert it to faces


# x2 = RX3_File(r".\f14\shoe_14.rx3", GameType.FIFA14)
# y = RX3_File_Hybrid(r".\f11\stadium_11.rx3", GameType.FIFA11)
# y = RX3_File_Hybrid(r".\f11\head_11.rx3", GameType.FIFA11)
# y = RX3_File_Hybrid(r".\f11\ball_11.rx3", GameType.FIFA11)
# y = RX3_File_Hybrid(r".\f11\ball_11_textures.rx3", GameType.FIFA11)
# print(y.texNames)
# print(y.meshNames)
# zx = 0
# if (zx < (len(TextureType))) and (zx >=0):
# 	print(TextureType(zx).name)
# region Additional Tests

def List_To_Tuple(lst):
	return tuple(List_To_Tuple(i) if isinstance(i, list) else i for i in lst)

def Add_Vgroup_To_Objects(vg_indices, vg_weights, vg_name, obj):
	assert(len(vg_indices) == len(vg_weights))
	# ob = bpy.data.objects[obj] 
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
		print(len(groups[y]))
		print(len(groupsV[y]))
		for x in groups[y]:
			print(f"{(x,)} , {groupsV[y][x]}")
			break
		break

# x = Add_Vgroup_To_Objects(x1.bonesIndice[0], x1.bonesWeight[0], "s", "x")

# endregion