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

#from . _settings 	import *
from . booleans		import *
from . boundingBox	import *
from . cutter		import CreateCutter, CreateCutterHelper
from . export		import ExportCollectionToGLtf, ExportObjectsToGLtf, ExportTilesetToJSON
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
	
#  
	
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
	ss_settings  = bpy.context.scene.ss_settings

	# Prefix to temporarily assign to objects being duplicated for export
	temp_prefix = "SS_TEMP_RENAME_"

	# Generate the basic tileset data from the collection -size, bounds, etc
	tileset_data = CreateTilesetFromCollection(col)
	tileset_size = tileset_data["tileset_size"]

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

	# Build a dict of each object and their min/max bounds
	col_object_bounds = GetCollectionObjectBounds(col)

	# Now we loop through each of the tiles, adding an entry to the tiles array for each
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

				# Find which objects are in the current tile
				objects_in_bounds = GetObjectsWithinBounds(col_object_bounds, tile_data["pos_min"], tile_data["pos_max"])

				# Export the objects in the tile
				if len(objects_in_bounds) > 0:
					
					# Move the cutter to the right position
					cutter.location = tile_data["pos_center"]

					# Move the 3d cursor to the right position
					bpy.context.scene.cursor.location = tile_data["pos_center"]
					if ss_settings.export_origin == "TILE_MIN":
						bpy.context.scene.cursor.location =tile_data["pos_min"]
					if ss_settings.export_origin == "TILE_MAX":
						bpy.context.scene.cursor.location =tile_data["pos_max"]

					# Duplicate all the objects (applying their modifiers and setting the right position)
					duplicate_objects = DuplicateObjects(objects_in_bounds, temp_prefix)

					# Trigger the gltf export
					ExportObjectsToGLtf(duplicate_objects, file_name)

					# Remove the duplicates
					for obj in duplicate_objects:
						bpy.data.objects.remove(obj)

					# Remove temp_prefix from original names
					for obj in objects_in_bounds:
						obj.name = obj.name.replace(temp_prefix, '')

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
	ExportTilesetToJSON(tileset_data)

	Log("Processed", processed_count, "tiles, skipped", skipped_count)
	Log("-----------------------------------------------------")
	return {'FINISHED'}


# Object cloning

def DuplicateObjects(
	objects    : list[bpy.types.Object], 
	temp_prefix: str
) -> list[bpy.types.Object]:
	"""
	Duplicate a list of Blender objects, apply modifiers, set origins, and move to .

	:param objects: List of Blender objects to duplicate.
	:type objects: list[bpy.types.Object]

	:param temp_prefix: Prefix to be added to the original objects' names temporarily.
	:type temp_prefix: str

	:return: List of duplicated objects with applied modifiers and updated origins.
	:rtype: list[bpy.types.Object]
	"""
	
	duplicate_objects = []
	
	# Clone objects, apply their modifiers, set their origins
	for obj in objects:
		
		# Create a duplicate of the object
		duplicate_obj      = obj.copy()
		duplicate_obj.data = obj.data.copy()
		bpy.context.collection.objects.link(duplicate_obj)

		# Rename the original temporarily
		original_name      = obj.name
		obj.name           = temp_prefix + original_name
		duplicate_obj.name = original_name
		
		# Set the duplicate object as the active object
		bpy.context.view_layer.objects.active = duplicate_obj
		duplicate_obj.select_set(True)
		
		# Switch to Object Mode
		bpy.ops.object.mode_set(mode='OBJECT')

		# Convert to mesh and apply modifiers
		bpy.ops.object.convert(target='MESH', keep_original=False)

		# Update the objects origin to match the 3d cursor
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='BOUNDS')

		# Move the object to the world origin
		duplicate_obj.location = (0, 0, 0)

		# Add the duplicate object to the list
		duplicate_objects.append(duplicate_obj)
	
	return duplicate_objects