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
		items = [(col.name, col.name, col.name) for col in bpy.context.scene.collection.children if col.name != "Cutters"]
		return items

	# Collection to export dropdown
	export_collection: bpy.props.EnumProperty(
		name        = "Export Collection",
		description = "Choose a collection to slice and export",
		items       = refresh_collections,
		default 	= None,
		#update      = refresh_collections,
		attr        = "export_collection"
	)  # type: ignore

	# Output path
	output_path: bpy.props.StringProperty(
		name        = "Output path",
		description = "Choose a folder to export to",
		default     = "//tileset/",
		subtype     = 'FILE_PATH'
	) # type: ignore

	# Grid size
	tile_dimensions: bpy.props.FloatVectorProperty(
		name        = "Grid size",
		description = "Set the size of each grid tile to partition the ",
		default     = (8, 8, 8),
		subtype     = 'XYZ',
		size        = 3
	) # type: ignore

	#
	# Advanced options

	# Bool solver method
	bool_solver: bpy.props.EnumProperty(
		name   = "Bool solver method",
		items  = [
			("FAST",  "Fast",  "Simple solver for best performance, without support for overlapping geometry"),
			("EXACT", "Exact", "Advanced solver for the best results, slower performance"),
		],
		default = "FAST",
	)  # type: ignore

	# Skip _collider export
	skip_colliders: bpy.props.BoolProperty(
		name        = "Skip exporting _colliders",
		description = "Ignore any meshes with names ending with '_collider'",
		default     = True,
	) # type: ignore

	# JSON minify
	minify_json: bpy.props.BoolProperty(
		name        = "Minify JSON",
		description = "Minify the exported JSON to reduce filesize",
		default     = True,
	) # type: ignore


	# glTF settings
	
	# Draco compression
	use_draco: bpy.props.BoolProperty(
		name        = "Use Draco compression",
		description = "Should Draco compression be enabled - note this does not work with certain glTF viewers",
		default     = False,
	) # type: ignore

	# File format: gltf or glb
	export_format: bpy.props.EnumProperty(
		name        = "glTF Export format",
		description = "Output format. Binary is most efficient, but JSON maybe be easier to edit later. Separate textures allow for texture re-use.",
		default     = "GLTF_SEPARATE",
		items       = [
			("GLB",   		  "glTF Binary (.glb)",   					"Exports a single file, with all data packed in binary form. Most efficient and portable, more difficult to edit later and does not support texture re-use."),
			("GLTF_SEPARATE", "glTF Separate (.gltf + .bin + texture)", "Exports multiple files, with separate JSON, binary and texture data. Easiest to edit later and allows for textu re-reuse."),
		],
	)  # type: ignore

	# Output file prefix
	output_prefix: bpy.props.StringProperty(
		name        = "Output prefix",
		description = "Specify the prefix for filenames when exporting",
		default     = "tile",
	) # type: ignore

	# Tile origin
	export_origin: bpy.props.EnumProperty(
		name        = "Export origin location",
		description = "Set the location of exported tile origins",
		default     = "CENTER",
		items       = [
			("CENTER",   "Center",   "Center of the tile"),
			("TILE_MIN", "Tile Min", "Minimum coordinates of the tile"),
			("TILE_MAX", "Tile Max", "Maximum coordinates of the tile"),
		],
	)  # type: ignore
