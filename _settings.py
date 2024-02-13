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
	
	def refresh_collections(self, context):
		print("Refreshing collection dropdown")
		items = [(col.name, col.name, col.name) for col in bpy.context.scene.collection.children]
		return items

	export_collection: bpy.props.EnumProperty(
		name        = "Export Collection",
		description = "Choose a collection to slice and export",
		items       = refresh_collections,
		default 	= None,
		#update      = refresh_collections,
		attr        = "export_collection"
	)  # type: ignore


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

	minify_json: bpy.props.BoolProperty(
		name    = "Minify JSON",
		default = True,
	) # type: ignore

	use_draco: bpy.props.BoolProperty(
		name    = "Use Draco compression",
		default = False,
	) # type: ignore

	skip_colliders: bpy.props.BoolProperty(
		name    = "Skip exporting _colliders",
		default = True,
	) # type: ignore

	export_origin: bpy.props.EnumProperty(
		name   = "Export origin location",
		items  = [
			("CENTER",   "Center",   "Center of the tile"),
			("TILE_MIN", "Tile Min", "Minimum coordinates of the tile"),
			("TILE_MAX", "Tile Max", "Maximum coordinates of the tile"),
		],
		default = "CENTER",
	)  # type: ignore