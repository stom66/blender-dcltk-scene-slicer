#!/bin/bash

# Zips up all .py files, README and LICENSE
# Usage: ./create-release.sh 1.0.0

# Check if the version number is provided as a command-line argument
if [ -z "$1" ]; then
    echo "Usage: $0 <version_number>"
    exit 1
fi

# Set the version number
version="$1"

# Create the releases folder if it doesn't exist
mkdir -p releases

# Generate the zip file name
zip_file="blender-dcl-scene-slicer.v${version}.zip"

# List of files to include in the zip
files="*.py README.md LICENSE.md"

# Zip specified files in the current directory
zip -r "${zip_file}" ${files}

# Move the generated zip file to the releases folder
mv "${zip_file}" releases/

echo "Zip file created: releases/${zip_file}"
