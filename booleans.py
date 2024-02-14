import bpy



# ██████╗  ██████╗  ██████╗ ██╗         ███╗   ███╗ ██████╗ ██████╗ ███████╗
# ██╔══██╗██╔═══██╗██╔═══██╗██║         ████╗ ████║██╔═══██╗██╔══██╗██╔════╝
# ██████╔╝██║   ██║██║   ██║██║         ██╔████╔██║██║   ██║██║  ██║███████╗
# ██╔══██╗██║   ██║██║   ██║██║         ██║╚██╔╝██║██║   ██║██║  ██║╚════██║
# ██████╔╝╚██████╔╝╚██████╔╝███████╗    ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████║
# ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝    ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
#                                                                           

def AddIntersectBooleans(obj, cutter):
	"""
	Adds an INTERSECT boolean modifier to an object, setting another object as the target.

	:param obj: The object to which the boolean modifier will be added.
	:type obj: bpy.types.Object
	:param cutter: The object to be set as the target for the boolean modifier.
	:type cutter: bpy.types.Object
	:return: None
	"""

	# Ignore non-mesh objects
	if obj.type != 'MESH':
		return
	
	# Check if the object already has an INTERSECT boolean modifier with the specified cutter
	modifier_exists = False
	for modifier in obj.modifiers:
		if modifier.type == 'BOOLEAN' and modifier.operation == 'INTERSECT' and modifier.object == cutter:
			modifier.solver = bpy.context.scene.ss_settings.bool_solver
			modifier_exists = True
			break

	# If no INTERSECT boolean modifier is found, add one
	if not modifier_exists:
		bool_modifier                  = obj.modifiers.new(name = "Boolean", type = 'BOOLEAN')
		bool_modifier.object           = cutter
		bool_modifier.operation        = 'INTERSECT'
		bool_modifier.solver           = bpy.context.scene.ss_settings.bool_solver
		bool_modifier.double_threshold = 0.0001
		bool_modifier.use_hole_tolerant = True


def RemoveIntersectBooleans(obj, cutter):
	"""
	Removes an INTERSECT boolean modifier from an object with the specified target.

	:param obj: The object from which the boolean modifier will be removed.
	:type obj: bpy.types.Object
	:param cutter: The target object of the boolean modifier to be removed.
	:type cutter: bpy.types.Object
	:return: None
	"""

	# Check if the object already has an INTERSECT boolean modifier with the specified target
	for modifier in obj.modifiers:
		if modifier.type == 'BOOLEAN' and modifier.operation == 'INTERSECT' and modifier.object == cutter:
			obj.modifiers.remove(modifier)
			break


def RemoveBrokenBooleans(obj):
	"""
	Removes broken INTERSECT boolean modifiers from an object.

	:param obj: The object from which broken boolean modifiers will be removed.
	:type obj: bpy.types.Object
	:return: None
	"""

	# Check if the object already has an INTERSECT boolean modifier with the specified target
	for modifier in obj.modifiers:
		if modifier.type == 'BOOLEAN' and modifier.operation == 'INTERSECT' and modifier.object == None:
			obj.modifiers.remove(modifier)
			break
