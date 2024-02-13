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
	bl_label       = 'Scene Slicer'
	bl_category    = 'Scene Slicer'
	bl_region_type = 'UI'
	bl_space_type  = 'VIEW_3D'

	def draw(self, context):
		layout = self.layout

		# Collection dropdown
		row = layout.row()
		row.label(text="Collection to export")
		col = row.column(align=True)
		col.prop(context.scene.ss_settings, "export_collection", text="")
		col = row.column(align=True)
		col.operator("scene.refresh_collections", text="", icon='FILE_REFRESH')

		# Output path
		row = layout.row()
		row.label(text="Output Path:")
		row.prop(context.scene.ss_settings, "output_path", text="")

		#row = layout.row()
		#row.label(text="Collection Prefix:")
		#row.prop(context.scene.ss_settings, "collection_prefix", text="")

		# Grid size
		row = layout.row()
		row.label(text="Grid Size:")
		row = layout.row()
		row.prop(context.scene.ss_settings, "tile_dimensions", text="")


		# Btn: Slice and Export
		row = layout.row()
		row.operator(VIEW3D_PT_SceneSlicer_Export.bl_idname, text="Slice and Export", icon="FILE_VOLUME")

class VIEW3D_PT_SceneSlicer_Options(bpy.types.Panel):
	bl_label       = 'Advanced Settings'
	bl_category    = 'Scene Slicer'
	bl_region_type = 'UI'
	bl_space_type  = 'VIEW_3D'
	bl_options     = { 'DEFAULT_CLOSED' }

	def draw(self, context):
		layout = self.layout

		# Tile origin
		row = layout.row()
		row.label(text="Tile origin")
		col = row.column(align=True)
		col.prop(context.scene.ss_settings, "export_origin", text="")

		# Minify JSON
		row = layout.row()
		col = row.column(align=False)
		col.label(text="Minify tileset JSON")

		col = row.column(align=True)
		col.prop(context.scene.ss_settings, "minify_json", text="")

	
		# use Draco compression
		row = layout.row()
		col = row.column(align=False)
		col.label(text="glTF: use Draco compression")
		col = row.column(align=True)
		col.prop(context.scene.ss_settings, "use_draco", text="")
		
		# Skip exporting colliders
		row = layout.row()
		col = row.column(align=False)
		col.label(text="Skip export for *_colliders")
		col = row.column(align=True)
		col.prop(context.scene.ss_settings, "skip_colliders", text="")