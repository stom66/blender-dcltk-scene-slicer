import bpy

from . _main import EXPORT_OT_SceneSlicer_Export, EXPORT_OT_SceneSlicer_Preview

# Define a variable to hold bl_info
try:
    from . import bl_info
except ImportError:
    bl_info = None

# ███████╗███████╗    ███████╗██╗  ██╗██████╗  ██████╗ ██████╗ ████████╗
# ██╔════╝██╔════╝    ██╔════╝╚██╗██╔╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝
# ███████╗███████╗    █████╗   ╚███╔╝ ██████╔╝██║   ██║██████╔╝   ██║   
# ╚════██║╚════██║    ██╔══╝   ██╔██╗ ██╔═══╝ ██║   ██║██╔══██╗   ██║   
# ███████║███████║    ███████╗██╔╝ ██╗██║     ╚██████╔╝██║  ██║   ██║   
# ╚══════╝╚══════╝    ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
#             
#

# UI button to refresh collection dropdown
class SCENE_OT_SceneSlicer_RefreshCollections(bpy.types.Operator):
	bl_idname  = "ss.btn_refresh_collections"
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
		
		split = row.split(factor=0.4)
		split.label(text="Export collection")

		split2 = split.split(factor=0.8)
		col = split2.column(align=True)
		col.prop(context.scene.ss_settings, "export_collection", text="")
		col = split2.column(align=True)
		col.operator("ss.btn_refresh_collections", text="", icon='FILE_REFRESH')

		# Output path
		row = layout.row()
		split = row.split(factor=0.4)

		split.label(text="Output folder")
		split.prop(context.scene.ss_settings, "output_path", text="")

		# Grid size
		row = layout.row()
		row.label(text="Grid size")
		row = layout.row()
		row.prop(context.scene.ss_settings, "tile_dimensions", text="")

		# Btn: Preview
		row = layout.row()
		row.operator(EXPORT_OT_SceneSlicer_Preview.bl_idname, text="Preview", icon="HIDE_OFF")

		# Btn: Slice and Export
		row = layout.row()
		row.operator(EXPORT_OT_SceneSlicer_Export.bl_idname, text="Slice and Export", icon="FILE_VOLUME")

		# Progress
		row = layout.row()
		split = layout.split(factor=0.4)

		col = split.column(align=True)
		col.label(text="Export progress")
		
		col = split.column()
		col.progress(factor = bpy.context.scene.ss_settings.export_progress, 
					 type   = 'BAR', 
					 text   = bpy.context.scene.ss_settings.export_text)


# ███████╗███████╗    ███████╗███████╗████████╗████████╗██╗███╗   ██╗ ██████╗ ███████╗
# ██╔════╝██╔════╝    ██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗  ██║██╔════╝ ██╔════╝
# ███████╗███████╗    ███████╗█████╗     ██║      ██║   ██║██╔██╗ ██║██║  ███╗███████╗
# ╚════██║╚════██║    ╚════██║██╔══╝     ██║      ██║   ██║██║╚██╗██║██║   ██║╚════██║
# ███████║███████║    ███████║███████╗   ██║      ██║   ██║██║ ╚████║╚██████╔╝███████║
# ╚══════╝╚══════╝    ╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝
#              
																			   
class VIEW3D_PT_SceneSlicer_Options(bpy.types.Panel):
	bl_label       = 'Scene Slicer: Advanced Settings'
	bl_category    = 'DCL Toolkit'
	bl_region_type = 'UI'
	bl_space_type  = 'VIEW_3D'
	bl_options     = { 'DEFAULT_CLOSED' }

	def draw(self, context):
		layout = self.layout

		# Version
		row = layout.row()
		col = row.column(align=True)
		col.label(text="Plugin version")

		col = row.column(align=True)
		if bl_info:
			plugin_version = ".".join(map(str, bl_info["version"]))
			col.label(text=plugin_version)

		# Bool solver method
		row = layout.row()
		col = row.column(align=False)
		col.label(text="Bool solver method")
		col = row.column(align=True)
		col.prop(context.scene.ss_settings, "bool_solver", text="")

		# Skip exporting colliders
		row = layout.row()
		col = row.column(align=False)
		col.label(text="Ignore '_collider' meshes")
		col = row.column(align=True)
		col.prop(context.scene.ss_settings, "skip_colliders", text="")

		# Minify JSON
		row = layout.row()
		col = row.column(align=False)
		col.label(text="JSON minify")
		col = row.column(align=True)
		col.prop(context.scene.ss_settings, "minify_json", text="")
	
		# glTF settings
		row = layout.row()
		row.label(text="glTF settings:")
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

		# File prefix
		row = box.row()
		row.label(text="Filename prefix")
		col = row.column(align=True)
		col.prop(context.scene.ss_settings, "output_prefix", text="")

		# Swizzle
		row = box.row()
		col = row.column(align=False)
		col.label(text="Swizzle YZ")
		col = row.column(align=True)
		col.prop(context.scene.ss_settings, "swizzle_yz", text="")

		# Tile origin
		row = box.row()
		row.label(text="Tile origin")
		col = row.column(align=True)
		col.prop(context.scene.ss_settings, "export_origin", text="")

