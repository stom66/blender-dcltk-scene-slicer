import bpy

#
# NOTE: This file is redundant and can be removed. Keeping it around for posterity/reference
#

# ████████╗██████╗ ██╗     ██████╗ ██████╗ ██╗   ██╗███╗   ██╗████████╗
# ╚══██╔══╝██╔══██╗██║    ██╔════╝██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝
#    ██║   ██████╔╝██║    ██║     ██║   ██║██║   ██║██╔██╗ ██║   ██║   
#    ██║   ██╔══██╗██║    ██║     ██║   ██║██║   ██║██║╚██╗██║   ██║   
#    ██║   ██║  ██║██║    ╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║   ██║   
#    ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   
#
	
def GetVisbileTriCount() -> int:
	"""
	Gets the total visible triangle count of all visible mesh objects in the scene.

	Note: This function relies on the GetTriCount function to calculate the triangle count for each visible mesh object.

	:return: The total visible triangle count.
	:rtype: int
	"""
	
	total_tri_count = 0
	for obj in bpy.context.visible_objects:
		if obj.type == 'MESH' and obj.visible_camera:
			total_tri_count += GetObjectTriCount(obj)

	return total_tri_count


def GetCollectionVisibleTriCount(col: bpy.types.Collection) -> int:
	"""
	Gets the total visible triangle count of all visible mesh objects in the specified collection.

	Note: This function relies on the GetObjectTriCount function to calculate the triangle count for each visible mesh object.

	:param col: The collection for which the visible triangle count will be calculated.
	:type col: bpy.types.Collection
	:return: The total visible triangle count in the collection.
	:rtype: int
	"""

	total_tri_count = 0
	for obj in col.all_objects:
		if obj.type == 'MESH' and obj.visible_camera:
			total_tri_count += GetObjectTriCount(obj)

	return total_tri_count


def GetObjectTriCount(obj) -> int:
	"""
	Gets the triangle count of an object, taking modifiers into account.

	Note: This function creates a duplicate of the object, adds a Triangulate modifier, and converts it to mesh to calculate
	the triangle count. This approach may be resource-intensive.

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
