import bpy


def DeleteCollection(
	col           : bpy.types.Collection,
	remove_objects: bool = False,
) -> bool:
	"""
	Deletes a collection, optionally removing all objects within it
	"""

	# Delete all objects in the scene
	if remove_objects:
		# Make a list for all objects in the collection
		# If we try and loop through the collection and delete at the same time, Blender may crash
		objects = []
		for obj in col.all_objects:
			obj.select_set(False)
			objects.append(obj)

		for obj in objects:   
			bpy.data.objects.remove(obj)
	
	# Delete the collection itself
	bpy.data.collections.remove(col)
	
	return True
