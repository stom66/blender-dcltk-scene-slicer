import bpy

from mathutils 	import Vector
from typing 	import Optional


ROUNDING_PRECISION = 3

def custom_round(number, decimal_places):
	factor       = 10 ** decimal_places
	result       = round(number * factor) / factor
	return result



# ██████╗ ██████╗      ██████╗ ██╗   ██╗███████╗██████╗ ██╗      █████╗ ██████╗ 
# ██╔══██╗██╔══██╗    ██╔═══██╗██║   ██║██╔════╝██╔══██╗██║     ██╔══██╗██╔══██╗
# ██████╔╝██████╔╝    ██║   ██║██║   ██║█████╗  ██████╔╝██║     ███████║██████╔╝
# ██╔══██╗██╔══██╗    ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██║     ██╔══██║██╔═══╝ 
# ██████╔╝██████╔╝    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║███████╗██║  ██║██║     
# ╚═════╝ ╚═════╝      ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     
#                                                                               

def GetObjectsWithinBounds(
		objects   : dict[bpy.types.Object, tuple[tuple[float, float, float], tuple[float, float, float]]], 
		bounds_min: tuple[float, float, float], 
		bounds_max: tuple[float, float, float]
    ) -> list[bpy.types.Object]:
	"""
	Checks if there are any mesh objects within the specified bounding box.

	:param objects: Dictionary mapping mesh objects to their bounding box coordinates.
	:type objects: dict[bpy.types.Object, tuple[tuple[float, float, float], tuple[float, float, float]]]

	:param bounds_min: The minimum coordinates of the bounding box.
	:type bounds_min: Tuple[float, float, float]

	:param bounds_max: The maximum coordinates of the bounding box.
	:type bounds_max: Tuple[float, float, float]

	:return: Tuple containing a boolean indicating if there are objects within the bounding box
				and a list of objects (or None if no objects are found).
	:rtype: Tuple[bool, Optional[List[bpy.types.Object]]]
	"""

	# Get scene slicer settings
	ss_settings = bpy.context.scene.ss_settings

	# Create a list to store the objects in
	objects_in_bounds = []

	for obj, obj_bounds in objects.items():

		# Check if we're skipping colliders
		if ss_settings.skip_colliders and obj.name.endswith("_collider"):
			continue

		
		if obj.type == 'MESH':
			
			# Extract the minimum and maximum bounds for the current object
			obj_bounds_min, obj_bounds_max = obj_bounds

			# Check if bounding boxes intersect or if one object is completely inside the other
			x_overlap = (bounds_max[0] > obj_bounds_min[0]) and (bounds_min[0] < obj_bounds_max[0])
			y_overlap = (bounds_max[1] > obj_bounds_min[1]) and (bounds_min[1] < obj_bounds_max[1])
			z_overlap = (bounds_max[2] > obj_bounds_min[2]) and (bounds_min[2] < obj_bounds_max[2])

			# If all three axis overlap, then it's a true overlap. Add the object to the list
			if x_overlap and y_overlap and z_overlap:
				objects_in_bounds.append(obj)
				#return True

	# Return true/false if objects were in bounds, plus a list of the objects
	return objects_in_bounds



#  ██████╗ ███████╗████████╗    ██████╗  ██████╗ ██╗   ██╗███╗   ██╗██████╗ ███████╗
# ██╔════╝ ██╔════╝╚══██╔══╝    ██╔══██╗██╔═══██╗██║   ██║████╗  ██║██╔══██╗██╔════╝
# ██║  ███╗█████╗     ██║       ██████╔╝██║   ██║██║   ██║██╔██╗ ██║██║  ██║███████╗
# ██║   ██║██╔══╝     ██║       ██╔══██╗██║   ██║██║   ██║██║╚██╗██║██║  ██║╚════██║
# ╚██████╔╝███████╗   ██║       ██████╔╝╚██████╔╝╚██████╔╝██║ ╚████║██████╔╝███████║
#  ╚═════╝ ╚══════╝   ╚═╝       ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚══════╝
#

def GetObjectBounds(obj: object) -> tuple[
		tuple[float, float, float], 
		tuple[float, float, float]
	]:
	"""
	Get the bounding box coordinates of an object.

	:param obj: The object.
	:type obj: bpy.types.object

	:return: A tuple of tuples representing the minimum and maximum bounds.
	:rtype: tuple[
				tuple[float, float, float], 
				tuple[float, float, float]
			]
	"""

	# Start with some min and max values
	min_xyz = [ float('inf'),  float('inf'),  float('inf')]
	max_xyz = [-float('inf'), -float('inf'), -float('inf')]
	
	# Check each bounding box corner, in world space
	for v in obj.bound_box:
		v_world = obj.matrix_world @ Vector((v[0], v[1], v[2]))

		# Update min/max for each axis
		for i in range(3):
			min_xyz[i] = min(min_xyz[i], custom_round(v_world[i], ROUNDING_PRECISION))
			max_xyz[i] = max(max_xyz[i], custom_round(v_world[i], ROUNDING_PRECISION))
	
	return min_xyz, max_xyz


def GetCollectionObjectBounds(col: bpy.types.Collection) -> dict[
		bpy.types.Object, 
		tuple[
			tuple[float, float, float], 
			tuple[float, float, float]
		]
	]:
	"""
	Get a dict of all object bounds in a collection. 

	:param col: The Blender collection containing objects.
	:type col: bpy.types.Collection

	:return: A dictionary mapping objects to their min and max bounding box coordinates.
	:rtype: Dict[
				bpy.types.Object, 
				tuple[
					tuple[float, float, float],
					tuple[float, float, float]
				]
			]
	"""

	# Get scene slicer settings
	ss_settings = bpy.context.scene.ss_settings

	# Blank dict to store the results
	object_bounds = {}
	
	# Get the bounds for each object in the collection and store it with the object reference as the key
	for obj in col.all_objects:
		if ss_settings.skip_colliders and obj.name.endswith("_collider"):
			continue

		object_bounds[obj] = GetObjectBounds(obj)
	
	return object_bounds


def GetCollectionBounds(col: bpy.types.Collection) -> tuple[
		tuple[float, float, float], 
		tuple[float, float, float], 
		tuple[float, float, float]
	]:
	"""
	Calculate the minimum and maximum bounds as well as the center of mass of objects in a collection.

	:param col: The Blender collection containing objects.
	:type col: bpy.types.Collection
	:return: A tuple containing the minimum bounds, maximum bounds, and center of mass.
	:rtype: Tuple[Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]]
	"""

	# Start with some min and max values
	min_xyz = [ float('inf'),  float('inf'),  float('inf')]
	max_xyz = [-float('inf'), -float('inf'), -float('inf')]

	## Loop through all the objects in the collection and their bounding boxes
	for obj in col.all_objects:

		# Check each bounding box corner, in world space
		for v in obj.bound_box:
			v_world = obj.matrix_world @ Vector((v[0], v[1], v[2]))

			# Update min/max for each axis
			for i in range(3):
				min_xyz[i] = min(min_xyz[i], custom_round(v_world[i], ROUNDING_PRECISION))
				max_xyz[i] = max(max_xyz[i], custom_round(v_world[i], ROUNDING_PRECISION))

	center_of_mass = [
		round(((max_xyz[i] - min_xyz[i]) / 2 ) + min_xyz[i], ROUNDING_PRECISION)
		for i in range(3)
	]

	return min_xyz, max_xyz, center_of_mass
	