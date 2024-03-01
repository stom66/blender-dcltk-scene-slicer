# WhatDo:
#
# This script is the main parts of the scene slicer and exporter.
#



# ██╗███╗   ███╗██████╗  ██████╗ ██████╗ ████████╗███████╗
# ██║████╗ ████║██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝
# ██║██╔████╔██║██████╔╝██║   ██║██████╔╝   ██║   ███████╗
# ██║██║╚██╔╝██║██╔═══╝ ██║   ██║██╔══██╗   ██║   ╚════██║
# ██║██║ ╚═╝ ██║██║     ╚██████╔╝██║  ██║   ██║   ███████║
# ╚═╝╚═╝     ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝
#

import bpy
import time
import os

#from . _settings 	import *
from . booleans		import *
from . boundingBox	import *
from . collections	import DeleteCollection
from . cutter		import CreateCutter, CreateCutterHelper
from . export		import ExportCollectionToGLtf, ExportObjectsToGLtf, ExportDataToJSON, GetExportPath
from . logging		import Log, LogReset
from . tiles		import GetTilePositionMin, GetTilePositionMax, GetTilePositionCenter
from . tilesets		import CreateTilesetFromCollection, SwizzleTilesetData
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

	Log("#------------------------------------------------#")
	Log("#      Exporting collection to tilset            #")
	Log("#------------------------------------------------#")

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

	time_start = time.time()

	# Get scene slicer settings
	ss_settings  = bpy.context.scene.ss_settings

	# Prefix to temporarily assign to objects being duplicated for export
	temp_prefix = "SS_TEMP_RENAME_"
	
	# Create a new collection to place the sliced objects in
	# If it already exists, remove it
	sliced_collection_name = "_sliced." + ss_settings.export_collection
	sliced_collection = bpy.data.collections.get(sliced_collection_name)
	if sliced_collection:
		DeleteCollection(sliced_collection, True)

	sliced_collection = bpy.data.collections.new(sliced_collection_name)
	bpy.context.scene.collection.children.link(sliced_collection)

	# Ensure nothing is selected
	bpy.ops.object.select_all(action='DESELECT')

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

	# Setup some counters
	processed_count   = 0
	skipped_count     = 0
	skipped_tri_count = 0

	# Build a dict of each object and their min/max bounds
	col_object_bounds = GetCollectionObjectBounds(col)
	
	# Timer stuff
	Log("col_object_bounds", time.time() - time_start)

	# Now we loop through each of the tiles, adding an entry to the tiles array for each
	for x in range(tileset_size[0]):
		tileset_data["tiles"].append([])

		for y in range(tileset_size[1]):
			tileset_data["tiles"][x].append([])

			for z in range(tileset_size[2]):
				
				timer_tile_start = time.time()

				file_name = f"{ss_settings.output_prefix}_{x}_{y}_{z}"

				if ss_settings.swizzle_yz:
					file_name = f"{ss_settings.output_prefix}_{x}_{z}_{y}"

				#Log("----------------------")
				#Log("Exporting tile", file_name)

				# Build the data about the tile
				tile_data = {
					"index"     : [x, y, z],
					"src"       : file_name,
					"pos_center": GetTilePositionCenter([x, y, z], tileset_data),
					"pos_min"   : GetTilePositionMin([x, y, z], tileset_data),
					"pos_max"   : GetTilePositionMax([x, y, z], tileset_data)
				}

				# Timer stuff
				#Log("1) tile_data took", time.time() - timer_tile_start)

				# Find which objects are in the current tile
				objects_in_bounds = GetObjectsWithinBounds(col_object_bounds, tile_data["pos_min"], tile_data["pos_max"])

				# Timer stuff
				#Log("2) objects_in_bounds", time.time() - timer_tile_start)

				# Export the objects in the tile
				if len(objects_in_bounds) > 0:
					
					# Move the cutter to the right position
					cutter.location = tile_data["pos_center"]

					# Move the 3d cursor to the right position
					tile_origin = tile_data["pos_center"]
					if ss_settings.export_origin == "TILE_MIN":
						tile_origin = tile_data["pos_min"]
					elif ss_settings.export_origin == "TILE_MAX":
						tile_origin = tile_data["pos_max"]

					bpy.context.scene.cursor.location = tile_origin
					#Log("3) updated cutter and cursor location", time.time() - timer_tile_start)

					# Duplicate all the objects (applying their modifiers and setting the right position)
					duplicate_objects = DuplicateObjects(objects_in_bounds, tile_origin, temp_prefix)
					#Log("4) duplicated objects", time.time() - timer_tile_start)

					
					bpy.ops.object.select_all(action='DESELECT')

					# Move the duplcaite objects to the sliced collection
					for obj in duplicate_objects:
						for collection in obj.users_collection:
							collection.objects.unlink(obj)
						sliced_collection.objects.link(obj)

					# Trigger the gltf export (only if the tri count is > 0)
					if GetTotalTriCount(duplicate_objects) > 0:
						ExportObjectsToGLtf(duplicate_objects, file_name)
						pass
					else:
						#Log("Skipping tile with 0 verts: ", x, y, z)
						skipped_count += 1
						skipped_tri_count += 1
						tile_data["src"] = None;
					#Log("5) export/skip", time.time() - timer_tile_start)

					# Remove the duplicates
					#for obj in duplicate_objects:
					#	bpy.data.objects.remove(obj)
					#Log("6) remove dupes", time.time() - timer_tile_start)

					# Remove temp_prefix from original names
					for obj in objects_in_bounds:
						obj.name = obj.name.replace(temp_prefix, '')

					pass

				# Otherwise skip the export and set the file_name to none
				else:
					skipped_count += 1
					tile_data["src"] = None;
				
				# Add the tile_data to the array of tiles
				Log("7) tile", file_name, "took", time.time() - timer_tile_start)
				tileset_data["tiles"][x][y].append(tile_data)
				processed_count += 1

	# End of Tiles loop
	
	# Cleanup after, remove the Bools used for cutting
	for obj in col.all_objects:
		RemoveIntersectBooleans(obj, cutter)
		pass

	# Export the tileset JSON
	file_path = GetExportPath("tileset.json")

	if ss_settings.swizzle_yz:
		tileset_data = SwizzleTilesetData(tileset_data)

	ExportDataToJSON(tileset_data, file_path, ss_settings.minify_json)

	Log("-----------------------------------------------------")
	Log("Processed", processed_count, "tiles, skipped", skipped_count, "(0 tris:", skipped_tri_count, ")")
	Log("Total time taken:", str(time.time() - time_start))
	return {'FINISHED'}

