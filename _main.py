# WhatDo:
#
# This script is the main parts of the scene slicer and exporter.
#                       
# How to use:
# 	Locate settings panel in 3D Viewport -> Sidebar -> Scene Slicer
# 	Choose collection to export from dropdown
# 	Set required grid size
# 	Select suitable folder for output
# 	Click "Slice and Export" button
#
# Notes:
#	* Does NOT support Curves, as they don't support bools
#	* Object visibility is ignored - if it's in the collection, it gets exported
#


# ██╗███╗   ███╗██████╗  ██████╗ ██████╗ ████████╗███████╗
# ██║████╗ ████║██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝
# ██║██╔████╔██║██████╔╝██║   ██║██████╔╝   ██║   ███████╗
# ██║██║╚██╔╝██║██╔═══╝ ██║   ██║██╔══██╗   ██║   ╚════██║
# ██║██║ ╚═╝ ██║██║     ╚██████╔╝██║  ██║   ██║   ███████║
# ╚═╝╚═╝     ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝
#

import bpy
import json

from . _settings 	import *
from . booleans		import *
from . boundingBox	import *
from . cutter		import CreateCutter, CreateCutterHelper
from . export		import ExportTileToGLtf, ExportTilesetToJSON
from . logging		import Log, LogReset
from . tiles		import GetTilePositionMin, GetTilePositionMax, GetTilePositionCenter
from . tilesets		import CreateTilesetFromCollection
from . triCounts 	import *



# ███╗   ███╗ █████╗ ██╗███╗   ██╗
# ████╗ ████║██╔══██╗██║████╗  ██║
# ██╔████╔██║███████║██║██╔██╗ ██║
# ██║╚██╔╝██║██╔══██║██║██║╚██╗██║
# ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
# ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
#

def Main() -> str:
	LogReset()

	Log("#--------------------------------------------------#")
	Log("#      Exporting collection to tilset3d            #")
	Log("#--------------------------------------------------#")

	# Get scene slicer settings
	ss_settings = bpy.context.scene.ss_settings

	# Get the chosen collection in the panel
	collection = bpy.data.collections.get(ss_settings.export_collection)

	# Ensure we have a valid collection and trigger the main function
	if collection:
		result = SliceCollection(collection)
		return result
	else:
		Log(f"ERROR: No collection specified. Nothing to do...")
		Log("-----------------------------------------------------")
		return {'FAILED - No collection specified'}

	"""
	OLD METHOD FOR FINDING COLLECTION BY PREFIX
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
	"""



# ███████╗██╗     ██╗ ██████╗███████╗     ██████╗ ██████╗ ██╗     ██╗     ███████╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗
# ██╔════╝██║     ██║██╔════╝██╔════╝    ██╔════╝██╔═══██╗██║     ██║     ██╔════╝██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║
# ███████╗██║     ██║██║     █████╗      ██║     ██║   ██║██║     ██║     █████╗  ██║        ██║   ██║██║   ██║██╔██╗ ██║
# ╚════██║██║     ██║██║     ██╔══╝      ██║     ██║   ██║██║     ██║     ██╔══╝  ██║        ██║   ██║██║   ██║██║╚██╗██║
# ███████║███████╗██║╚██████╗███████╗    ╚██████╗╚██████╔╝███████╗███████╗███████╗╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║
# ╚══════╝╚══════╝╚═╝ ╚═════╝╚══════╝     ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
# 

def SliceCollection(col: bpy.types.Collection) -> str:

	"""
	Slice a collection into tiles and export each tile as a separate GLTF file.

	:param col: The collection to be sliced.
	:type col: bpy.types.Collection
	"""

	# Get scene slicer settings
	ss_settings = bpy.context.scene.ss_settings

	# Generate the basic tileset data from the collection -size, bounds, etc
	tileset_data = CreateTilesetFromCollection(col)

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
	tileset_size = tileset_data["tileset_size"]

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
	ExportTilesetToJSON(tileset_data, ss_settings.output_path)

	Log("Processed", processed_count, "tiles, skipped", skipped_count)
	Log("-----------------------------------------------------")
	return {'FINISHED'}
