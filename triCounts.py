import bpy



# ████████╗██████╗ ██╗     ██████╗ ██████╗ ██╗   ██╗███╗   ██╗████████╗
# ╚══██╔══╝██╔══██╗██║    ██╔════╝██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝
#    ██║   ██████╔╝██║    ██║     ██║   ██║██║   ██║██╔██╗ ██║   ██║   
#    ██║   ██╔══██╗██║    ██║     ██║   ██║██║   ██║██║╚██╗██║   ██║   
#    ██║   ██║  ██║██║    ╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║   ██║   
#    ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   
#

def GetTotalTriCount(objects: bpy.types.Object) -> int:
	"""
	Gets the total triangle count of all the given objects.

	Note: This function relies on the GetTriCount function to calculate the triangle count for each visible mesh object.

	:return: The total visible triangle count.
	:rtype: int
	"""
	count = 0
	for object in objects:
		count += len(object.data.polygons)

	return count


def GetDuplicatedObjectTriCount(obj) -> int:
	"""
	Gets the triangle count of an object, after it has had all its modifiers applied

	Note: This function creates a duplicate of the object, adds a Triangulate modifier, and converts it to mesh to calculate
	the triangle count. This approach very resource-intensive.

	:param obj: The object for which the triangle count will be calculated.
	:type obj: bpy.types.Object
	:return: The triangle count of the object.
	:rtype: int
	"""

	# Create a duplicate of the object
	duplicate_obj      = obj.copy()
	duplicate_obj.data = obj.data.copy()
	bpy.context.collection.objects.link(duplicate_obj)

	# Add a Triangulate modifier
	duplicate_obj.modifiers.new(name='Triangulate', type='TRIANGULATE')

	# Set the original object as the active object
	bpy.context.view_layer.objects.active = duplicate_obj
	duplicate_obj.select_set(True)
	
	# Switch to Object Mode
	bpy.ops.object.mode_set(mode='OBJECT')

	# Convert to mesh and apply modifiers
	bpy.ops.object.convert(target='MESH', keep_original=False)

	# Get the triangle count
	tri_count = len(duplicate_obj.data.polygons)

	# Remove the duplicate object
	bpy.data.objects.remove(duplicate_obj)

	return tri_count
