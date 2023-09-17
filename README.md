# LightTime
Utilities for adjusting settings over time for timelapse sequences in Lightroom Classic


# exiftool -overwrite_original -"Exposure 2012=-1.0" image-1.dng
# exiftool -s /Volumes/SSD500/Las\ Palmas\ Timelapse/LPA\ DNG/test/image-1.dng > exif_dump.txt


exiftool -overwrite_original -"Tint"="0" image-1.dng

exiftool -overwrite_original -"AutoWhiteVersion"="134348800" image-1.dng


# Requirements
Python 3.11
exiftool - https://exiftool.org/install.html
DNG files - with filenames in sequence (e.g. my_shot_1.dng, my_shot_2.dng, etc), in a specific folder
 - This only works with DNG files for now
- DNGs must have the metadata stored in the file (CMD+S in Lightroom / Metadata > Save Metadata to file) 
Adobe Lightroom Classic, with specific folders added to Catalogue Folders. Save is only required on keyframes.

# Usage:
1) Clone repo
 - `git clone https://github.com/regularsteven/LightTime.git`

2) Set start and end keyframe in Lightroom, by adding "keyframe" as a keyword to the metadata
 - Note; this only works with two keyframes for now. Plan to support many keyframes.
 - Also add 'temp_', with the color temperature value of the keyframe image. Eg 'temp_4420'. - This is hack, as reading the color temperature from the DNG isn't so obvious.

3) Current transtions support color temperature, tint and exposure, from included metadata. Note the hack solution for the color temperature.

4) Run script from cloned repo, targeting the folder with DNGs eg:
- run `python3 process.py /Volumes/SSD500/Las\ Palmas\ Timelapse/LPA\ DNG/test`

5) At completion, read the metadata from the updated DNG files inside of Lightroom


# Troubleshooting
Do you have Python installed? Run `python -v` to make sure you have version 3.11 (other versions may work).
Is exiftool installed? Run `exiftool -s image-1.dng` on your image to verify you can extract metadata.

# Issues
Current approach of keyframe is very limited, and must be on first and last images in folder. This will be fixed.
White Balance (ColorTemperature) issue is hacky, and need to find a solution.
Need to implement a simple method to run this utility. Commandline is yuk for most people.
And so much more... Need to add support for
    • Contrast2012 • Highlights2012 • Shadows2012 • Whites2012 • Blacks2012 • Texture • Clarity2012 • Dehaze • Vibrance and so on
Will also add support for transitions of masks.
