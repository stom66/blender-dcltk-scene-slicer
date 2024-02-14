import bpy


def DeleteCollection(
	col           : bpy.types.Collection,
	remove_objects: bool = False,
):
	"""
	Deletes a collection, optionally removing all objects within it
	"""
	# Delete all objects in the scene
	if remove_objects:
		for obj in col.all_objects:   
			#bpy.data.objects.unlink(obj)
			bpy.data.objects.remove(obj)
	
	# Delete the collection itself
	bpy.data.collections.remove(col)
	