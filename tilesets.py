import bpy
import json
import math
import mathutils
import os
from mathutils import Vector
from collections import defaultdict
from xml.etree.ElementTree import tostring



# ████████╗██╗██╗     ███████╗███████╗███████╗████████╗███████╗
# ╚══██╔══╝██║██║     ██╔════╝██╔════╝██╔════╝╚══██╔══╝██╔════╝
#    ██║   ██║██║     █████╗  ███████╗█████╗     ██║   ███████╗
#    ██║   ██║██║     ██╔══╝  ╚════██║██╔══╝     ██║   ╚════██║
#    ██║   ██║███████╗███████╗███████║███████╗   ██║   ███████║
#    ╚═╝   ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝   ╚═╝   ╚══════╝
#

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

	:param min_coords: The minimum bounding box coordinates.
	:type min_coords: tuple
	:param max_coords: The maximum bounding box coordinates.
	:type max_coords: tuple
	:return: A tuple containing two lists - the size and origin of the tileset in each axis.
	:rtype: tuple
	"""

	tiles_x, origin_x = GetTilesetAxisSize(min_bounds[0], max_bounds[0], tile_dimensions[0])
	tiles_y, origin_y = GetTilesetAxisSize(min_bounds[1], max_bounds[1], tile_dimensions[1])
	tiles_z, origin_z = GetTilesetAxisSize(min_bounds[2], max_bounds[2], tile_dimensions[2])

	return [tiles_x, tiles_y, tiles_z], [origin_x, origin_y, origin_z]


def GetTilesetAxisSize(
	minPos   : float, 
	maxPos   : float, 
	tile_size: float
) -> tuple[
	int,
	float
]:
	"""
	Helper function to calculate the length and origin of a single tileset axis.

	:param minPos: The minimum position on the axis.
	:type minPos: float
	:param maxPos: The maximum position on the axis.
	:type maxPos: float
	:param tile_size: The size of each tile.
	:type tile_size: float
	:return: A tuple containing the count (int) and origin (float) of tiles on the axis.
	:rtype: tuple
	"""
	
	# Set the default origin - gets adjusted below
	origin = 0

	# First get the distance from 0 -> max
	tileCount = math.ceil(maxPos / tile_size)

	# Then subtract the extra cells if our start position was > 0
	if minPos > 0:
		tiles     =  math.floor(minPos / tile_size)
		origin    += tiles * tile_size
		tileCount += tiles
	# Add on some cells if start position was < 0
	if minPos < 0:
		tiles     =  math.ceil(minPos / -tile_size)
		origin    -= tiles * tile_size
		tileCount += tiles

	return tileCount, origin


