import 	bpy
import 	os
import 	json
from 	collections 			import defaultdict
from 	xml.etree.ElementTree 	import tostring



# ██████╗  █████╗ ████████╗██╗  ██╗
# ██╔══██╗██╔══██╗╚══██╔══╝██║  ██║
# ██████╔╝███████║   ██║   ███████║
# ██╔═══╝ ██╔══██║   ██║   ██╔══██║
# ██║     ██║  ██║   ██║   ██║  ██║
# ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
#                                  

def GetExportPath(file: str = None) -> str:
	"""
	Get the export path for the collection.

	Returns:
	- str: The export path.
	"""
	# Get scene slicer settings
	ss_settings = bpy.context.scene.ss_settings

	# Get the export path based on the current settings value
	path = bpy.path.abspath(ss_settings.output_path)

	# Ensure the output folder exists
	try:
		# Ensure filepath exists, create it if it doesn't
		os.makedirs(os.path.dirname(path))
	except FileExistsError:
		pass  # The directory already exists, no need to create

	# If a filename was specified, join it
	if file:
		path = os.path.join(path, file)

	path = os.path.normpath(path)
	
	# Ensure filepath doesn't have a trailing slash, as this causes a permission error
	#if path.endswith("/") or path.endswith("\\"):
	#	path = path[:-1]

	return path



# ███████╗██╗  ██╗██████╗  ██████╗ ██████╗ ████████╗         ██╗███████╗ ██████╗ ███╗   ██╗
# ██╔════╝╚██╗██╔╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝         ██║██╔════╝██╔═══██╗████╗  ██║
# █████╗   ╚███╔╝ ██████╔╝██║   ██║██████╔╝   ██║            ██║███████╗██║   ██║██╔██╗ ██║
# ██╔══╝   ██╔██╗ ██╔═══╝ ██║   ██║██╔══██╗   ██║       ██   ██║╚════██║██║   ██║██║╚██╗██║
# ███████╗██╔╝ ██╗██║     ╚██████╔╝██║  ██║   ██║       ╚█████╔╝███████║╚██████╔╝██║ ╚████║
# ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝        ╚════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝
#

def ExportDataToJSON(
	data,
	file,
	minify
):
	"""
	Export the supplied tileset_data to a file at the given output_path
	"""

	if minify:
		json_string = json.dumps(data)
	else:
		json_string = json.dumps(data, indent="\t")

	# Write the data object to an output JSON file
	with open(file, "w") as json_file:
		json_file.write(json_string)



#  ██████╗ ██╗  ████████╗███████╗    ███████╗███████╗████████╗████████╗██╗███╗   ██╗ ██████╗ ███████╗
# ██╔════╝ ██║  ╚══██╔══╝██╔════╝    ██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗  ██║██╔════╝ ██╔════╝
# ██║  ███╗██║     ██║   █████╗      ███████╗█████╗     ██║      ██║   ██║██╔██╗ ██║██║  ███╗███████╗
# ██║   ██║██║     ██║   ██╔══╝      ╚════██║██╔══╝     ██║      ██║   ██║██║╚██╗██║██║   ██║╚════██║
# ╚██████╔╝███████╗██║   ██║         ███████║███████╗   ██║      ██║   ██║██║ ╚████║╚██████╔╝███████║
#  ╚═════╝ ╚══════╝╚═╝   ╚═╝         ╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝
#

