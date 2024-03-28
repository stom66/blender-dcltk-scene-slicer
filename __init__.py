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
	"version"    : (0, 2, 2),
	"blender"    : (4, 0, 0),
	"location"   : "3D Viewport -> Sidebar -> DCL Toolkit",
	"description": "DCL Toolkit: Scene Slicer",
	"category"   : "Import-Export",
	"doc_url"    : "https://github.com/stom66/blender-dcltk-scene-slicer"
}

import bpy

from bpy.app.handlers import persistent

from . _main 		import *
from . _settings 	import *
from . logging		import *
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
	
	# Register operators
	bpy.utils.register_class(EXPORT_OT_SceneSlicer_Preview)
	bpy.utils.register_class(SCENE_OT_SceneSlicer_RefreshCollections)
	bpy.utils.register_class(EXPORT_OT_SceneSlicer_Export)

	# Register UI panels
	bpy.utils.register_class(VIEW3D_PT_SceneSlicer_Main)
	bpy.utils.register_class(VIEW3D_PT_SceneSlicer_Options)

	# Register handlers
	if HANDLER_UI_ResetProgress not in bpy.app.handlers.load_post:
		bpy.app.handlers.load_post.append(HANDLER_UI_ResetProgress)



def unregister():
	# Remove handlers
	if HANDLER_UI_ResetProgress in bpy.app.handlers.load_pre:
		bpy.app.handlers.load_pre.remove(HANDLER_UI_ResetProgress)
	if HANDLER_UI_ResetProgress in bpy.app.handlers.depsgraph_update_post:
		bpy.app.handlers.depsgraph_update_post.remove(HANDLER_UI_ResetProgress)

	# Remove UI panels
	bpy.utils.unregister_class(VIEW3D_PT_SceneSlicer_Options)
	bpy.utils.unregister_class(VIEW3D_PT_SceneSlicer_Main)

	# remove operators
	bpy.utils.unregister_class(EXPORT_OT_SceneSlicer_Export)
	bpy.utils.unregister_class(SCENE_OT_SceneSlicer_RefreshCollections)
	bpy.utils.unregister_class(EXPORT_OT_SceneSlicer_Preview)

	# Remove settings class
	bpy.utils.unregister_class(SceneSlicerSettings)
	del bpy.types.Scene.ss_settings



# ██╗  ██╗ █████╗ ███╗   ██╗██████╗ ██╗     ███████╗██████╗ ███████╗
# ██║  ██║██╔══██╗████╗  ██║██╔══██╗██║     ██╔════╝██╔══██╗██╔════╝
# ███████║███████║██╔██╗ ██║██║  ██║██║     █████╗  ██████╔╝███████╗
# ██╔══██║██╔══██║██║╚██╗██║██║  ██║██║     ██╔══╝  ██╔══██╗╚════██║
# ██║  ██║██║  ██║██║ ╚████║██████╔╝███████╗███████╗██║  ██║███████║
# ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝
#

@persistent
def HANDLER_UI_ResetProgress(scene):

	Log("HANDLER_Scene_Update_Pre()")
	EXPORT_OT_SceneSlicer_Export.UI_ResetProgress(EXPORT_OT_SceneSlicer_Export)
