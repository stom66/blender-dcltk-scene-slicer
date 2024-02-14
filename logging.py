import bpy



# ██╗      ██████╗  ██████╗  ██████╗ ██╗███╗   ██╗ ██████╗
# ██║     ██╔═══██╗██╔════╝ ██╔════╝ ██║████╗  ██║██╔════╝
# ██║     ██║   ██║██║  ███╗██║  ███╗██║██╔██╗ ██║██║  ███╗
# ██║     ██║   ██║██║   ██║██║   ██║██║██║╚██╗██║██║   ██║
# ███████╗╚██████╔╝╚██████╔╝╚██████╔╝██║██║ ╚████║╚██████╔╝
# ╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝
#

LOG_PATH = "scene_slicer.log"

def Log(*args):
	"""
	Prints the log message composed of the provided arguments and writes it to the LOG_TXT file.

	Args:
	*args: Variable number of arguments to be included in the log message.
	"""

	if LOG_PATH not in bpy.data.texts:
		LOG_TXT = bpy.data.texts.new(LOG_PATH)
	else:
		LOG_TXT = bpy.data.texts[LOG_PATH]

	formatted_args = [f"{arg:.6f}" if isinstance(arg, float) else str(arg) for arg in args]
	message = ' '.join(formatted_args)
	print(message)
	LOG_TXT.write(message + '\n')

def LogReset():
	if LOG_PATH in bpy.data.texts:
		bpy.data.texts[LOG_PATH].clear()