gltf_settings = {
	"use_renderable"                         : False,
	"use_selection"                          : False,
	"use_visible"                            : False,
	"use_active_scene"                       : False,
	"use_active_collection"                  : False,
	"use_active_collection_with_nested"      : False,

	# Basic export settings
	"export_format"                          : 'GLTF_SEPARATE',
	#"filepath"                              : file_path,

	# Texture settings
	"export_keep_originals"                  : False, 	 #
	"export_image_format"                    : 'AUTO', 	 # `AUTO` | Images, Output format for images. PNG is lossless and generally preferred, but JPEG might be preferable for web applications due to the smaller file size. Alternatively they can be omitted if they are not needed\
	"export_texture_dir"                     : 'tex', 	 #
	"export_materials"                       : 'EXPORT', #
	"export_original_specular"               : False,    # false |  Export original PBR Specular, Export original glTF PBR Specular, instead of Blender Principled Shader Specular
	"export_import_convert_lighting_mode"    : 'SPEC',   # `SPEC` | Lighting Mode, Optional backwards compatibility for non-standard render engines. Applies to lights

	# Compression settings
	"export_draco_mesh_compression_enable"   : False, 	 # false | Draco mesh compression, Compress mesh using Draco
	"export_draco_mesh_compression_level"    : 6, 		 # 6  	| Compression level, Compression level (0                                                     = most speed, 6 = most compression, higher values currently not supported)
	"export_draco_color_quantization"        : 10,		 # 10 	| Color quantization bits, Quantization bits for color values (0                              = no quantization)
	"export_draco_generic_quantization"      : 12, 		 # 12 	| Generic quantization bits, Quantization bits for generic values like weights or joints (0  = no quantization)
	"export_draco_normal_quantization"       : 10, 		 # 10 	| Normal quantization bits, Quantization bits for normal values (0                           = no quantization)
	"export_draco_position_quantization"     : 14, 	 	 # 14 	| Position quantization bits, Quantization bits for position values (0                      = no quantization)
	"export_draco_texcoord_quantization"     : 12, 		 # 12 	| Texcoord quantization bits, Quantization bits for texture coordinate values (0             = no quantization)

	# Object data
	"export_apply"                           : True,     # true  | Apply Modifiers, Apply modifiers (excluding Armatures) to mesh objects -WARNING: prevents exporting shape keys
	"export_attributes"                      : False, 	 # false | Attributes, Export Attributes (when starting with underscore)
	"export_colors"                          : False,    # false | Vertex Colors, Export vertex colors with meshes
	"export_copyright"                       : '',       # ''    | Copyright, Legal rights and conditions for the model
	"export_extras"                          : False,    # false | Custom Properties, Export custom properties as glTF extras
	"export_morph"                           : True,     # true  | Shape Keys, Export shape keys (morph targets)
	"export_morph_normal"                    : True,     # true  | Shape Key Normals, Export vertex normals with shape keys (morph targets)
	"export_morph_tangent"                   : False,    # false | Shape Key Tangents, Export vertex tangents with shape keys (morph targets)
	"export_normals"                         : True,     # true  | Normals, Export vertex normals with meshes
	"export_skins"                           : True,     # true  | Skinning, Export skinning (armature) data
	"export_tangents"                        : True,     # true  | Tangents, Export vertex tangents with meshes
	"export_texcoords"                       : True,     # true  | UVs, Export UVs (texture coordinates) with meshes
	"export_yup"                             : True,     # true  | +Y Up, Export using glTF convention, +Y up
	"use_mesh_edges"                         : False,    # false | Loose Edges, Export loose edges as lines, using the material from the first material slot
	"use_mesh_vertices"                      : False,    # false | Loose Points, Export loose points as glTF points, using the material from the first material slot

	# Animation settings
	"export_animations"                      : True,     # true  | Animations, Exports active actions and NLA tracks as glTF animations
	"export_current_frame"                   : False,    # false | Use Current Frame, Export the scene in the current animation frame
	"export_force_sampling"                  : True,     # true  | Always Sample Animations, Apply sampling to all animations
	"export_frame_range"                     : True,     # true  | Limit to Playback Range, Clips animations to selected playback range
	"export_frame_step"                      : 1,        # 1     | Sampling Rate, How often to evaluate animated values (in frames)
	"export_nla_strips"                      : True,     # true  | Group by NLA Track, When on, multiple actions become part of the same glTF animation if they’re pushed onto NLA tracks with the same name. When off, all the currently assigned actions become one glTF animation
	"export_nla_strips_merged_animation_name": 'action', # 'Animation' | Merged Animation Name, Name of single glTF animation to be exported
	"export_optimize_animation_size"         : True,     # true  | Optimize Animation Size, Reduce exported file size by removing duplicate keyframes (can cause problems with stepped animation)

	# Armature settings
	"export_all_influences"                  : True,     # true  | Include All Bone Influences, Allow >4 joint vertex influences. Models may appear incorrectly in many viewers
	"export_anim_single_armature"            : True,     # true  | Export all Armature Actions, Export all actions, bound to a single armature. WARNING: Option does not support exports including multiple armatures
	"export_def_bones"                       : True,     # true  | Export Deformation Bones Only, Export Deformation bones only
	"export_reset_pose_bones"                : True,     # true  | Reset pose bones between actions, Reset pose bones between each action exported. This is needed when some bones are not keyed on some animations

	# Extra objects
	"export_cameras"                         : False,  	 # Export camera
	"export_lights"                          : False  	 #
}



