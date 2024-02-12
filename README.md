# Blender Scene Slicer

This is a Blender plugin for partitioning a scene and exporting it as a collection of 3D tiles.

It was written for use with the **Infinity Engine** in Decentraland - see the [Decentrally repository](https://github.com/decentraland-scenes/decentrally) for more information.

Installation
--
Go to `Edit > Preferences > Addons > Install` and either select .zip file or the unzipped `main.py` file.

Location
--
`3D Viewport -> Sidebar -> Scene Slicer`

Features
--
* Export tiles to GLtf
* Export tileset data to JSON
* Configurable tile size

ToDo/Bugs:

* Move origin of object
* Clone meshes to export, to apply modifiers and move origin
* Select meshes and selectively export - rather than exporting entire collection
* Support for Draco
* Export cannon-js compatible collider data

How to use
--
* Place your scene in a collection with the prefix `_tileset.`, for example `_tileset.Racetrack01`
* In the **Scene Slicer** sidebar panel: 
    * Configure grid size (see below)
    * Configure output path (see below)
    * Click the "Export Scene" button


### Notes on output path

Blender uses `//` for relative paths. Use `//tiles/` to output to a folder named `tiles` in current file location. This folder must exist.


### Notes on Grid size:

Note: use a grid size < 1/2 your parcel size. Smaller grid sizes will take longer to process. Larger grid sizes will result in the tile being unloaded closer to the player. Suggest using 1/4 parcel size or smaller for good results.

Known issues, limitations and caveats:
--

* Does NOT support Curves, as they don't support bools
* Object visibility is ignored - if it's in the collection, it gets exported