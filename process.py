import argparse
import os
import subprocess
import re

#metadata worth caring about
# Exposure2012 Tint / Contrast2012 / Highlights2012 / Shadows2012 / Whites2012 / Blacks2012 / Texture / Clarity2012 / Dehaze / Vibrance

def find_keyframes(directory):
    dng_files = [f for f in os.listdir(directory) if f.lower().endswith(".dng")]

    keyframes = []
    keyframe_indices = []
    keyframe_exposures = []

    for i, filename in enumerate(dng_files):
        dng_file = os.path.join(directory, filename)
        try:
            result = subprocess.run(['exiftool', dng_file], capture_output=True, text=True)
            output = result.stdout.strip()
            if 'keyframe' in output.lower():
                keyframes.append(filename)
                keyframe_indices.append(i)
                print(f"Found keyframe in {filename}")
                exposureStr = re.search(r'Exposure 2012\s*:\s*([-+]?\d*\.\d+|\d+)', output)
                colorTemperatureStr = re.search(r'ColorTemperature 2012\s*:\s*([-+]?\d*\.\d+|\d+)', output)
                if exposureStr:
                    value = float(exposureStr.group(1))
                    print(f"Exposure 2012: {value}")
                    keyframe_exposures.append(value)
        except subprocess.CalledProcessError as e:
            print(f"Error reading metadata for {filename}: {e.stderr}")

    return keyframes, keyframe_indices, keyframe_exposures

def adjust_exposure(directory, keyframe_data):
    # Get a list of all DNG files in the specified directory
    dng_files = [f for f in os.listdir(directory) if f.lower().endswith(".dng")]

    keyframe_indices = [dng_files.index(name) for name in keyframe_data[0]]

    if len(keyframe_indices) < 2:
        print("At least two keyframes are required for transitions.")
        return
    


    for i in range(len(dng_files)):
        if i in keyframe_indices:
            # Skip keyframe images
            print("not writing data to keyframe")
            continue
        
        # calculate the new exposure value based on the percentage of the way from the previous keyframe to the next
        previous_keyframe_index = max([index for index in keyframe_indices if index < i])
        next_keyframe_index = min([index for index in keyframe_indices if index > i])
        
        print(f"Previous keyframe index: {previous_keyframe_index}")
        print(f"Next keyframe index: {next_keyframe_index}")

        print(f"Current index: {i}")
        
        # Calculate the percentage of the way from the previous keyframe to the next
        percentage_progress = (i - previous_keyframe_index) / (next_keyframe_index - previous_keyframe_index)
        print(f"Percentage: {percentage_progress}")

        range_between_begin_and_end = keyframe_data[2][0] - keyframe_data[2][1]
        
        print(f"Range between begin and end: {range_between_begin_and_end}")

        new_exposure = keyframe_data[2][0] - (range_between_begin_and_end * percentage_progress)

        new_exposure = new_exposure

        # Apply the new exposure value to the current image
        filename = dng_files[i]
        dng_file = os.path.join(directory, filename)

        command = [
            'exiftool',
            f'-overwrite_original',
            f'-Exposure2012={new_exposure}',
            dng_file
        ]

        try:
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"Exposure adjusted successfully for {filename} to {new_exposure}")
        except subprocess.CalledProcessError as e:
            print(f"Error adjusting exposure for {filename}: {e.stderr}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transition Exposure2012 values for DNG files with 'keyframe' metadata in a directory.")
    parser.add_argument("directory", help="Directory containing DNG files.")
    
    args = parser.parse_args()
    
    directory = args.directory

    keyframe_data = find_keyframes(directory)
    print(f"Keyframe files: {keyframe_data}")
    adjust_exposure(directory, keyframe_data)
