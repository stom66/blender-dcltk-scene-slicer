import bpy


from . _main import Main


# ██╗   ██╗███████╗███████╗██████╗     ██╗███╗   ██╗████████╗███████╗██████╗ ███████╗ █████╗  ██████╗███████╗
# ██║   ██║██╔════╝██╔════╝██╔══██╗    ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝
# ██║   ██║███████╗█████╗  ██████╔╝    ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝█████╗  ███████║██║     █████╗  
# ██║   ██║╚════██║██╔══╝  ██╔══██╗    ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗██╔══╝  ██╔══██║██║     ██╔══╝  
# ╚██████╔╝███████║███████╗██║  ██║    ██║██║ ╚████║   ██║   ███████╗██║  ██║██║     ██║  ██║╚██████╗███████╗
#  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝    ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝
#

# UI Main button for exporting
class VIEW3D_PT_SceneSlicer_Export(bpy.types.Operator):
	bl_idname  = "scene.slice_and_export"
	bl_label   = "Main function"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		self.report({'INFO'}, 'Exporting...')
		result = Main()
		return result

# UI button to refresh collection dropdown
class SCENE_OT_RefreshCollections(bpy.types.Operator):
	bl_idname  = "scene.refresh_collections"
	bl_label   = "Refresh Collections"
	bl_options = {'REGISTER'}

	def execute(self, context):
		# Trigger the update_collection_items method
		context.scene.ss_settings.refresh_collections(context)
		return {'FINISHED'}

# UI Panel class
class VIEW3D_PT_SceneSlicer_Main(bpy.types.Panel):
	bl_label       = 'Scene Slicer: Export'
	bl_category    = 'DCL Toolkit'
	bl_region_type = 'UI'
	bl_space_type  = 'VIEW_3D'

	def draw(self, context):
		layout = self.layout

		# Collection dropdown
		row = layout.row()
		row.label(text="Export collection")
		col = row.column(align=True)
		col.prop(context.scene.ss_settings, "export_collection", text="")
		col = row.column(align=True)
		col.operator("scene.refresh_collections", text="", icon='FILE_REFRESH')

		# Output path
		row = layout.row()
		row.label(text="Output path:")
		row.prop(context.scene.ss_settings, "output_path", text="")

		# Grid size
		row = layout.row()
		row.label(text="Grid size:")
		row = layout.row()
		row.prop(context.scene.ss_settings, "tile_dimensions", text="")


		# Btn: Slice and Export
		row = layout.row()
		row.operator(VIEW3D_PT_SceneSlicer_Export.bl_idname, text="Slice and Export", icon="FILE_VOLUME")

class VIEW3D_PT_SceneSlicer_Options(bpy.types.Panel):
	bl_label       = 'Scene Slicer: Advanced Settings'
	bl_category    = 'DCL Toolkit'
	bl_region_type = 'UI'
	bl_space_type  = 'VIEW_3D'
	bl_options     = { 'DEFAULT_CLOSED' }

	def draw(self, context):
		layout = self.layout

		# Bool solver method
		row = layout.row()
		col = row.column(align=False)
		col.label(text="Bool: solver method")
		col = row.column(align=True)
		col.prop(context.scene.ss_settings, "bool_solver", text="")

		# Skip exporting colliders
		row = layout.row()
		col = row.column(align=False)
		col.label(text="Colliders:  skip export")
		col = row.column(align=True)
		col.prop(context.scene.ss_settings, "skip_colliders", text="")

		# Minify JSON
		row = layout.row()
		col = row.column(align=False)
		col.label(text="JSON: minify output")
		col = row.column(align=True)
		col.prop(context.scene.ss_settings, "minify_json", text="")
	
		# glTF settings
		row = layout.row()
		row.label(text="glTF Settings:")
		box = layout.box()

		# Draco compression
		row = box.row()
		col = row.column(align=False)
		col.label(text="Draco compression")
		col = row.column(align=True)
		col.prop(context.scene.ss_settings, "use_draco", text="")
	
		# glTF export format
		row = box.row()
		col = row.column(align=False)
		col.label(text="Export format")
		col = row.column(align=True)
		col.prop(context.scene.ss_settings, "export_format", text="")

		# Tile prefix
		row = box.row()
		row.label(text="Filename prefix")
		col = row.column(align=True)
		col.prop(context.scene.ss_settings, "output_prefix", text="")

		# Tile origin
		row = box.row()
		row.label(text="Tile origin")
		col = row.column(align=True)
		col.prop(context.scene.ss_settings, "export_origin", text="")
