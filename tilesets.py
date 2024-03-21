import bpy
import json
import math
import mathutils
import os

from collections import defaultdict
from xml.etree.ElementTree import tostring

from . _settings 	import *
from . boundingBox 	import *
from . tiles		import GetTilePositionMin, GetTilePositionMax, GetTilePositionCenter

# ████████╗██╗██╗     ███████╗███████╗███████╗████████╗███████╗
# ╚══██╔══╝██║██║     ██╔════╝██╔════╝██╔════╝╚══██╔══╝██╔════╝
#    ██║   ██║██║     █████╗  ███████╗█████╗     ██║   ███████╗
#    ██║   ██║██║     ██╔══╝  ╚════██║██╔══╝     ██║   ╚════██║
#    ██║   ██║███████╗███████╗███████║███████╗   ██║   ███████║
#    ╚═╝   ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝   ╚═╝   ╚══════╝
#


def CreateTilesetFromCollection(col: bpy.types.Collection) -> dict[str, object]:
	"""
	Creates tileset data from a collection.

	Args:
	- col (bpy.types.Collection): The Blender collection.

	Returns:
	- Dict[str, object]: A dictionary containing tileset data.
		The dictionary includes the following keys:
		- "name"            : The name of the tileset.
		- "tile_dimensions" : The dimensions of each tile.
		- "tileset_size"    : The size of the tileset.
		- "tileset_origin"  : The origin point of the tileset.
		- "bounds_min"      : The minimum coordinates of the bounding box.
		- "bounds_max"      : The maximum coordinates of the bounding box.
		- "bounds_com"      : The center of mass coordinates of the bounding box.
		- "tiles"           : An empty list for future tile data.
	"""

	# Get scene slicer settings
	ss_settings = bpy.context.scene.ss_settings

	# Convert the tile dimensions to a tuple
	tile_dimensions = (
		ss_settings.tile_dimensions.x,
		ss_settings.tile_dimensions.y,
		ss_settings.tile_dimensions.z,
	)

	# Get bounds min/max points for all objects in the collections
	bounds_min, bounds_max, bounds_com = GetCollectionBounds(col)

	# Use bounds to work out the required tileset size and origin
	tileset_size, tileset_origin = GetTilesetSizeOrigin(bounds_min, bounds_max, tile_dimensions)

	# Build Tileset data
	tileset_data = {
		"version"        : ss_settings.version,
		"name"           : col.name,
		"tileset_size"   : tileset_size,
		"tileset_origin" : tileset_origin,
		"tile_dimensions": tile_dimensions,
		"tile_format"    : ss_settings.export_format,
		"tile_origin"    : ss_settings.export_origin,
		"tile_y_is_up"   : ss_settings.swizzle_yz,
		#"bounds_min"     : bounds_min,
		#"bounds_max"     : bounds_max,
		#"bounds_com"     : bounds_com,
        "tiles": [
            [
                [
                    {
                        "index"     : [x, y, z],
                        "src"       : f"{ss_settings.output_prefix}_{x}_{z}_{y}" if ss_settings.swizzle_yz else f"{ss_settings.output_prefix}_{x}_{y}_{z}",
                        "pos_center": GetTilePositionCenter([x, y, z], tileset_origin, tile_dimensions),
                        "pos_min"   : GetTilePositionMin([x, y, z], tileset_origin, tile_dimensions),
                        "pos_max"   : GetTilePositionMax([x, y, z], tileset_origin, tile_dimensions)
                    }
                    for z in range(tileset_size[2])
                ]
                for y in range(tileset_size[1])
            ]
            for x in range(tileset_size[0])
        ]
	}

	return tileset_data


def GetTilesetSizeOrigin(
	min_bounds     : tuple[int, int, int], 
	max_bounds     : tuple[int, int, int],
	tile_dimensions: tuple[int, int, int]
) -> tuple[
		tuple[int, int, int],
		tuple[int, int, int],
]:
	"""
	Get the size and origin of the tileset based on min and max bounding box coordinates.

	Args:
	- min_bounds (tuple[int, int, int]): The minimum bounding box coordinates.
	- max_bounds (tuple[int, int, int]): The maximum bounding box coordinates.
	- tile_dimensions (tuple[int, int, int]): The dimensions of each tile.

	Returns:
	- tuple[tuple[int, int, int], tuple[int, int, int]]: 
	A tuple containing two tuples - the size and origin of the tileset in each axis.
	"""

	tiles_x, origin_x = GetTilesetAxisSize(min_bounds[0], max_bounds[0], tile_dimensions[0])
	tiles_y, origin_y = GetTilesetAxisSize(min_bounds[1], max_bounds[1], tile_dimensions[1])
	tiles_z, origin_z = GetTilesetAxisSize(min_bounds[2], max_bounds[2], tile_dimensions[2])

	return (tiles_x, tiles_y, tiles_z), (origin_x, origin_y, origin_z)


def GetTilesetAxisSize(
	minPos   : float, 
	maxPos   : float, 
	tile_size: float
) -> tuple[int, float]:
	"""
	Helper function to calculate the count and origin of tiles on a single tileset axis.

	Args:
	- minPos (float): The minimum position on the axis.
	- maxPos (float): The maximum position on the axis.
	- tile_size (float): The size of each tile.

	Returns:
	- tuple[int, float]: A tuple containing the count (int) and origin (float) of tiles on the axis.
	"""

	# Set the default origin - gets adjusted below
	origin = 0

	# First get the distance from 0 -> max
	tileCount = math.ceil(maxPos / tile_size)

	# Then subtract the extra cells if our start position was > 0
	if minPos > 0:
		tiles     = math.floor(minPos / tile_size)
		origin    += tiles * tile_size
		tileCount -= tiles
	# Add on some cells if start position was < 0
	if minPos < 0:
		tiles     = math.ceil(minPos / -tile_size)
		origin    -= tiles * tile_size
		tileCount += tiles

	return tileCount, origin


def SwizzleYZ(data: tuple[float, float, float]) -> tuple[float, float, float]:
	return [data[0], data[2], data[1]]


def SwizzleTilesetData(og_data) -> dict[str, object]:

	new_data = {
		"name"           : og_data["name"],
		"tileset_size"   : SwizzleYZ(og_data["tileset_size"]),
		"tileset_origin" : SwizzleYZ(og_data["tileset_origin"]),
		"tile_dimensions": SwizzleYZ(og_data["tile_dimensions"]),
		"tile_format"    : og_data["tile_format"],
		"tile_origin"    : og_data["tile_origin"],
		"tiles"          : []
	}

	for x in range(new_data["tileset_size"][0]):
		new_data["tiles"].append([])

		for y in range(new_data["tileset_size"][1]):
			new_data["tiles"][x].append([])

			for z in range(new_data["tileset_size"][2]):
				
				og_tile = og_data["tiles"][x][z][y]

				new_data["tiles"][x][y].append({
					"index"     : SwizzleYZ(og_tile["index"]),
					"src"       : og_tile["src"],
					"pos_center": SwizzleYZ(og_tile["pos_center"]),
					"pos_min"   : SwizzleYZ(og_tile["pos_min"]),
					"pos_max"   : SwizzleYZ(og_tile["pos_max"]),
				})

	return new_data
