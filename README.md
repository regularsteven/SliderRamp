# LightTime
Utilities for managing timelapse sequences in Lightroom Classic - LightTime


# exiftool -overwrite_original -"Exposure 2012=-1.0" image-1.dng
# exiftool -s /Volumes/SSD500/Las\ Palmas\ Timelapse/LPA\ DNG/test/image-1.dng > exif_dump.txt


exiftool -overwrite_original -"Tint"="0" image-1.dng

exiftool -overwrite_original -"AutoWhiteVersion"="134348800" image-1.dng


exiftool -s image-1.dng


python3 process.py /Volumes/SSD500/Las\ Palmas\ Timelapse/LPA\ DNG/16mm_dusk_boardwalk