import bpy 


# ████████╗██╗██╗     ███████╗    ███╗   ███╗ █████╗ ████████╗██╗  ██╗
# ╚══██╔══╝██║██║     ██╔════╝    ████╗ ████║██╔══██╗╚══██╔══╝██║  ██║
#    ██║   ██║██║     █████╗      ██╔████╔██║███████║   ██║   ███████║
#    ██║   ██║██║     ██╔══╝      ██║╚██╔╝██║██╔══██║   ██║   ██╔══██║
#    ██║   ██║███████╗███████╗    ██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║
#    ╚═╝   ╚═╝╚══════╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
#                                                               
			  
def GetTilePositionMin(grid_coords, tileset_origin, tile_dimensions) -> tuple[float, float, float]:
	"""
	Returns the lowest coordinates of the cell (its bottom corner).

	Args:
	- grid_coords (Tuple[float, float, float]): The grid coordinates of the cell.
	- tileset_origin: tuple[float, float, float]
	- tile_dimensions: tuple[float, float, float] 

	Returns:
	- Tuple[float, float, float]: The minimum coordinates of the cell.
	"""

	x = tileset_origin[0] + (grid_coords[0] * tile_dimensions[0])
	y = tileset_origin[1] + (grid_coords[1] * tile_dimensions[1])
	z = tileset_origin[2] + (grid_coords[2] * tile_dimensions[2])

	return x, y, z


def GetTilePositionMax(grid_coords, tileset_origin, tile_dimensions) -> tuple[float, float, float]:
	"""
	Returns the highest coordinates of the cell (its upper-most corner)

	Args:
	- grid_coords (Tuple[float, float, float]): The grid coordinates of the cell.
	- tileset_origin: tuple[float, float, float]
	- tile_dimensions: tuple[float, float, float] 

	Returns:
	- Tuple[float, float, float]: The maximum coordinates of the cell.
	"""

	[min_x, min_y, min_z] = GetTilePositionMin(grid_coords, tileset_origin, tile_dimensions)

	max_coords = (
		min_x + tile_dimensions[0],
		min_y + tile_dimensions[1],
		min_z + tile_dimensions[2]
	)

	return max_coords


def GetTilePositionCenter(grid_coords, tileset_origin, tile_dimensions) -> tuple[float, float, float]:
	"""
	Returns the center coordinates of the cell.

	Args:
	- grid_coords (Tuple[float, float, float]): The grid coordinates of the cell.
	- tileset_origin: tuple[float, float, float]
	- tile_dimensions: tuple[float, float, float] 

	Returns:
	- Tuple[float, float, float]: The center coordinates of the cell.
	"""

	[min_x, min_y, min_z] = GetTilePositionMin(grid_coords, tileset_origin, tile_dimensions)
	
	center_coords = (
		min_x + (tile_dimensions[0] / 2),
		min_y + (tile_dimensions[1] / 2),
		min_z + (tile_dimensions[2] / 2)
	)

	return center_coords