import bpy


# ███████╗███████╗████████╗████████╗██╗███╗   ██╗ ██████╗ ███████╗
# ██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗  ██║██╔════╝ ██╔════╝
# ███████╗█████╗     ██║      ██║   ██║██╔██╗ ██║██║  ███╗███████╗
# ╚════██║██╔══╝     ██║      ██║   ██║██║╚██╗██║██║   ██║╚════██║
# ███████║███████╗   ██║      ██║   ██║██║ ╚████║╚██████╔╝███████║
# ╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝
#

# Define default settings
class SceneSlicerSettings(bpy.types.PropertyGroup):

	output_path: bpy.props.StringProperty(
		name    = "Output path",
		default = "//tileset/",
		subtype = 'FILE_PATH'
	) # type: ignore

	output_prefix: bpy.props.StringProperty(
		name    = "Output prefix",
		default = "tile",
	) # type: ignore

	collection_prefix: bpy.props.StringProperty(
		name    = "Collection prefix",
		default = "_tileset."
	) # type: ignore

	tile_dimensions: bpy.props.FloatVectorProperty(
		name    = "Grid size",
		default = (8, 8, 8),
		subtype = 'XYZ',
		size    = 3
	) # type: ignore