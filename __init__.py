#    <Scene Slicer - Blender addon for exporting a scene in a confiruable grid of 3d tiles>
#
#    Copyright (C) <2024> <Tom Steventon>
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
	"name"       : "DCL Toolkit: Scene Slicer",
	"description": "Exporter tool for partitioning a scene into a collection of 3D tiles and exporting them to glTF",
	"author"     : "Tom Steventon - stom66",
	"version"    : (1, 0, 0),
	"blender"    : (3, 6, 0),
	"location"   : "3D Viewport -> Sidebar -> DCL Toolkit",
	"description": "DCL Toolkit: Scene Slicer",
	"category"   : "Import-Export",
	"doc_url"    : "https://github.com/stom66/blender-dcltk-scene-slicer"
}

from . _main 		import *
from . _settings 	import *
from . ui 			import *



# ██████╗ ███████╗ ██████╗ ██╗███████╗████████╗██████╗  █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
# ██╔══██╗██╔════╝██╔════╝ ██║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
# ██████╔╝█████╗  ██║  ███╗██║███████╗   ██║   ██████╔╝███████║   ██║   ██║██║   ██║██╔██╗ ██║
# ██╔══██╗██╔══╝  ██║   ██║██║╚════██║   ██║   ██╔══██╗██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
# ██║  ██║███████╗╚██████╔╝██║███████║   ██║   ██║  ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
# ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
#
		
def register():
	# Register settings class
	bpy.utils.register_class(SceneSlicerSettings)
	bpy.types.Scene.ss_settings = bpy.props.PointerProperty(type=SceneSlicerSettings)
	
	# Register various UI component classes
	bpy.utils.register_class(SCENE_OT_RefreshCollections)
	bpy.utils.register_class(VIEW3D_PT_SceneSlicer_Main)
	bpy.utils.register_class(VIEW3D_PT_SceneSlicer_Export)
	bpy.utils.register_class(VIEW3D_PT_SceneSlicer_Options)

def unregister():
	# Unregister various UI component classes
	bpy.utils.unregister_class(VIEW3D_PT_SceneSlicer_Options)
	bpy.utils.unregister_class(VIEW3D_PT_SceneSlicer_Export)
	bpy.utils.unregister_class(VIEW3D_PT_SceneSlicer_Main)
	bpy.utils.unregister_class(SCENE_OT_RefreshCollections)

	# Unregister settings class
	bpy.utils.unregister_class(SceneSlicerSettings)
	del bpy.types.Scene.ss_settings
