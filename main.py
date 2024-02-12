# WhatDo:
#
# This script is the main parts of the scene slicer and exporter.
#                       
# How to use:
# 	Move all items that are to be exported together into a collection
# 	Name the collection, including the collection_prefix below, eg: `_tileset.myLevel`
# 	(Optionally) Go to Window -> Toggle System Console
# 	Click the play button to run the script
#
# Notes:
#	* Does NOT support Curves, as they don't support bools
#	* Object visibility is ignored - if it's in the collection, it gets exported
#

bl_info = {
	"name"       : "Scene Slicer",
	"description": "Exporter tool for partitioning a scene into a collection of 3d tiles",
	"author"     : "Tom Steventon - stom66",
	"version"    : (1, 0, 0),
	"blender"    : (3, 6, 0),
	"location"   : "3D Viewport -> Sidebar -> Scene Slicer",
	"description": "Scene Slicer",
	"category"   : "Import-Export",
	"doc_url"    : "https://github.com/stom66/blender-scene-slicer"
}



# ██╗███╗   ███╗██████╗  ██████╗ ██████╗ ████████╗███████╗
# ██║████╗ ████║██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝
# ██║██╔████╔██║██████╔╝██║   ██║██████╔╝   ██║   ███████╗
# ██║██║╚██╔╝██║██╔═══╝ ██║   ██║██╔══██╗   ██║   ╚════██║
# ██║██║ ╚═╝ ██║██║     ╚██████╔╝██║  ██║   ██║   ███████║
# ╚═╝╚═╝     ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝
#

import bpy
import json

from . boundingBox	import *
from . booleans		import *
from . cutter		import CreateCutter, CreateCutterHelper
from . export		import ExportTileToGLtf, ExportTilesetToJSON
from . tiles		import *
from . tilesets		import *
#from . triCounts 	import *

from . settings import *



# ██╗      ██████╗  ██████╗  ██████╗ ██╗███╗   ██╗ ██████╗
# ██║     ██╔═══██╗██╔════╝ ██╔════╝ ██║████╗  ██║██╔════╝
# ██║     ██║   ██║██║  ███╗██║  ███╗██║██╔██╗ ██║██║  ███╗
# ██║     ██║   ██║██║   ██║██║   ██║██║██║╚██╗██║██║   ██║
# ███████╗╚██████╔╝╚██████╔╝╚██████╔╝██║██║ ╚████║╚██████╔╝
# ╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝
#

LOG_PATH = "scene_slicer.log"

def log(*args):
	"""
	Prints the log message composed of the provided arguments and writes it to the LOG_TXT file.

	Args:
	*args: Variable number of arguments to be included in the log message.
	"""

	if LOG_PATH not in bpy.data.texts:
		LOG_TXT = bpy.data.texts.new(LOG_PATH)
	else:
		LOG_TXT = bpy.data.texts[LOG_PATH]

	message = ' '.join(str(arg) for arg in args)
	print(message)
	LOG_TXT.write(message + '\n')

def LogReset():
	if LOG_PATH in bpy.data.texts:
		bpy.data.texts[LOG_PATH].clear()



# ███╗   ███╗ █████╗ ██╗███╗   ██╗
# ████╗ ████║██╔══██╗██║████╗  ██║
# ██╔████╔██║███████║██║██╔██╗ ██║
# ██║╚██╔╝██║██╔══██║██║██║╚██╗██║
# ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
# ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
#

def Main():
	LogReset()

	log("#---------------------------------------------------#")
	log("#      Exporting collections to tilset3d            #")
	log("#---------------------------------------------------#")

	# Check that the "_export" collection exists
	tilesetCollectionExists = False
	collection_prefix       = bpy.context.scene.ss_settings.collection_prefix

	# Loop through all collections in the current view layer
	for col in bpy.context.view_layer.layer_collection.children:
		
		# Check the current collection to see if it should be exported
		if col.name.count(collection_prefix) and not col.exclude:
			tilesetCollectionExists = True
			SliceCollection(bpy.data.collections.get(col.name))

	# Throw an error if there's no export collection
	if not tilesetCollectionExists:
		log(f"ERROR: a collection with '{collection_prefix}' in the name could not be found. Nothing to do...")
		log("-----------------------------------------------------")



