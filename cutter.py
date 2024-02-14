import bpy



#  ██████╗██╗   ██╗████████╗████████╗███████╗██████╗ 
# ██╔════╝██║   ██║╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗
# ██║     ██║   ██║   ██║      ██║   █████╗  ██████╔╝
# ██║     ██║   ██║   ██║      ██║   ██╔══╝  ██╔══██╗
# ╚██████╗╚██████╔╝   ██║      ██║   ███████╗██║  ██║
#  ╚═════╝ ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝
#

CUTTER_NAME = "SS_Cutter"
	
def CreateCutter(tileset) -> object:
	"""
	Creates a cutter cube for slicing, ensuring it is in the correct collection and at the right size.

	Returns:
	bpy.types.Object: The created or existing cutter cube object.
	"""

	# Check if "Cutters" collection already exists
	cutters_collection = bpy.data.collections.get("Cutters")

	# If "Cutters" collection doesn't exist, create it
	if cutters_collection is None:
		cutters_collection = bpy.data.collections.new("Cutters")
		bpy.context.scene.collection.children.link(cutters_collection)
 
	# Check if the cube already exists
	cutter = bpy.data.objects.get(CUTTER_NAME)

	# Create a cube with size based on TILE_SIZE_X, TILE_SIZE_Y, TILE_SIZE_Z
	if cutter is None:
		bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
		cutter              = bpy.context.active_object
		cutter.name         = CUTTER_NAME
		cutter.display_type = 'WIRE'

	# Ensure the cutter cube is at the correct size for our slicing
	cutter.scale = tileset["tile_dimensions"]
		
	# Clear existing collections and ensure our cutter cube is on the right collection
	for col in cutter.users_collection:
		col.objects.unlink(cutter)
		
	cutters_collection.objects.link(cutter)

	return cutter



#  ██████╗██╗   ██╗████████╗████████╗███████╗██████╗     ██╗  ██╗███████╗██╗     ██████╗ ███████╗██████╗ 
# ██╔════╝██║   ██║╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗    ██║  ██║██╔════╝██║     ██╔══██╗██╔════╝██╔══██╗
# ██║     ██║   ██║   ██║      ██║   █████╗  ██████╔╝    ███████║█████╗  ██║     ██████╔╝█████╗  ██████╔╝
# ██║     ██║   ██║   ██║      ██║   ██╔══╝  ██╔══██╗    ██╔══██║██╔══╝  ██║     ██╔═══╝ ██╔══╝  ██╔══██╗
# ╚██████╗╚██████╔╝   ██║      ██║   ███████╗██║  ██║    ██║  ██║███████╗███████╗██║     ███████╗██║  ██║
#  ╚═════╝ ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝
#

def ToggleCutterHelper():
	"""
	Toggle the visibility of the cutter helper object. If it doesn't exist, create it.
	If it exists, delete it.
	"""
	# Check if the cube already exists
	cutter_helper = bpy.data.objects.get(CUTTER_NAME + "Helper")

	if cutter_helper is None:
		CreateCutterHelper()
	else:
		bpy.data.objects.remove(cutter_helper, do_unlink=True)


	
def CreateCutterHelper(tileset) -> object:
	"""
	Create or update the cutter helper cube for slicing.

	:param tileset: Data containing information about the tileset.
	:type tileset: dict

	:return: The created or updated cutter helper object.
	:rtype: bpy.types.Object
	"""
	# shorthand references to the values we need
	tileset_origin  = tileset["tileset_origin"] 	# [float, float, float]
	tileset_size    = tileset["tileset_size"] 		# [int, int, int]
	tile_dimensions = tileset["tile_dimensions"] 	# [float, float, float]

	# Check if "Cutters" collection already exists
	cutters_collection = bpy.data.collections.get("Cutters")

	# If "Cutters" collection doesn't exist, create it
	if cutters_collection is None:
		cutters_collection = bpy.data.collections.new("Cutters")
		bpy.context.scene.collection.children.link(cutters_collection)
 
	# Check if the cube already exists
	cutter_helper = bpy.data.objects.get(CUTTER_NAME + "Helper")

	# Create a cube with size based on TILE_SIZE_X, TILE_SIZE_Y, TILE_SIZE_Z
	if cutter_helper is None:
		bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
		cutter_helper              = bpy.context.active_object
		cutter_helper.name         = CUTTER_NAME + "Helper"
		cutter_helper.display_type = 'WIRE'

	# Ensure the cutter cube is at the correct size and position for our slicing
	cutter_helper.scale    = tile_dimensions
	cutter_helper.location = (
		tileset_origin[0] + tile_dimensions[0] / 2,
		tileset_origin[1] + tile_dimensions[1] / 2,
		tileset_origin[2] + tile_dimensions[2] / 2
	)

	# Ensure we have three array modifiers and they are set to the correct values
	AddArray(cutter_helper, "TileX", tileset_size[0], [1,0,0])
	AddArray(cutter_helper, "TileY", tileset_size[1], [0,1,0])
	AddArray(cutter_helper, "TileZ", tileset_size[2], [0,0,1])
		
	# Clear existing collections and ensure our cutter cube is on the right collection
	for col in cutter_helper.users_collection:
		col.objects.unlink(cutter_helper)
		
	cutters_collection.objects.link(cutter_helper)

	# Ensure it's not selected
	cutter_helper.select_set(False)

	return cutter_helper


def AddArray(obj, name, count, relative_offset):
	"""
	Add or update an array modifier to an object.

	:param obj: The object to which the array modifier will be added or updated.
	:type obj: bpy.types.Object

	:param name: The name of the array modifier.
	:type name: str

	:param count: The count parameter of the array modifier.
	:type count: int

	:param relative_offset: The relative offset displacement of the array modifier.
	:type relative_offset: bpy.types.Vector
	"""

	# Check if the array modifier already exists
	for modifier in obj.modifiers:
		if modifier.type == 'ARRAY' and modifier.name == name:
			modifier.count = count
			modifier.relative_offset_displace = relative_offset
			return

	# Add the array modifier
	array_modifier                          = obj.modifiers.new(name = name, type = 'ARRAY')
	array_modifier.count                    = count
	array_modifier.relative_offset_displace = relative_offset

