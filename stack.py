import os
import rawpy
from PIL import Image, ImageChops

# Specify the directory containing your DNG files
input_directory = '/Volumes/SSD500/Las\ Palmas\ Timelapse/LPA\ DNG/test/'

# Get a list of DNG files in the directory
dng_files = [f for f in os.listdir(input_directory) if f.lower().endswith('.dng')]

if not dng_files:
    print("No DNG files found in the specified directory.")
    exit()

# Sort DNG files by name to ensure the correct order
dng_files.sort()

# Create an empty image as the final result
final_image = None

for dng_file in dng_files:
    dng_path = os.path.join(input_directory, dng_file)

    # Open and process the DNG file using rawpy
    with rawpy.imread(dng_path) as raw:
        # Convert the DNG image to a PIL image (RGB)
        rgb_image = raw.postprocess()

    # Convert the PIL image to grayscale
    grayscale_image = rgb_image.convert('L')

    # Create a PIL image with an alpha channel to store the cumulative result
    if final_image is None:
        final_image = Image.new('LA', grayscale_image.size)

    # Blend the grayscale image with the cumulative result using the "lighten" mode
    final_image = ImageChops.lighter(final_image, grayscale_image)

# Save the final stacked image as a DNG file
output_path = input_directory + '/result.dng'
final_image.save(output_path, format='DNG')

print(f"Stacking complete. The stacked image is saved at: {output_path}")
