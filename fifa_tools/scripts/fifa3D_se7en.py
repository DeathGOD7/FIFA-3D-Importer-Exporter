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
		self.cols = []
		self.colCount = 0
		self.data = 0
		self.endian = ""
		self.endianStr = ""
		self.endianType = ""
		self.faces= []
		self.faceCount = 0
		self.indicesCount = 0
		self.indicesLength = 0
		self.offsets = []
		self.primitiveType = 0
		self.vertexFormat = []
		self.vertexPosition = []
		self.totalVertCount = 0
		self.uvs = []
		self.uvCount = 0

	def getDataRx3(self, file):
		data = open(file, 'rb')
		filename = os.path.basename(file)
		print(f"\nFile : {filename}")
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

	def facereadlist(self, f, offset, indicesLength, indicesCount, endian):
		f.seek(offset)
		faces = []
		self.faceCount = int(indicesCount / 3)

		print(f"Face Count: {self.faceCount}")

		# this is read in addon to get indicescount and length
		# f.read(4) 
		# f.read(4) # indicescount
		# f.read(1) # indiceslength
		# f.read(3)
		# f.read(4)
		# all read are 16 bytes so...auto doing read of 16

		f.read(16)

		if indicesLength == 4:
			string = endian + 'III'
		elif indicesLength == 2:
			string = endian + 'HHH'

		for i in range(self.faceCount):
			temp = struct.unpack(string, f.read(indicesLength * 3))
			if not temp[0] == temp[1]:
				if not temp[2] == temp[1]:
					if temp[0] == temp[2]:
						continue
					faces.append((temp[0], temp[1], temp[2]))

		return faces

	def facereadstrip(self, f, offset, indicesLength, indicesCount, endian):
		f.seek(offset)
		faces = []
		self.faceCount = indicesCount - 2

		print(f"Face Count: {self.faceCount}")

		# f.read(4)
		# f.read(4) # indicescount
		# f.read(4) # indiceslength
		# f.read(4)
		# all read are 16 bytes so...auto doing read of 16

		f.read(16)

		if indicesLength == 4:
			string = '<III'
		elif indicesLength == 2:
			string = '<HHH'

		flag = False
		for i in range(self.faceCount):
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

	def read_file_data(self, rx3file, opts, count):
		uvcount = 0
		colcount = 0
		uvs = []
		cols = []
		cols_0 = []
		cols_1 = []
		cols_2 = []
		uvs_0, uvs_1, uvs_2, uvs_3, uvs_4, uvs_5, uvs_6, uvs_7 = ([], [], [], [], [], [], [], [])
		bones_i0 = []
		bones_i1 = []
		bones_w = []
		bones_c = []
		for i in range(count):
			uvcount = 0
			colcount = 0
			for j in opts:
				if j[0][0] == 't':
					if j[4] == '2f32':
						eval('uvs_' + str(j[0][1]) + '.append(gh.read_uvs_1(f))')
					elif j[4] == '2f16':
						eval('uvs_' + str(j[0][1]) + '.append(gh.read_uvs_0(f))')
					uvcount += 1
				elif j[0][0] == 'n':
					colcount += 1
					cols_0.append(gh.read_cols(f))
				elif j[0][0] == 'b':
					colcount += 1
					cols_2.append(gh.read_cols(f))
				elif j[0][0] == 'g':
					colcount += 1
					cols_1.append(gh.read_cols(f))
				elif j[0][0] == 'i':
					if j[4] == '4u8':
						eval('bones_i' + str(j[0][1]) + ".append(struct.unpack('<4B',f.read(4)))")
					elif j[4] == '4u16':
						eval('bones_i' + str(j[0][1]) + ".append(struct.unpack('<4H',f.read(8)))")
				elif j[0][0] == 'w':
					bones_w.append(struct.unpack('<4B', f.read(4)))
				elif j[0][0] == 'c':
					bones_c.append(struct.unpack('<4B', f.read(4)))
					continue

		for j in range(uvcount):
			eval('uvs.append(uvs_' + str(j) + ')')

		for j in range(colcount):
			eval('cols.append(cols_' + str(j) + ')')

		return (
		 verts, cols, uvs, bones_i0, bones_w)

	def getVertexFormats(self, rx3file):
		for x in range(rx3file.Rx3VertexFormats.Length):
			print(f"Total Vertex Elements : {rx3file.Rx3VertexFormats[x].VertexFormat.Length}")
			for y in range(rx3file.Rx3VertexFormats[x].VertexFormat.Length):
				self.vertexFormat.append(rx3file.Rx3VertexFormats[x].VertexFormat[y])

		print(f"Vertex Formats : {self.vertexFormat}")
		return self.vertexFormat

	def getVertexPosition(self, rx3file):
		v = rx3file.Rx3VertexBuffers[0]

		self.totalVertCount = v.Vertexes.Length
		print(f"Total Vertices Count : {self.totalVertCount}")

		for x in range(v.Vertexes.Length):
			data = [v.Vertexes[x].Positions[0].X/100 , -v.Vertexes[x].Positions[0].Z/100, v.Vertexes[x].Positions[0].Y/100, v.Vertexes[x].Positions[0].W]
			self.vertexPosition.append(data)
		
		print(f"Position X,Z,Y,W of Vertex 0 = {self.vertexPosition[0]}")
		return self.vertexPosition

	def getIndicesData(self, rx3file):
		# rx3model.Rx3IndexBuffer(meshid) ==> For faces
		# rx3model.Rx3IndexBuffer(meshid).Rx3IndexBufferHeader.IndexSize is the same as "indiceslength" in your code
			
		indices = rx3file.Rx3IndexBuffers[0]

		self.indicesCount = indices.IndexStream.Length
		print(f"Incides Count : {self.indicesCount}")

		self.indicesLength =  indices.Rx3IndexBufferHeader.IndexSize
		print(f"Indices Length : {self.indicesLength}")

		return [self.indicesCount, self.indicesLength]
			
	def loadRx3(self, rx3file):
		file = rx3file
		if file != "":
			f = self.data = self.getDataRx3(file)
	
			mainFile = Rx3File()
			mainFile.Load(file)

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

			self.getIndicesData(mainFile)

			fcOffset = 0
			for x in self.offsets:
				if x[0] == 5798132:
					fcOffset = x[1]

			# f.seek(-16, 2)
			# self.primitiveType = int.from_bytes(f.read(1),"little")
			self.primitiveType = mainFile.GetPrimitiveType(0)

			if self.primitiveType == 4:
				print(f"Primitive Type : {self.primitiveType} (TriangleList)")
				self.faces.append(self.facereadlist(self.data, fcOffset, self.indicesLength, self.indicesCount, self.endianType))
			elif self.primitiveType == 6:
				print(f"Primitive Type : {self.primitiveType} (TriangleFans)") #TriangleStrip
				self.faces.append(self.facereadstrip(self.data, fcOffset, self.indicesLength, self.indicesCount, self.endianType))
			else:
				print("Unknown Primitive Type")

			print(f"Values of Face 0 : {self.faces[0][0]}")

		else:
			print("Please choose the model file.")


