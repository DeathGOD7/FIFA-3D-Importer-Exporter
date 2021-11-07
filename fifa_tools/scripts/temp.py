#COPY FILE
if i==1:
	name=scn.hair_import_path.split(sep='\\')[-1]
	copyfile(scn.hair_import_path,scn.export_path+'\\'+name)
else:
	
for i in range(len(e.mesh_offsets)):
	try:
		if e.type=='head':
			print('Trying to find: ',e.type+'_'+str(file_id)+'_'+str(i)+'_'+e.sub_names[i].split(sep='_')[0])
			object=bpy.data.objects[e.type+'_'+str(file_id)+'_'+str(i)+'_'+e.sub_names[i].split(sep='_')[0]]
			parts_dict[e.sub_names[i].split(sep='_')[0]]=[dict[e.sub_names[i].split(sep='_')[0]],i]
		else:
			print('Trying to find: ',e.type+'_'+str(file_id)+'_'+str(i))
			object=bpy.data.objects[e.type+'_'+str(file_id)+'_'+str(i)]
			parts_dict[e.type]=[e.type,i]
			
	except:
		print('Missing Part')
		print('Check your Scene objects')
		continue
	
	verts=[]
	uvs=[]
	cols=[]
	indices=[]
	
	print(e.mesh_offsets)
	print(e.indices_offsets)
	
	opts=fifa_func.mesh_descr_convert(e.mesh_descrs[i])
	print(opts)
	verts,uvs,cols,indices=fifa_func.convert_original_mesh_to_data(object)
	
	print('Part Description: ',opts,'Part Vertices: ',len(verts),'Part UV maps: ',e.uvcount[i],'Part Indices: ',len(indices),'Part Color maps: ',e.colcount[i])
	
	e.data.seek(e.mesh_offsets[i][0]+16) #get to geometry data offset
	
	fifa_func.convert_mesh_to_bytes(e.data,opts,len(verts),verts,uvs,cols)
	
	e.data.seek(e.indices_offsets[i][0]+16) #get to indices data offset
	fifa_func.write_indices(e.data,indices)
	
e.data.flush()
e.data.close()	
print(str(e.type).upper()+' EXPORT SUCCESSFULL')
print('\n')

self.report({'INFO'}, 'Models Overwritten Successfully')


#Texture Exporting
if scn.texture_export_flag:
for k in range(len(parts)):
	textures_list=[]
	texture_dict={}
	offset_list=[]
	
	if parts[k] in ['head','eyes']:
		name=scn.model_import_path.split(sep='\\')[-1]
	else:
		name=scn.hair_import_path.split(sep='\\')[-1]
	
	file_type=name.split(sep='.')[0].split(sep='_')[0]
	file_id=name.split(sep='.')[0].split(sep='_')[1]
	
	
	
	try:
		if parts[k] in ['head','eyes']:
			object=bpy.data.objects[file_type+'_'+str(file_id)+'_'+str(parts_dict[parts[k]][1])+'_'+parts[k]]
		else:
			object=bpy.data.objects[file_type+'_'+str(file_id)+'_'+str(parts_dict[parts[k]][1])]	
	

		try:
			mat=bpy.data.materials[object.material_slots[0].name]
			
			for i in range(3):
				try:
					texture_name=mat.texture_slots[i].name
					texture_image=bpy.data.textures[texture_name].image.name
					texture_path=bpy.data.images[texture_image].filepath
					texture_alpha=bpy.data.images[texture_image].use_alpha
					texture_maxsize=max(bpy.data.images[texture_image].size[0],bpy.data.images[texture_image].size[1])
					
					if not texture_name in texture_dict:
						textures_list.append([texture_name,texture_path,texture_alpha,0,0,0,0,'',texture_maxsize])
						texture_dict[texture_name]=len(textures_list)
					
				except:
					print('Empty Texture Slot')
		except:
			print('Head Material is Missing')
	except:
		print('Head Part is Missing')
				
	
	#Convert Textures to DDS
	
	status=fifa_func.texture_convert(self,textures_list)
	if status.split(sep=',')[0]=='texture_path_error':
		self.report({'ERROR'},'Missing '+status.split(sep=',')[1]+' Texture File')
		return {'CANCELLED'}
	
	#Read converted textures and calculate offsets
	
	offset_list,textures_list=fifa_func.read_converted_textures(offset_list,textures_list,'fifa_tools\\')
	
	
	#Calling Writing to file Functions
	f=open(scn.export_path+parts_dict[parts[k]][0]+'_'+str(file_id)+'_textures.rx3','wb')
	fifa_func.write_offsets_to_file(f,offset_list)
	fifa_func.write_offset_data_to_file(f,'fifa_tools\\',offset_list,[],[],[],textures_list,[],[],[])
	
	#Signature
	f.seek(offset_list[-1][1])
	f.seek(offset_list[-1][2],1)
	s=bytes(sig,'utf-8')
	f.write(s)
	
	f.close()	
	
	print(offset_list)


