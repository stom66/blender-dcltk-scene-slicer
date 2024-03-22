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

from . booleans		import *
from . boundingBox	import *
from . collections	import DeleteCollection
from . cutter		import CreateCutter, CreateCutterHelper
from . duplicate	import DuplicateObjects
from . export		import ExportObjectsToGLtf, ExportDataToJSON, GetExportPath
from . logging		import Log, LogReset
from . tilesets		import CreateTilesetFromCollection, SwizzleTilesetData
from . triCounts 	import *

# ██████╗ ██████╗ ███████╗██╗   ██╗██╗███████╗██╗    ██╗    ████████╗██╗██╗     ███████╗███████╗███████╗████████╗
# ██╔══██╗██╔══██╗██╔════╝██║   ██║██║██╔════╝██║    ██║    ╚══██╔══╝██║██║     ██╔════╝██╔════╝██╔════╝╚══██╔══╝
# ██████╔╝██████╔╝█████╗  ██║   ██║██║█████╗  ██║ █╗ ██║       ██║   ██║██║     █████╗  ███████╗█████╗     ██║   
# ██╔═══╝ ██╔══██╗██╔══╝  ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║       ██║   ██║██║     ██╔══╝  ╚════██║██╔══╝     ██║   
# ██║     ██║  ██║███████╗ ╚████╔╝ ██║███████╗╚███╔███╔╝       ██║   ██║███████╗███████╗███████║███████╗   ██║   
# ╚═╝     ╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝        ╚═╝   ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝   ╚═╝   
#                                                                                                                

class EXPORT_OT_SceneSlicer_Preview(bpy.types.Operator):

	
	bl_idname  = "ss.preview"
	bl_label   = "Slice and Export"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):		
		# Ensure nothing is selected
		bpy.ops.object.select_all(action='DESELECT')

		# Get scene slicer settings
		ss_settings = bpy.context.scene.ss_settings

		# Get the chosen collection in the panel
		collection = bpy.data.collections.get(ss_settings.export_collection)

		# Generate the basic tileset data from the collection: size, bounds, etc
		tileset_data = CreateTilesetFromCollection(collection)

		# Create/update the cutter and the helper object
		cutter_helper = CreateCutterHelper(tileset_data)
		
		return {'FINISHED'}



# ███╗   ███╗ █████╗ ██╗███╗   ██╗
# ████╗ ████║██╔══██╗██║████╗  ██║
# ██╔████╔██║███████║██║██╔██╗ ██║
# ██║╚██╔╝██║██╔══██║██║██║╚██╗██║
# ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
# ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
#