# ███████╗██╗     ██╗ ██████╗███████╗██████╗     ███╗   ███╗ █████╗ ██╗███╗   ██╗
# ██╔════╝██║     ██║██╔════╝██╔════╝██╔══██╗    ████╗ ████║██╔══██╗██║████╗  ██║
# ███████╗██║     ██║██║     █████╗  ██████╔╝    ██╔████╔██║███████║██║██╔██╗ ██║
# ╚════██║██║     ██║██║     ██╔══╝  ██╔══██╗    ██║╚██╔╝██║██╔══██║██║██║╚██╗██║
# ███████║███████╗██║╚██████╗███████╗██║  ██║    ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
# ╚══════╝╚══════╝╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
#
		
def SliceCollection(col: bpy.types.Collection) -> None:

	"""
	Slice a collection into tiles and export each tile as a separate GLTF file.

	:param col: The collection to be sliced.
	:type col: bpy.types.Collection
	"""

	# Get scene slicer settings
	ss_settings = bpy.context.scene.ss_settings

	# Get bounds min/max points for all objects in the collections
	bounds_min, bounds_max, bounds_com = GetCollectionBounds(col)

	# Use bounds to work out the required tileset size and origin
	tileset_size, tileset_origin = GetTilesetSizeOrigin(bounds_min, bounds_max, ss_settings.tile_dimensions)

	# Build Tileset data
	tileset_data = {
		"name"           : col.name.replace(ss_settings.collection_prefix, ''),
		"tile_dimensions": ss_settings.tile_dimensions,
		"tileset_size"   : tileset_size,
		"tileset_origin" : tileset_origin,
		"bounds_min"     : bounds_min,
		"bounds_max"     : bounds_max,
		"bounds_com"     : bounds_com,
		"tiles"          : []
	}

	# Create/update the cutter and the helper object
	cutter        = CreateCutter(tileset_data)
	cutter_helper = CreateCutterHelper(tileset_data)

	# Ensure every object has a bool mod on it which uses our cutter
	# also tidy up old/broken booleans
	for obj in col.all_objects:
		if obj.type == 'MESH':
			AddIntersectBooleans(obj, cutter)
			RemoveBrokenBooleans(obj)

	# Add a Triangulate modifier to every object
	triangulate_modifiers = {}
	for obj in col.all_objects:
		if obj.type == 'MESH':
			modifier = obj.modifiers.new(name="Triangulate", type='TRIANGULATE')
			triangulate_modifiers[obj] = modifier	

	# Setup some counters
	processed_count = 0
	skipped_count = 0

	# Now we loop through each of the tiles, adding an entry to the tiles array for each tile
	for x in range(tileset_size[0]):
		tileset_data["tiles"].append([])

		for y in range(tileset_size[1]):
			tileset_data["tiles"][x].append([])

			for z in range(tileset_size[2]):
				file_name = f"{ss_settings.output_prefix}_{x}_{y}_{z}"

				# Build the data about the tile
				tile_data = {
					"index"     : [x, y, z],
					"src"       : file_name,
					"pos_center": GetTilePositionCenter([x, y, z], tileset_data),
					"pos_min"   : GetTilePositionMin([x, y, z], tileset_data),
					"pos_max"   : GetTilePositionMax([x, y, z], tileset_data)
				}

				# Move the cutter to the right position
				cutter.location = tile_data["pos_center"]

				# Check if any collection object bounding boxes intersect the cutter
				# If so, trigger the export
				if CheckForObjectsWithinBounds(col, tile_data["pos_min"], tile_data["pos_max"]):
					# Trigger the gltf export
					#ExportTile(file_name, col)
					pass

				# Otherwise skip the export and set the file_name to none
				else:
					skipped_count += 1
					tile_data["file_name"] = None;
				
				# Add the tile_data to the array of tiles
				tileset_data["tiles"][x][y].append(tile_data)
				processed_count += 1
	# End of Tiles loop
	
	# Cleanup after, remove the Bools used for cutting
	for obj in col.all_objects:
		RemoveIntersectBooleans(obj, cutter)

	# Remove the triangulate modifiers we added
	for obj, modifier in triangulate_modifiers.items():
		obj.modifiers.remove(modifier)

	# Export the tileset JSON
	ExportTilesetToJSON(tile_data, ss_settings.output_path)

	log("Processed", processed_count, "tiles, skipped", skipped_count)
	log("-----------------------------------------------------")