# ███████╗██╗  ██╗██████╗  ██████╗ ██████╗ ████████╗     ██████╗ ██╗  ████████╗███████╗
# ██╔════╝╚██╗██╔╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝    ██╔════╝ ██║  ╚══██╔══╝██╔════╝
# █████╗   ╚███╔╝ ██████╔╝██║   ██║██████╔╝   ██║       ██║  ███╗██║     ██║   █████╗  
# ██╔══╝   ██╔██╗ ██╔═══╝ ██║   ██║██╔══██╗   ██║       ██║   ██║██║     ██║   ██╔══╝  
# ███████╗██╔╝ ██╗██║     ╚██████╔╝██║  ██║   ██║       ╚██████╔╝███████╗██║   ██║     
# ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝        ╚═════╝ ╚══════╝╚═╝   ╚═╝     
#                                                                                      

def ExportCollectionToGLtf(
	collection  : bpy.types.Collection, 
	filename    : str, 
	reset_origin: bool = True
) -> None:
	"""
	Export the specified collection to a GLTF file with the given filename.

	Args:
	- filename (str): The name of the file to export.
	- collection (bpy.types.Collection): The Blender collection containing objects to export.

	Returns:
	- None
	"""

	# Get scene slicer settings
	ss_settings = bpy.context.scene.ss_settings

	# Work out the destination name
	file_path = GetExportPath(filename)

	# Set the collection as the active collection
	bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[collection.name]

	# Deselect all the objects
	bpy.ops.object.select_all(action='DESELECT')

	# Do the actual export, inherit the default settings specified above
	export_settings                                         = gltf_settings
	export_settings["filepath"]                             = file_path
	export_settings["export_format"]						= ss_settings.export_format
	export_settings["export_yup"]                           = ss_settings.swizzle_yz
	export_settings["use_active_collection"]                = True
	export_settings["use_active_collection_with_nested"]    = True
	export_settings["export_draco_mesh_compression_enable"] = ss_settings.use_draco

	bpy.ops.export_scene.gltf(**export_settings)


def ExportObjectsToGLtf(
	objects     : list[bpy.types.Object], 
	filename    : str,		
	reset_origin: bool = True
) -> None:
	"""
	Export the specified objects to a GLTF file with the given filename.

	Args:
	- filename (str): The name of the file to export.
	- objects (List[bpy.types.Object]): The objects to export.

	Returns:
	- None
	"""

	# Get scene slicer settings
	ss_settings = bpy.context.scene.ss_settings

	# Work out the destination name
	file_path = GetExportPath(filename)

	# Deselect all the objects
	bpy.ops.object.select_all(action='DESELECT')

	# If we need to reset_origin, store the current locations and move the object to world origin
	object_locations = {}
	if reset_origin:
		for obj in objects:
			object_locations[obj] = obj.location.copy()

	# Select all the objects we want to export
	for obj in objects:
		obj.select_set(True)
		if reset_origin:
			obj.location = (0,0,0)

	# Do the actual export, inherit the default settings specified above
	export_settings                                         = gltf_settings
	export_settings["filepath"]                             = file_path
	export_settings["export_format"]						= ss_settings.export_format
	export_settings["export_yup"]                           = ss_settings.swizzle_yz
	export_settings["use_selection"]             		    = True
	export_settings["export_draco_mesh_compression_enable"] = ss_settings.use_draco

	bpy.ops.export_scene.gltf(**export_settings)

	# If we reset the origin for export, move the object back to it's original location
	if reset_origin:
		pass
		for obj, location in object_locations.items():
			obj.location          = location
