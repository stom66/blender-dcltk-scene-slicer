import bpy
import time

from . logging import Log



# ██████╗ ██╗   ██╗██████╗ ██╗     ██╗ ██████╗ █████╗ ████████╗ ██████╗ ██████╗ 
# ██╔══██╗██║   ██║██╔══██╗██║     ██║██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
# ██║  ██║██║   ██║██████╔╝██║     ██║██║     ███████║   ██║   ██║   ██║██████╔╝
# ██║  ██║██║   ██║██╔═══╝ ██║     ██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗
# ██████╔╝╚██████╔╝██║     ███████╗██║╚██████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
# ╚═════╝  ╚═════╝ ╚═╝     ╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
#

def DuplicateObjects(
	objects    : list[bpy.types.Object],
	new_origin : tuple[float, float, float],
	temp_prefix: str
) -> list[bpy.types.Object]:
	"""
	Duplicate a list of Blender objects, applying modifiers and updating the origin.
	Note that this function will set the origin to the current 3d cursor position,
	then move the object to 0,0,0

	:param objects: List of Blender objects to duplicate.
	:type objects: list[bpy.types.Object]

	:param temp_prefix: Prefix to be added to the original objects' names temporarily.
	:type temp_prefix: str

	:return: List of duplicated objects with applied modifiers and updated origins.
	:rtype: list[bpy.types.Object]
	"""
	time_start = time.time()

	# Ensure nothing is selected
	bpy.ops.object.select_all(action='DESELECT')

	# Create a blank list to store the duplicated objects
	duplicate_objects = []

	# Set the 3d cursor to the new origin
	bpy.context.scene.cursor.location = new_origin
	
	# Clone objects, apply their modifiers, set their origins
	for index, obj in enumerate(objects):
		t = time.time
		time_object_start = t

		# Create a duplicate of the object
		duplicate_obj      = obj.copy()
		duplicate_obj.data = obj.data.copy()
		bpy.context.collection.objects.link(duplicate_obj)

		# Rename the original temporarily and ensure the clone has the original name
		# We do this so that the exported model doesn't end up with different mesh names
		original_name      = obj.name
		obj.name           = temp_prefix + original_name
		duplicate_obj.name = original_name
		
		# Set the duplicate object as the active object
		bpy.context.view_layer.objects.active = duplicate_obj
		duplicate_obj.select_set(True)
		
		#Log("    ", index, "rename and set active took", time.time() - time_object_start)

		# Ensure we're in Object Mode
		bpy.ops.object.mode_set(mode='OBJECT')

		# If the object had a rigidbody, remove it
		if obj.rigid_body is not None:
			bpy.ops.rigidbody.object_remove()

		# Convert to mesh and apply modifiers
		bpy.ops.object.convert(target='MESH', keep_original=False)

		# Update the objects origin to match the 3d cursor
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

		# Add the duplicate object to the list
		duplicate_objects.append(duplicate_obj)
	
	# Move all the objects AFTER we have duplicated them, otherwise some origins are incorrect
	#for obj in duplicate_objects:
	#	obj.location = (0, 0, 0)
	
	
	Log("DuplicateObjects took", time.time() - time_start, "for", len(objects), "objects")
	return duplicate_objects