# ██╗   ██╗███████╗███████╗██████╗     ██╗███╗   ██╗████████╗███████╗██████╗ ███████╗ █████╗  ██████╗███████╗
# ██║   ██║██╔════╝██╔════╝██╔══██╗    ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝
# ██║   ██║███████╗█████╗  ██████╔╝    ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝█████╗  ███████║██║     █████╗  
# ██║   ██║╚════██║██╔══╝  ██╔══██╗    ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗██╔══╝  ██╔══██║██║     ██╔══╝  
# ╚██████╔╝███████║███████╗██║  ██║    ██║██║ ╚████║   ██║   ███████╗██║  ██║██║     ██║  ██║╚██████╗███████╗
#  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝    ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝
#

# UI Main button for exporting
class VIEW3D_PT_SceneSlicer_Export(bpy.types.Operator):
	bl_idname  = "scene.slice_and_export"
	bl_label   = "Main function"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		self.report({'INFO'}, 'Exporting...')
		Main()
		return {'FINISHED'}

# UI Panel class
class VIEW3D_PT_SceneSlicer_Main(bpy.types.Panel):
	bl_label       = 'Scene Slicer'
	bl_category    = 'Scene Slicer'
	bl_region_type = 'UI'
	bl_space_type  = 'VIEW_3D'

	def draw(self, context):
		layout = self.layout

		row = layout.row()
		row.label(text="Output Path:")
		row.prop(context.scene.ss_settings, "output_path", text="")

		row = layout.row()
		row.label(text="Collection Prefix:")
		row.prop(context.scene.ss_settings, "collection_prefix", text="")

		row = layout.row()
		row.label(text="Grid Size:")

		row = layout.row()
		row.prop(context.scene.ss_settings, "tile_dimensions", text="")

		row = layout.row()
		#row.label(text="Select Sequenced Vertices to:")
		row.operator(VIEW3D_PT_SceneSlicer_Export.bl_idname, text="Slice and Export", icon="FILE_VOLUME")



# ██████╗ ███████╗ ██████╗ ██╗███████╗████████╗██████╗  █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
# ██╔══██╗██╔════╝██╔════╝ ██║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
# ██████╔╝█████╗  ██║  ███╗██║███████╗   ██║   ██████╔╝███████║   ██║   ██║██║   ██║██╔██╗ ██║
# ██╔══██╗██╔══╝  ██║   ██║██║╚════██║   ██║   ██╔══██╗██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
# ██║  ██║███████╗╚██████╔╝██║███████║   ██║   ██║  ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
# ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
#
		
def register():
	bpy.utils.register_class(SceneSlicerSettings)
	bpy.types.Scene.ss_settings = bpy.props.PointerProperty(type=SceneSlicerSettings)
	bpy.utils.register_class(VIEW3D_PT_SceneSlicer_Main)
	bpy.utils.register_class(VIEW3D_PT_SceneSlicer_Export)

def unregister():
	bpy.utils.unregister_class(VIEW3D_PT_SceneSlicer_Main)
	bpy.utils.unregister_class(VIEW3D_PT_SceneSlicer_Export)
	bpy.utils.unregister_class(SceneSlicerSettings)
	del bpy.types.Scene.ss_settings