class EXPORT_OT_SceneSlicer_Export(bpy.types.Operator):
	"""
	Slice a collection into tiles and export each tile as a separate GLTF file.

	:param col: The collection to be sliced.
	:type col: bpy.types.Collection
	"""
	
	bl_idname  = "ss.export"
	bl_label   = "Slice and Export"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		# Get scene slicer settings
		ss_settings = bpy.context.scene.ss_settings
		
		# Setup some starting values for the operation
		self.count_total         = 0
		self.count_processed     = 0
		self.count_skipped       = 0
		self.count_skipped_empty = 0

		self.tileset_data        = None
		self.tiles_total         = 0
		self.tileset_index       = [0, 0, 0]

		self.collection          = bpy.data.collections.get(ss_settings.export_collection)
		self.col_object_bounds   = None
		self.sliced_collection   = None

		self.cutter              = None
		self.cutter_helper       = None
				
		self.time_start          = time.time()

		LogReset()
		Log("#------------------------------------------------#")
		Log("#      Exporting collection to tilset            #")
		Log("#------------------------------------------------#")


		# Ensure we have a valid collection and trigger the main function
		if not self.collection:
			Log(f"ERROR: No collection specified. Nothing to do...")
			Log("-----------------------------------------------------")
			self.report({'INFO'}, 'No collection specified')
			return {'CANCELLED'}

		
		# Create a new collection to place the sliced objects in
		# If it already exists, remove it and any objects in it
		sliced_collection_name = "_sliced." + ss_settings.export_collection
		self.sliced_collection = bpy.data.collections.get(sliced_collection_name)
		if self.sliced_collection:
			DeleteCollection(self.sliced_collection, True)

		self.sliced_collection = bpy.data.collections.new(sliced_collection_name)
		bpy.context.scene.collection.children.link(self.sliced_collection)

		# Ensure nothing is selected
		bpy.ops.object.select_all(action='DESELECT')

		# Generate the basic tileset data from the collection: size, bounds, etc
		self.tileset_data = CreateTilesetFromCollection(self.collection)

		# Update the expected number of tiles
		size = self.tileset_data["tileset_size"]
		self.count_total = size[0] * size[1] * size[2]

		# Build a dict of each object and their min/max bounds
		self.col_object_bounds = GetCollectionObjectBounds(self.collection)

		# Create/update the cutter and the helper object
		self.cutter        = CreateCutter(self.tileset_data)
		self.cutter_helper = CreateCutterHelper(self.tileset_data)

		# Ensure every object has a bool mod, set to use our cutter
		# also tidy up old/broken booleans
		for obj in self.collection.all_objects:
			if obj.type == 'MESH':
				AddIntersectBooleans(obj, self.cutter)
				RemoveBrokenBooleans(obj)

		# Update the UI
		self.UI_UpdateProgress()

		# Setup the modal, with a timer to ensure it runs properly
		self._timer = context.window_manager.event_timer_add(0.1, window=context.window)
		context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}


	def modal(self, context, event):
		
		if event.type == 'ESC':
			return {'CANCELLED'}
		
		if event.type == 'TIMER':

			# Get scene slicer settings
			ss_settings = bpy.context.scene.ss_settings

			# Prefix to temporarily assign to objects being duplicated for export
			temp_prefix = "SS_TEMP_RENAME_"

			# Batch size, testing resulted in 1 per loop being the most responsive, especialyl when dealing with larger models
			batch_size = 1

			# Get max tile indexes
			x_max, y_max, z_max = self.tileset_data["tileset_size"]

			# Loop through the tiles in this batch
			for _ in range(batch_size):
				tile_time_start = time.time()

				# Get the current tile indexes
				x, y, z = self.tileset_index

				# Check if we need to intitialise this array
				if x == 0: 
					self.tileset_data["tiles"].append([])

				if y == 0:
					self.tileset_data["tiles"][x].append([])
						
				# Reference to tile data
				tile_data = self.tileset_data["tiles"][x][y][z]

				# Find which objects are in the current tile
				objects_in_bounds = GetObjectsWithinBounds(self.col_object_bounds, tile_data["pos_min"], tile_data["pos_max"])


				# Export the objects in the tile
				if len(objects_in_bounds) > 0:
					
					# Move the cutter to the right position
					self.cutter.location = tile_data["pos_center"]

					# Get the desired tile origin from settings
					tile_origin = tile_data["pos_center"]
					if ss_settings.export_origin == "TILE_MIN":
						tile_origin = tile_data["pos_min"]
					elif ss_settings.export_origin == "TILE_MAX":
						tile_origin = tile_data["pos_max"]

					# Move the 3d cursor to the tile origin. This is semi-redundant as it's also done
					# by DuplicateObjects, but adding it here seems to be required sometimes
					bpy.context.scene.cursor.location = tile_origin

					# Duplicate all the objects (applying their modifiers and setting the right position)
					duplicate_objects = DuplicateObjects(objects_in_bounds, tile_origin, temp_prefix)

					# Ensure all objects are deselected
					bpy.ops.object.select_all(action='DESELECT')

					# Move the duplicate objects to the sliced collection
					for obj in duplicate_objects:
						for collection in obj.users_collection:
							collection.objects.unlink(obj)
						self.sliced_collection.objects.link(obj)

					# Check we have some tris before triggering the glTF export
					if GetTotalTriCount(duplicate_objects) > 0:
						ExportObjectsToGLtf(duplicate_objects, tile_data["src"])
						pass

					else:
						self.count_skipped += 1
						self.count_skipped_empty += 1
						tile_data["src"] = None;

					# Remove the duplicates?
					#for obj in duplicate_objects:
					#	bpy.data.objects.remove(obj)
					#Log("6) remove dupes", time.time() - timer_tile_start)

					# Remove temp_prefix from original names
					for obj in objects_in_bounds:
						obj.name = obj.name.replace(temp_prefix, '')

					pass

				# If no objects are in the bounds, skip the export and set the src to none
				else:
					self.count_skipped += 1
					tile_data["src"] = None;


				# Update the progress bar
				self.UI_UpdateProgress()				
				
				# Add the tile_data to the array of tiles
				Log(str(self.count_processed), tile_data["src"], "took", time.time() - tile_time_start)
				self.tileset_data["tiles"][x][y].append(tile_data)
				self.count_processed += 1

				# Increment the indexes
				self.tileset_index[2] += 1

				# Check if Z has overrun and increment Y
				if self.tileset_index[2] > (z_max - 1):
					self.tileset_index[2] = 0
					self.tileset_index[1] += 1

				# Check if Y has overrun and increment X
				if self.tileset_index[1] > (y_max - 1):
					self.tileset_index[1] = 0
					self.tileset_index[0] += 1

				# If X has overrun, then we're done and finished
				if self.tileset_index[0] > (x_max - 1):
					
					# Cleanup after, remove the Bools used for cutting
					for obj in self.collection.all_objects:
						RemoveIntersectBooleans(obj, self.cutter)
						pass

					# Swizzle the data if required
					if ss_settings.swizzle_yz:
						self.tileset_data = SwizzleTilesetData(self.tileset_data)

					# Export the tileset json
					file_path = GetExportPath("tileset.json")
					ExportDataToJSON(self.tileset_data, file_path, ss_settings.minify_json)

					# Logging
					Log("-----------------------------------------------------")
					Log("Processed", self.count_processed, "tiles, skipped", self.count_skipped, "-", self.count_skipped_empty, "had 0 tris after bool)")
					Log("Total time taken:", str(time.time() - self.time_start))

					self.UI_UpdateProgress()

					# Return and show info
					report = f"Exported {str(self.count_processed - self.count_skipped)} of {str(self.count_processed)} tiles"
					self.report({'INFO'}, report)
					return {'FINISHED'}
			
			# Otherwise we've completed the batch
			# Update progress
		return {'PASS_THROUGH'}
	

	def UI_UpdateProgress(self):
		# Get scene slicer settings
		ss_settings = bpy.context.scene.ss_settings

		# Setup progress indicator
		ss_settings.export_text     = f"{self.count_processed} of {self.count_total}"
		ss_settings.export_progress = self.count_processed / self.count_total

		# Update the UI
		RefreshUI()

	def UI_ResetProgress(self):

		# Get scene slicer settings
		ss_settings = bpy.context.scene.ss_settings

		# Setup progress indicator
		ss_settings.export_text     = "Idle"
		ss_settings.export_progress = 0

		Log("SS.ResetProgress")

		# Update the UI
		RefreshUI()

def RefreshUI():
	for wm in bpy.data.window_managers:
		for w in wm.windows:
			for area in w.screen.areas:
				area.tag_redraw()
