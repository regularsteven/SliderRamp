import argparse
import os
import subprocess
import re



def convert_exiftool_output_to_dict(output):
    metadata = {}
    for line in output.splitlines():
        split_line = line.split(":")
        #remove all spaces from the key
        split_line[0] = split_line[0].replace(" ", "")

        typed_value = split_line[1].strip()
        if '+' in typed_value or '-' in typed_value or typed_value == "0":
            metadata[split_line[0].strip()] = float(split_line[1].strip())
        elif typed_value == "True" or typed_value == "False":
            metadata[split_line[0].strip()] = bool(split_line[1].strip())
        else:
            metadata[split_line[0].strip()] = split_line[1].strip()
    return metadata


#metadata worth caring about
# Exposure2012 Tint / Contrast2012 / Highlights2012 / Shadows2012 / Whites2012 / Blacks2012 / Texture / Clarity2012 / Dehaze / Vibrance

def find_keyframes(directory):
    dng_files = [f for f in os.listdir(directory) if f.lower().endswith(".dng")]

    #sort the the files by index number in filename
    dng_files.sort(key=lambda f: int(re.sub('\D', '', f)))
    # 
    
    keyframes = []
    keyframe_indices = []
    keyframe_exposures = []

    metadata = []

    

    for i, filename in enumerate(dng_files):
        dng_file = os.path.join(directory, filename)
        try:
            result = subprocess.run(['exiftool', "-Tint", "-ColorTemperature", "-Exposure2012", "-Subject", dng_file], capture_output=True, text=True)
            output = result.stdout.strip()
            if 'keyframe' in output.lower():

                resp = {}

                keyframes.append(filename)
                resp["filename"] = output

                keyframe_indices.append(i)

                resp["indicies"] = [i]

                print(f"Found keyframe in {filename}")
                
                data = convert_exiftool_output_to_dict(output)
                data["filename"] = filename
                data["index"] = i
                metadata.append(data)

        except subprocess.CalledProcessError as e:
            print(f"Error reading metadata for {filename}: {e.stderr}")

    return keyframes, keyframe_indices, keyframe_exposures, metadata

def calc_value_between_two_values(values, percentage):
    range_between_begin_and_end = values[0] - values[1]
    return values[0] - (range_between_begin_and_end * percentage)
    


def adjust_exposure(directory, keyframe_data):
    # Get a list of all DNG files in the specified directory
    dng_files = [f for f in os.listdir(directory) if f.lower().endswith(".dng")]
    dng_files.sort(key=lambda f: int(re.sub('\D', '', f)))

    keyframe_indices = keyframe_data[1] #[dng_files.index(name) for name in keyframe_data[0]]

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

        keyToManage = "Exposure2012"
        keys = [keyframe_data[3][0][keyToManage], keyframe_data[3][1][keyToManage]]
        new_exposure = calc_value_between_two_values(keys, percentage_progress)

        keyToManage = "Tint"
        keys = [keyframe_data[3][0][keyToManage], keyframe_data[3][1][keyToManage]]
        new_tint = int(calc_value_between_two_values(keys, percentage_progress))
        
        keyToManage = "ColorTemperature"
        keys = [9205, 3150]
        
        new_color_temperature = int(calc_value_between_two_values(keys, percentage_progress))
        

        # Apply the new exposure value to the current image
        filename = dng_files[i]
        dng_file = os.path.join(directory, filename)
        #new_tint = 10
        command = [
            'exiftool',
            f'-overwrite_original',
            f'-Exposure2012={new_exposure}',
            f'-Tint={new_tint}',
            f'-ColorTemperature={new_color_temperature}',
            
            dng_file
        ]
        #['exiftool', '-overwrite_original', f'-Exposure2012={exposure_value}', f'-Tint={tint_value}', image_file]

        try:
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)



            print(f"Adjusted successfully : {command}")
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
