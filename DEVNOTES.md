# Dev Notes

Misc notes for development.

Dev environment:

* project folder is in `%APPDATA%\Roaming\Blender Foundation\Blender\4.0\scripts\addons\blender-dcltk-scene-slicer`
* VSCode plugins
    * https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development
    * https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy
    

## Releasing new versions

The GitHub repository is configured with a workflow action to create a release zip upon pushing a new tag.

Create and push a tag:

```sh


# Create and push a tag:
git tag 1.0.0
git push origin 1.0.0`
```

Remove a tag:
```sh
# Create and push a tag:
git --delete tag 1.0.0
git push --delete origin 1.0.0`
```
