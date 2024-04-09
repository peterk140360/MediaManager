import os
import subprocess

def convert_jpeg_to_jpg(folder_path):
    # Ensure the folder path is valid
    if not os.path.isdir(folder_path):
        print("Error: Invalid folder path.")
        return

    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.jpeg'):
            # Construct full path to the file
            filepath = os.path.join(folder_path, filename)
            # Construct new filename with '.jpg' extension
            new_filepath = os.path.join(folder_path, os.path.splitext(filename)[0] + '.jpg')
            # Construct command to convert file
            command = ['magick', 'convert', filepath, new_filepath]
            # Execute the command
            subprocess.run(command, shell=True, check=True)
            # Remove the old file (optional)
            os.remove(filepath)
            print(f"Converted: {filename} to {os.path.basename(new_filepath)}")


if __name__ == "__main__":
    # Input for folder path
    folder_path = input("Enter the path of the folder: ")
    # Call function to convert JPEG to JPG
    convert_jpeg_to_jpg(folder_path)
