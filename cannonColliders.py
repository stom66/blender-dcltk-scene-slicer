import bpy

class EXPORT_OT_CannonColliders(bpy.types.Operator):
	bl_idname  = "cc.export"
	bl_label   = "Export Cannon Colliders"
	bl_options = {'REGISTER', 'UNDO'}

	filepath: bpy.props.StringProperty(subtype="FILE_PATH")  # type: ignore

	def execute(self, context):
		# Your export logic goes here
		# Use self.filepath to get the export path

		# Call the Main function
		result = CC_Main()

		# Report the result
		if result:
			self.report({'INFO'}, 'Cannon colliders exported successfully')
			return {'FINISHED'}
		else:
			self.report({'ERROR'}, 'Failed to export cannon colliders')
			return {'CANCELLED'}

	#def invoke(self, context, event):
	#	# Open the file dialog
	#	context.window_manager.fileselect_add(self)
	#	return {'RUNNING_MODAL'}


def CC_Main():
	# Ensure nothing is selected
	bpy.ops.object.select_all(action='DESELECT')
	
	# Get collider exporter settings
	cc_settings = bpy.context.scene.cc_settings

	# Get the chosen collection in the panel
	col = bpy.data.collections.get(cc_settings.export_collection)

	# Blank dict for storing RB objects and their properties
	rb_objects = {}

	# Loop through all collection objects, and gt the RB properties
	for obj in col.all_objects:
		if obj.type == 'MESH' and obj.rigid_body is not None:
			rb_objects[obj] = GetObjectRBProperties(obj)

	# Add the properties of each object to  dict
	pass

	return True

			
def GetObjectRBProperties(obj: bpy.types.Object):

	obj_data = {
		"vertices"   : [],
		"indices"    : [],
		"shape"      : "",
		"friction"   : 0,
		"restitution": 0,
		"mass"       : 0,
		"type"       : "",
	}

	mesh = obj.data
	for vertex in mesh.vertices:
		obj_data["vertices"].append(tuple(vertex.co))

	for face in mesh.polygons:
		obj_data["indices"].extend(face.vertices)

	# Physics properties
	obj_data["shape"]       = obj.rigid_body.collision_shape
	obj_data["friction"]    = obj.rigid_body.friction
	obj_data["restitution"] = obj.rigid_body.restitution
	obj_data["mass"]        = obj.rigid_body.mass
	obj_data["type"]        = obj.rigid_body.type

	return obj_data