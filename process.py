import argparse
import os
import subprocess

# exiftool -overwrite_original -"Exposure2012"="-1.0" image-1.dng
# exiftool -s /Volumes/SSD500/Las\ Palmas\ Timelapse/LPA\ DNG/test/image-1.dng > exif_dump.txt


def adjust_exposure(directory, exposure_value):
    # Get a list of all DNG files in the specified directory
    dng_files = [f for f in os.listdir(directory) if f.lower().endswith(".dng")]

    # Check if there are any DNG files in the directory
    if not dng_files:
        print("No DNG files found in the specified directory.")
        return

    for filename in dng_files:
        # Construct the full path to the DNG file
        dng_file = os.path.join(directory, filename)

        # Define the exiftool command
        command = [
            'exiftool',
            f'-overwrite_original',
            f'-Exposure2012={exposure_value}',
            dng_file
        ]

        # Run the exiftool command
        try:
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"Exposure adjusted successfully for {filename}")
        except subprocess.CalledProcessError as e:
            print(f"Error adjusting exposure for {filename}: {e.stderr}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adjust exposure for DNG files in a directory.")
    parser.add_argument("directory", help="Directory containing DNG files.")
    parser.add_argument("exposure_value", type=float, help="Exposure adjustment value.")
    
    args = parser.parse_args()
    
    directory = args.directory
    exposure_value = args.exposure_value
    
    adjust_exposure(directory, exposure_value)
