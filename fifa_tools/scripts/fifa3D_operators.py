import bpy
from bpy.props import EnumProperty
import webbrowser

from fifa_tools import configManager, packageManager, addonLoc, dependencyManager

pythonnetinstalled = False
libsinstalled = False

def check_first_run():
	global pythonnetinstalled, libsinstalled
	# Check if Python.NET is installed
	pythonnetinstalled = configManager.config['VERSIONS'].get('Python.NET') != "0.0.0"
	# Check if FIFA3DLibs is installed
	libsinstalled = configManager.config['VERSIONS'].get('FIFA3DLibs') != "0.0.0"

	if pythonnetinstalled and libsinstalled:
		configManager.writeConfig("SETTINGS", "First_Run", "False")

# Operator: Install Python.NET
class FIFA3D_OT_InstallPythonNET(bpy.types.Operator):
	bl_idname = "fifa3d.install_pythonnet"
	bl_label = "Install Python.NET"

	def execute(self, context):
		self.report({'INFO'}, "Installing Python.NET...")
		try:
			pckgfile = "pythonnet-3.0.5-py3-none-any.whl"
			redistLoc = addonLoc + rf"\fifa_tools\redist\PythonNET"
			packageManager.install(f"{redistLoc}\{pckgfile}")
		except Exception as e:
			self.report({'ERROR'}, f"Error installing Python.NET: {e}")
			return {'CANCELLED'}
		else:
			check_first_run()
			self.report({'INFO'}, "Python.NET installed successfully.")
		return {'FINISHED'}

# PropertyGroup
availablelibs = []

def refresh_availablelibs():
	global availablelibs
	availablelibs.clear()
	dependencyManager.checkDependencies()
	for ver in dependencyManager.availableVersions:
		availablelibs.append((ver, "v" + ver, ""))
	if len(availablelibs) == 0:
		availablelibs.append(("-", "-", "Please follow the guide above"))


def get_availablelibs(self, context):
	return availablelibs

class FIFA3DAvailableLibs(bpy.types.PropertyGroup):
	libs_selector: EnumProperty(
		name="Available Libs",
		description="Select the available libs version",
		items=get_availablelibs
	)

# Operator: Refresh Dropdown
class FIFA3D_OT_RefreshList(bpy.types.Operator):
	bl_idname = "fifa3d.refresh_list"
	bl_label = "Refresh"

	def execute(self, context):
		refresh_availablelibs()
		context.scene.f3d_availablelibs.libs_selector = availablelibs[0][0]
		# Optionally force UI redraw as previously suggested
		for area in context.window.screen.areas:
			if area.type == 'PROPERTIES':
				area.tag_redraw()
		self.report({'INFO'}, "Refreshed list.")
		return {'FINISHED'}

# Operator: Install Libs
class FIFA3D_OT_InstallLibs(bpy.types.Operator):
	bl_idname = "fifa3d.install_libs"
	bl_label = "Install Libs"

	def execute(self, context):
		scn = context.scene
		self.report({'INFO'}, "Installing libraries...")
		
		selected_lib = scn.f3d_availablelibs.libs_selector
		if (selected_lib == "-" or selected_lib == ""):
			self.report({'WARNING'}, "Please select a valid lib version.")
			return {'CANCELLED'}

		try:
			dependencyManager.installLibs(selected_lib)
		except Exception as e:
			self.report({'ERROR'}, f"Error installing FIFA3DLibs: {e}")
			return {'CANCELLED'}
		else:
			# Check if the installation was successful
			if dependencyManager.isInstalled:
				check_first_run()
				self.report({'INFO'}, f"FIFA3DLibs v{selected_lib} installed successfully.")
			else:
				self.report({'ERROR'}, f"Failed to install FIFA3DLibs v{selected_lib}.")
				return {'CANCELLED'}
		
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

classes = [
	FIFA3D_OT_InstallPythonNET,
	FIFA3D_OT_RefreshList,
	FIFA3D_OT_InstallLibs,
	FIFA3DAvailableLibs,
	FIFA3D_OT_VisitThreadURL,
	FIFA3D_OT_VisitGitHubURL,
	FIFA3D_OT_CreateIssue,
]

def print_installed_versions():
	print(f"Python.NET: v{configManager.config['VERSIONS'].get('Python.NET')}")
	print(f"FIFA3DLibs: v{configManager.config['VERSIONS'].get('FIFA3DLibs')}")

def register():
	print_installed_versions()
	refresh_availablelibs()
	for cls in classes:
		bpy.utils.register_class(cls)
	bpy.types.Scene.f3d_availablelibs = bpy.props.PointerProperty(type=FIFA3DAvailableLibs)

def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
	del bpy.types.Scene.f3d_availablelibs

if __name__ == "__main__":
	register()