def ProcessTile(tile_data, scene_objects):

	pass




# ██████╗ ██╗   ██╗██████╗ ██╗     ██╗ ██████╗ █████╗ ████████╗ ██████╗ ██████╗ 
# ██╔══██╗██║   ██║██╔══██╗██║     ██║██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
# ██║  ██║██║   ██║██████╔╝██║     ██║██║     ███████║   ██║   ██║   ██║██████╔╝
# ██║  ██║██║   ██║██╔═══╝ ██║     ██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗
# ██████╔╝╚██████╔╝██║     ███████╗██║╚██████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
# ╚═════╝  ╚═════╝ ╚═╝     ╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
#

def DuplicateObjects(
	objects    : list[bpy.types.Object],
	new_origin : tuple[float, float, float],
	temp_prefix: str
) -> list[bpy.types.Object]:
	"""
	Duplicate a list of Blender objects, applying modifiers and updating the origin.
	Note that this function will set the origin to the current 3d cursor position,
	then move the object to 0,0,0

	:param objects: List of Blender objects to duplicate.
	:type objects: list[bpy.types.Object]

	:param temp_prefix: Prefix to be added to the original objects' names temporarily.
	:type temp_prefix: str

	:return: List of duplicated objects with applied modifiers and updated origins.
	:rtype: list[bpy.types.Object]
	"""
	time_start = time.time()

	# Ensure nothing is selected
	bpy.ops.object.select_all(action='DESELECT')

	# Create a blank list to store the duplicated objects
	duplicate_objects = []

	# Set the 3d cursor to the new origin
	bpy.context.scene.cursor.location = new_origin
	
	# Clone objects, apply their modifiers, set their origins
	for index, obj in enumerate(objects):
		t = time.time
		time_object_start = t

		# Create a duplicate of the object
		duplicate_obj      = obj.copy()
		duplicate_obj.data = obj.data.copy()
		bpy.context.collection.objects.link(duplicate_obj)

		#Log("    ", index, "copy object took ", time.time() - time_object_start)

		# Rename the original temporarily and ensure the clone has the original name
		# We do this so that the exported model doesn't end up with different mesh names
		original_name      = obj.name
		obj.name           = temp_prefix + original_name
		duplicate_obj.name = original_name
		
		# Set the duplicate object as the active object
		bpy.context.view_layer.objects.active = duplicate_obj
		duplicate_obj.select_set(True)
		
		#Log("    ", index, "rename and set active took", time.time() - time_object_start)

		# Ensure we're in Object Mode
		bpy.ops.object.mode_set(mode='OBJECT')

		# Convert to mesh and apply modifiers
		bpy.ops.object.convert(target='MESH', keep_original=False)

		# Update the objects origin to match the 3d cursor
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

		# Add the duplicate object to the list
		duplicate_objects.append(duplicate_obj)
	
	# Move all the objects AFTER we have duplicated them, otherwise some origins are incorrect
	#for obj in duplicate_objects:
	#	obj.location = (0, 0, 0)
	
	
	Log("DuplicateObjects took", time.time() - time_start, "for", len(objects), "objects")
	return duplicate_objects