class RX3_File_Hybrid():
	def __init__(self, file, ftype): 
		self.file = file
		self.ftype = ftype
		self.cols = []
		self.colCount = 0
		self.data = 0
		self.endian = ""
		self.endianStr = ""
		self.endianType = ""
		self.faces= []
		self.faceCount = 0
		self.indicesCount = 0
		self.indicesLength = 0
		self.offsets = []
		self.primitiveType = 0
		self.vertexFormat = []
		self.vertexPosition = []
		self.totalVertCount = 0
		self.uvs = []
		self.uvCount = 0

	def getDataRx3(self, file):
		data = open(file, 'rb')
		filename = os.path.basename(file)
		print(f"\nFile : {filename}")
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

	def facereadlist(self, f, offset, indicesLength, indicesCount, endian):
		f.seek(offset)
		faces = []
		self.faceCount = int(indicesCount / 3)

		print(f"Face Count: {self.faceCount}")

		# this is read in addon to get indicescount and length
		# f.read(4) 
		# f.read(4) # indicescount
		# f.read(1) # indiceslength
		# f.read(3)
		# f.read(4)
		# all read are 16 bytes so...auto doing read of 16

		f.read(16)

		if indicesLength == 4:
			string = endian + 'III'
		elif indicesLength == 2:
			string = endian + 'HHH'

		for i in range(self.faceCount):
			temp = struct.unpack(string, f.read(indicesLength * 3))
			if not temp[0] == temp[1]:
				if not temp[2] == temp[1]:
					if temp[0] == temp[2]:
						continue
					faces.append((temp[0], temp[1], temp[2]))

		return faces

	def facereadstrip(self, f, offset, indicesLength, indicesCount, endian):
		f.seek(offset)
		faces = []
		self.faceCount = indicesCount - 2

		print(f"Face Count: {self.faceCount}")

		# f.read(4)
		# f.read(4) # indicescount
		# f.read(4) # indiceslength
		# f.read(4)
		# all read are 16 bytes so...auto doing read of 16

		f.read(16)

		if indicesLength == 4:
			string = '<III'
		elif indicesLength == 2:
			string = '<HHH'

		flag = False
		for i in range(self.faceCount):
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

	def read_file_data(self, rx3file, opts, count):
		uvcount = 0
		colcount = 0
		uvs = []
		cols = []
		cols_0 = []
		cols_1 = []
		cols_2 = []
		uvs_0, uvs_1, uvs_2, uvs_3, uvs_4, uvs_5, uvs_6, uvs_7 = ([], [], [], [], [], [], [], [])
		bones_i0 = []
		bones_i1 = []
		bones_w = []
		bones_c = []
		for i in range(count):
			uvcount = 0
			colcount = 0
			for j in opts:
				if j[0][0] == 't':
					if j[4] == '2f32':
						eval('uvs_' + str(j[0][1]) + '.append(gh.read_uvs_1(f))')
					elif j[4] == '2f16':
						eval('uvs_' + str(j[0][1]) + '.append(gh.read_uvs_0(f))')
					uvcount += 1
				elif j[0][0] == 'n':
					colcount += 1
					cols_0.append(gh.read_cols(f))
				elif j[0][0] == 'b':
					colcount += 1
					cols_2.append(gh.read_cols(f))
				elif j[0][0] == 'g':
					colcount += 1
					cols_1.append(gh.read_cols(f))
				elif j[0][0] == 'i':
					if j[4] == '4u8':
						eval('bones_i' + str(j[0][1]) + ".append(struct.unpack('<4B',f.read(4)))")
					elif j[4] == '4u16':
						eval('bones_i' + str(j[0][1]) + ".append(struct.unpack('<4H',f.read(8)))")
				elif j[0][0] == 'w':
					bones_w.append(struct.unpack('<4B', f.read(4)))
				elif j[0][0] == 'c':
					bones_c.append(struct.unpack('<4B', f.read(4)))
					continue

		for j in range(uvcount):
			eval('uvs.append(uvs_' + str(j) + ')')

		for j in range(colcount):
			eval('cols.append(cols_' + str(j) + ')')

		return (
		 verts, cols, uvs, bones_i0, bones_w)

	def getVertexFormats(self, rx3file):
		# RW4VertexDescriptors

		for x in range(rx3file.RW4Section.RW4VertexDescriptors.Length):
			print(f"Total Vertex Elements : {rx3file.RW4Section.RW4VertexDescriptors[x].NumElements}")
			for y in range(rx3file.RW4Section.RW4VertexDescriptors[x].Elements.Length):
				temp0 = rx3file.RW4Section.RW4VertexDescriptors[x].Elements[y]
				# usage, usageIndex, offset, unk0, dataType
				temp1 = f"{temp0.Usage, temp0.UsageIndex, temp0.Offset, 0, temp0.DataType}"
				self.vertexFormat.append(temp1)

		print(f"Vertex Formats : {self.vertexFormat}")
		return self.vertexFormat

	def getVertexPosition(self, rx3file):
		v = rx3file.Rx3VertexBuffers[0]

		self.totalVertCount = v.Vertexes.Length
		print(f"Total Vertices Count : {self.totalVertCount}")

		for x in range(v.Vertexes.Length):
			data = [v.Vertexes[x].Positions[0].X/100 , -v.Vertexes[x].Positions[0].Z/100, v.Vertexes[x].Positions[0].Y/100, v.Vertexes[x].Positions[0].W]
			self.vertexPosition.append(data)
		
		print(f"Position X,Z,Y,W of Vertex 0 = {self.vertexPosition[0]}")
		return self.vertexPosition

	def getIndicesData(self, rx3file):
		# rx3model.Rx3IndexBuffer(meshid) ==> For faces
		# rx3model.Rx3IndexBuffer(meshid).Rx3IndexBufferHeader.IndexSize is the same as "indiceslength" in your code
			
		indices = rx3file.Rx3IndexBuffers[0]

		self.indicesCount = indices.IndexStream.Length
		print(f"Incides Count : {self.indicesCount}")

		self.indicesLength =  indices.Rx3IndexBufferHeader.IndexSize
		print(f"Indices Length : {self.indicesLength}")

		return [self.indicesCount, self.indicesLength]
			
	def loadRx3(self, rx3file):
		file = rx3file
		if file != "":
			f = self.data = self.getDataRx3(file)
	
			mainFile = Rx3File()
			mainFile.Load(file)


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

			self.getIndicesData(mainFile)

			fcOffset = 0
			for x in self.offsets:
				if x[0] == 5798132:
					fcOffset = x[1]

			self.primitiveType = mainFile.GetPrimitiveType(0)
			# self.primitiveType = mainFile.RW4Section.RW4Shader_FxRenderableSimples[0].PrimitiveType

			if self.primitiveType == 4:
				print(f"Primitive Type : {self.primitiveType} (TriangleList)")
				self.faces.append(self.facereadlist(self.data, fcOffset, self.indicesLength, self.indicesCount, self.endianType))
			elif self.primitiveType == 6:
				print(f"Primitive Type : {self.primitiveType} (TriangleFans)") #TriangleStrip
				self.faces.append(self.facereadstrip(self.data, fcOffset, self.indicesLength, self.indicesCount, self.endianType))
			else:
				print("Unknown Primitive Type")

			print(f"Values of Face 0 : {self.faces[0][0]}")

		else:
			print("Please choose the model file.")

