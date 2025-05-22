import bpy
from bpy.props import EnumProperty
import webbrowser

version_text = "v0.70"

credit1 = version_text + ", FIFA 3D Importer / Exporter "
credit2 = "Maintained & Updated by Death GOD 7"
credit3 = "(Original Author : arti-10)"

game_version = " 3D " # you can add number if you want which shows up in panel layout , removed by deathgod7

# Operator: Install Python.NET
class FIFA3D_OT_InstallPythonNET(bpy.types.Operator):
	bl_idname = "fifa3d.install_pythonnet"
	bl_label = "Install Python.NET"

	def execute(self, context):
		self.report({'INFO'}, "Installing Python.NET...")
		if configManager.config['SETTINGS'].getboolean('First_Run'):
			pckgfile = "pythonnet-3.0.5-py3-none-any.whl"
			redistLoc = addonLoc + rf"\fifa_tools\redist\PythonNET"
			packageManager.install(f"{redistLoc}\{pckgfile}")
			configManager.writeConfig("SETTINGS", "First_Run", "False")
		return {'FINISHED'}

# PropertyGroup
dynamic_enum_items = [
	('-', "-", "Please follow the guide above")
]

def get_dynamic_enum_items(self, context):
	return dynamic_enum_items

class FIFA3DAvailableLibs(bpy.types.PropertyGroup):
	libs_selector: EnumProperty(
		name="Available Libs",
		description="Select the available libs version",
		items=get_dynamic_enum_items
	)

# Operator: Refresh Dropdown
class FIFA3D_OT_RefreshList(bpy.types.Operator):
	bl_idname = "fifa3d.refresh_list"
	bl_label = "Refresh"

	def execute(self, context):
		global dynamic_enum_items
		dynamic_enum_items.clear()
		dynamic_enum_items.extend([
			('1.0.0', "v1.0.0", ""),
			('1.1.0', "v1.1.0", ""),
			('1.1.1', "v1.1.1", "")
		])
		self.report({'INFO'}, "Refreshed list.")
		# Your refresh logic here
		return {'FINISHED'}

# Operator: Install Libs
class FIFA3D_OT_InstallLibs(bpy.types.Operator):
	bl_idname = "fifa3d.install_libs"
	bl_label = "Install Libs"

	def execute(self, context):
		scn = context.scene
		self.report({'INFO'}, "Installing libraries...")
		
		selected_lib = scn.f3d_availablelibs.libs_selector
		if (selected_lib == "-"):
			self.report({'WARNING'}, "Please select a valid lib version.")
			print("Please select a valid lib version.")
			return {'CANCELLED'}
		
		self.report({'INFO'}, "Installed libs v" + selected_lib)
		print("Installed libs v" + selected_lib)
		
		return {'FINISHED'}

# Operator: Visit Soccergaming Thread URL
class FIFA3D_OT_VisitThreadURL(bpy.types.Operator):
	bl_idname = 'fifa3d.visit_thread_url'
	bl_label = 'Visit Addon Thread'
	bl_description = 'Visit the official thread of this addon on soccergaming'

	def invoke(self, context, event):
		webbrowser.open(url='http://soccergaming.com/index.php?threads/se7en-fifa-3d-importer-exporter-updated-version-blender-2-8x.6470022/')
		return {'FINISHED'}

# Operator: Visit GitHub URL
class FIFA3D_OT_VisitGitHubURL(bpy.types.Operator):
	bl_idname = 'fifa3d.visit_github_url'
	bl_label = 'Visit GitHub Wiki'
	bl_description = 'Check out the GitHub wiki to find tutorials about this addon'

	def invoke(self, context, event):
		webbrowser.open(url='https://github.com/DeathGOD7/FIFA-3D-Importer-Exporter/wiki')
		return {'FINISHED'}

# Operator: Create Issue in GitHub
class FIFA3D_OT_CreateIssue(bpy.types.Operator):
	bl_idname = 'fifa3d.create_issue'
	bl_label = 'Report Bug / Request Feature'
	bl_description = 'If you have found a bug or want a feature in this addon, click here'

	def invoke(self, context, event):
		webbrowser.open(url='https://github.com/DeathGOD7/FIFA-3D-Importer-Exporter/issues/new/choose')
		return {'FINISHED'}

# Panel: First Install
class FIFA3D_PT_FirstInstall(bpy.types.Panel):
	"""Create category in N-Menu"""
	bl_category = "FIFA 3D I/E"

	"""Creates a Panel in Scene properties window"""
	bl_label = "FIFA" + game_version + "Initialization"
	bl_idname = "FIFA3D_PT_FirstInstall"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'

	def draw(self, context):
		scn = context.scene
		layout = self.layout
		f3d_availablelibs = scn.f3d_availablelibs
		
		box = layout.box()
		box.label(icon='INFO', text='Info')
		col1 = box.column()
		col1.label(text = "Since this is your first time installing this addon.")
		col1.label(text = "Please follow the guide on how to install properly.")
		col1.label(text = "1) Click on 'Install Python.NET'")
		col1.label(text = "2) Get the libs from github repo")
		col1.label(text = "3) Put it in your ..\\Documents\\SE7EN\FIFA3D\\Updates")
		col1.label(text = "4) Click refresh and choose the version")
		col1.label(text = "5) Click on 'Install Libs'")
		col1.label(text = "6) Voila! You installed it")
		col1.label(text = "7) Now enjoy the addon <3")
		

		box2 = layout.box()
		col2 = box2.column()

		col2.operator("fifa3d.install_pythonnet", icon='CONSOLE')

		row = box2.row()
		row.prop(f3d_availablelibs, "libs_selector", text="")
		row.operator("fifa3d.refresh_list", text="", icon='FILE_REFRESH')
		row.operator("fifa3d.install_libs", text="Install Libs", icon='IMPORT')


		col_btm = layout.column()
		col_btm.separator(factor=0.2)
		r_top = col_btm.row()
		r_top.alignment ='CENTER'
		r_top.scale_y = 1.2
		r_top.operator(
			"fifa3d.visit_github_url", text='Visit Github Wiki')
		r_top.operator(
			"fifa3d.visit_thread_url", text='Visit Official Thread')
		r_btm = col_btm.row()
		r_btm.alignment ='CENTER'
		r_btm.scale_y = 1.2
		r_btm.operator(
			"fifa3d.create_issue", text='Report Bug / Request Feature')

		col_btm.separator(factor=0.5)
		r1 = col_btm.row()
		r1.alignment = 'CENTER'
		r1.label(text=credit1)
		r2 = col_btm.row()
		r2.alignment = 'CENTER'
		r2.label(text=credit2)
		r3 = col_btm.row()
		r3.alignment = 'CENTER'
		r3.label(text=credit3)


classes = [
	FIFA3D_OT_InstallPythonNET,
	FIFA3D_OT_RefreshList,
	FIFA3D_OT_InstallLibs,
	FIFA3DAvailableLibs,
	FIFA3D_OT_VisitThreadURL,
	FIFA3D_OT_VisitGitHubURL,
	FIFA3D_OT_CreateIssue,
	FIFA3D_PT_FirstInstall,
]

def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	bpy.types.Scene.f3d_availablelibs = bpy.props.PointerProperty(type=FIFA3DAvailableLibs)

def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
	del bpy.types.Scene.f3d_availablelibs

if __name__ == "__main__":
	register()