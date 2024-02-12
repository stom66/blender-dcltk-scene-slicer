#    <Scene Slicer - Blender addon for exporting a scene in a confiruable grid of 3d tiles>
#
#    Copyright (C) <2024> <Tom Steventon>
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
	"name"       : "Scene Slicer",
	"description": "Exporter tool for partitioning a scene into a collection of 3d tiles",
	"author"     : "Tom Steventon - stom66",
	"version"    : (1, 0, 0),
	"blender"    : (3, 6, 0),
	"location"   : "3D Viewport -> Sidebar -> Scene Slicer",
	"description": "Scene Slicer",
	"category"   : "Import-Export",
	"doc_url"    : "https://github.com/stom66/blender-scene-slicer"
}

from .main import *