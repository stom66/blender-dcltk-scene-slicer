import bpy 


# ████████╗██╗██╗     ███████╗    ███╗   ███╗ █████╗ ████████╗██╗  ██╗
# ╚══██╔══╝██║██║     ██╔════╝    ████╗ ████║██╔══██╗╚══██╔══╝██║  ██║
#    ██║   ██║██║     █████╗      ██╔████╔██║███████║   ██║   ███████║
#    ██║   ██║██║     ██╔══╝      ██║╚██╔╝██║██╔══██║   ██║   ██╔══██║
#    ██║   ██║███████╗███████╗    ██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║
#    ╚═╝   ╚═╝╚══════╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
#                                                               
			  
def GetTilePositionMin(grid_coords, tileset_data) -> tuple[float, float, float]:
	"""
	Returns the lowest coordinates of the cell (its bottom corner).

	:param grid_coords: The grid coordinates of the cell.
	:type grid_coords: Tuple[float, float, float]
	:param tileset_data: The tileset data.
	:type tileset_data: Object{... tile_dimensions: Vector ...}
	:return: The minimum coordinates of the cell.
	:rtype: Vector
	"""
	
	tileset_origin  = tileset_data["tileset_origin"]
	tile_dimensions = tileset_data["tile_dimensions"]

	x = tileset_origin[0] + (grid_coords[0] * tile_dimensions[0])
	y = tileset_origin[1] + (grid_coords[1] * tile_dimensions[1])
	z = tileset_origin[2] + (grid_coords[2] * tile_dimensions[2])

	return x, y, z


def GetTilePositionMax(grid_coords, tileset_data) -> tuple[float, float, float]:
	"""
	Returns the highest coordinates of the cell (its upper-most corner)

	:param grid_coords: The grid coordinates of the cell.
	:type grid_coords: Tuple[float, float, float]
	:param tileset_data: The tileset data.
	:type tileset_data: Object{... tile_dimensions: Vector ...}
	:return: The maximum coordinates of the cell.
	:rtype: Vector
	"""

	[min_x, min_y, min_z] = GetTilePositionMin(grid_coords, tileset_data)

	max_coords = (
		min_x + tileset_data["tile_dimensions"][0],
		min_y + tileset_data["tile_dimensions"][1],
		min_z + tileset_data["tile_dimensions"][2]
	)

	return max_coords


def GetTilePositionCenter(grid_coords, tileset_data) -> tuple[float, float, float]:
	"""
	Returns the center coordinates of the cell.

	:param grid_coords: The grid coordinates of the cell.
	:type grid_coords: Tuple[float, float, float]
	:param tileset_data: The tileset data.
	:type tileset_data: Object{... tile_dimensions: Vector ...}
	:return: The center coordinates of the cell.
	:rtype: Vector
	"""


	[min_x, min_y, min_z] = GetTilePositionMin(grid_coords, tileset_data)
	
	center_coords = (
		min_x + (tileset_data["tile_dimensions"][0] / 2),
		min_y + (tileset_data["tile_dimensions"][1] / 2),
		min_z + (tileset_data["tile_dimensions"][2] / 2)
	)

	return center_coords